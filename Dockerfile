FROM python:3.10-slim

WORKDIR /usr/scr/app

COPY requirements.txt ./

RUN apt-get update

RUN apt-get install libmariadb-dev -y
RUN apt-get install gcc -y

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install pydantic[email]

COPY . .

CMD ["uvicorn", "app_orm:app", "--host=0.0.0.0", "--port=8000"]

