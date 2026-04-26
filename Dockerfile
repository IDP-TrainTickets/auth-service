FROM python:3.9-slim
WORKDIR /app
RUN pip install flask flask-sqlalchemy pyjwt psycopg2-binary werkzeug
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
