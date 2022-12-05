FROM python:3-alpine

WORKDIR palti_app

COPY src .
COPY ./requirements.txt .
RUN pip install -r requirements.txt

CMD ["python3" ,"app.py"]
