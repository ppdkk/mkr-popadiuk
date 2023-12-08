FROM python:latest
LABEL authors="ppdkk"
LABEL description="TRSPO"

WORKDIR /opt/project
COPY . /opt/project

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 12345

CMD ["python", "main.py"]
