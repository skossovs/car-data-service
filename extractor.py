# https://www.crummy.com/software/BeautifulSoup/bs4/doc/


import json
import time
import requests 
from bs4 import BeautifulSoup
from utils import left

timeDelay = 9 # between the requests in seconds
urlBase   = 'https://www.autotrader.com/cars-for-sale/all-cars/'
ulrEnding = 'isNewSearch=true&marketExtension=include&numRecords=100&searchRadius=400&sortBy=relevance&zip=37379'

def isFactEmpty(aString):
    if aString is None: return True
    if aString.string is None: return True
    #fucked up language: using exception instead of proper check
    try:
        aString.string  == 'doesnt matter'
    except:
        return True
    return False

class Car:
    def __init__(self, make, model, mileage, price, originalName):
        self.make = make
        self.model = model
        self.mileage = mileage
        self.price = price
        self.originalName = originalName

def parseExtractedFields(name: any, makeFilter:any, miles: any, price: any):
    originalName = name.string
    name  = str.replace(name.string,'Certified ','')
    name  = str.replace(name, 'Used ','')
    year  = left(name,4)
    name  = str.replace(name, year + ' ', '')
    make  = str.replace(makeFilter, '/', '').upper()
    name  = str.upper(name)
    model = str.replace(name, make, '').strip()
    miles = str.replace(miles.string,',','')
    miles = str.replace(miles,' miles','')
    price = str.replace(price.string,',','')
    return Car(make, model, miles, price, originalName)

def obj_dict(obj):
    return obj.__dict__

def extractCarData(makeFilter: any, modelFilter: any, nPages: any, latestYear: any):
    # creating list
    lstCars = []

    for i in range(1, nPages):
        firstRecordNum = i * 100
        firstRecord = '?firstRecord=' + str(firstRecordNum) +'&'
        endYear     = 'endYear='+ str(latestYear) +'&'
        url = urlBase  + makeFilter + '/' + modelFilter + '/soddy-daisy-tn' + firstRecord + endYear + ulrEnding
        print ('requested URL: ' + url)
        #url = 'https://www.autotrader.com/cars-for-sale/all-cars?zip=37379&makeCodeList=BMW&seriesCodeList=3_SERIES'  # Replace this with the URL of the website you want to scrape
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Continue with parsing the HTML content
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            # cars tags
            #<div class="item-card-body margin-bottom-auto"><div data-cmp="positionedOverlay" class="positioned-overlay"><div class="positioned-overlay-wrapper"><div data-cmp="positionedOverlayBase" class="positioned-overlay-base"><div class="padding-left-3 inventory-listing-body padding-top-3 padding-right-3 margin-bottom-2" role="link" tabindex="0"><div class="row"><div class="text-left col-xs-8"><div class="display-flex justify-content-between"><a rel="nofollow" href="/cars-for-sale/vehicledetails.xhtml?listingId=681860265&amp;allListingType=all-cars&amp;city=Soddy%20Daisy&amp;isNewSearch=false&amp;makeCodeList=BMW&amp;referrer=%2Fcars-for-sale%2Fall-cars%3Fzip%3D37379%26makeCodeList%3DBMW%26seriesCodeList%3D3_SERIES&amp;searchRadius=50&amp;seriesCodeList=3_SERIES&amp;state=TN&amp;zip=37379&amp;clickType=listing"><h3 data-cmp="subheading" class="text-bold text-size-300 link-unstyled">Used 2020 BMW 330i Sedan</h3></a></div><div class="display-grid text-subdued-lighter padding-0"><div class="list-truncated text-size-200">Premium Pkg&nbsp;&nbsp;•&nbsp;&nbsp;Parking Assistance Pkg</div></div><div class="row"><div class="item-card-specifications col-xs-9 margin-top-4 text-subdued-lighter"><span class="text-bold">25,504 miles</span><div></div></div></div></div><div class="margin-left-auto col-xs-4 text-right pull-right"><div data-cmp="pricing" class="text-gray-base text-bold text-size-500"><span class="first-price" data-cmp="firstPrice">33,999</span></div><div><div class="text-right"><div class="text-right" data-cmp="lnk-pymt-dtls"><span class="text-link text-size-200 display-block" role="link" tabindex="0"><span class="text-bold text-size-300 first-price text-blue-darker">701</span><span class="text-bold text-size-300 text-blue-darker">/mo.</span><span class="display-block text-link text-size-200">See&nbsp;Details</span></span></div></div></div></div></div></div></div><div data-cmp="positionedOverlayAnchor" class="positioned-overlay-anchor topRight"><div class="offset-top-50"><div class=""><div data-cmp="positionedOverlay" class="positioned-overlay display-flex"><div class="positioned-overlay-wrapper"><div data-cmp="positionedOverlayBase" class="positioned-overlay-base"><div class="ribbon text-bold right ribbon-good-price text-size-200 margin-vertical-1 padding-left-3"><div class="ribbon-content-right">GOOD PRICE</div></div></div><div data-cmp="positionedOverlayAnchor" class="positioned-overlay-anchor topLeft"><div style=""><img class="media-gallery-viewer order-2" height="34" width="25" alt="KBB.com Price Advisor" src="https://www.autotrader.com/content/dam/autotrader/additionalresources/kbb_logo.svg" loading="lazy" style="right: 17px;"></div></div></div></div></div></div></div></div></div></div>
            tags = soup.find_all('div', class_='item-card-body margin-bottom-auto')

            for tag in tags:
                #print('*******  CAR DATA    *************')
                #print(tag.prettify())
                name = tag.find('h3', class_="text-bold text-size-300 link-unstyled")
                
                miles = tag.find('span', class_="text-bold")
                #item-card-specifications
                if isFactEmpty(miles) :
                    miles = tag.find('div', class_='item-card-specifications')
                else: 
                    if miles.string == "Reduced Price" or miles.string == "Newly Listed":
                        miles = tag.find('div', class_='item-card-specifications')
                
                price = tag.find('span', class_="first-price")
                ## print out
                if price is not None and price.string != None and price.string != 'KBB.com Dealer Rating':
                    if name is not None and name.string != None:
                        if miles is not None and miles.string != None:
                            lstCars.append(parseExtractedFields(name, makeFilter, miles, price))
                            #outputConsole(name, miles, price)
                price = None
                name  = None
                miles = None
        else:
            print(f"Failed to fetch the web page. Status code: {response.status_code}")
        time.sleep(timeDelay)
    # lst to JSON
    jsonList = json.dumps(lstCars, default=obj_dict)
    return jsonList