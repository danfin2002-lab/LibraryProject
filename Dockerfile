FROM python:3.12.3-bookworm

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x ./prestart.sh

ENTRYPOINT ["./prestart.sh"]

CMD ["python", "main.py"]