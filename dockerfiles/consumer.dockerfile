FROM python:3.8-slim
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD ["celery", "-A", "app", "worker", "-l", "INFO"]