FROM python:3.8

WORKDIR /better.me

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . /better.me

CMD streamlit run --server.port 8080 --server.enableCORS false app.py

