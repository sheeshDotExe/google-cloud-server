FROM python:3.10.5-alpine

RUN mkdir /app
WORKDIR /app

COPY . .

RUN chmod +x main.py
RUN pip install -r requirements.txt

EXPOSE 4444

ENTRYPOINT [ "python", "main.py", "0.0.0.0", "4444"]