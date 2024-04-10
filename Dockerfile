FROM python:3.12

EXPOSE 8080

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "mcbound_framework.py"]