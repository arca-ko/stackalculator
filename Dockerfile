# syntax=docker/dockerfile:1

FROM python:alpine
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "app.py" ]
EXPOSE 5000
