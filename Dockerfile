FROM python:3.10

EXPOSE 8080

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "deploy_framework.py"]