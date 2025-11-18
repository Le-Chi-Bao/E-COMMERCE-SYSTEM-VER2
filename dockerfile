FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8866

# Dùng shell form để đảm bảo env variables work
CMD python web/app.py