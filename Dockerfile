FROM python:3.9.18

ADD extractor.py .
ADD utils.py .
ADD main.py .
RUN pip install bs4
RUN pip install requests

CMD ["python", "./main.py"]