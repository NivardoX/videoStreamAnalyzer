FROM python:3.8-slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD ["python3", "main.py"]