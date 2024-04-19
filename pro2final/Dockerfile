# 使用官方 Python 运行时作为父镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY . /app

# 安装 requirements.txt 中的所有依赖
RUN pip install --no-cache-dir -r requirements.txt

# 让端口 5000 可用于外界访问
EXPOSE 5000

# 定义环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 使用 flask 命令运行应用
CMD ["flask", "run"]
