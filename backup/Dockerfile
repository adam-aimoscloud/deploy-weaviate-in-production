FROM shentu-registry-registry-vpc.cn-shanghai.cr.aliyuncs.com/base/python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

CMD ["python", "main.py"]
