FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
