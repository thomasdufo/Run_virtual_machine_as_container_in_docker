FROM python:3.10

WORKDIR /app


RUN pip install --no-cache-dir flask requests python-dotenv gunicorn docker 
#mysql-connector-python cryptography


COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
 #a laisser en 0.0.0.0:5000 car ecoute a l interieur du container


