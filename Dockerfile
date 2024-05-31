# 第一阶段
FROM python:3.10.2-slim as builder

# 设置环境变量
ENV PIP_CACHE_DIR=/app/.cache 

WORKDIR /app

ADD  sources.list /etc/apt

COPY requirements.txt .

# 使用指定的源来安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



# 第二阶段
FROM python:3.10.2-slim

LABEL maintainer="llody55"

COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]
