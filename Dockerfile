# 基础镜像 python3.7
FROM python:3.7
# 设置工作目录
WORKDIR /app

# 复制requirements.txt到工作目录
COPY requirements.txt /app/
# 复制scrapy项目到工作目录
COPY . /app/

# 安装依赖pwd


RUN cd /app \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 设置环境变量
ENV SCRAPY_SETTINGS=tdscrapy.settings

# 运行scrapy
CMD ["scrapy", "crawl", "eastmoney"]