FROM python:3.10.2

MAINTAINER llody55

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD ["python", "app.py"]