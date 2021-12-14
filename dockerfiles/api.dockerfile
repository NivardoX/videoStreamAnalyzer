FROM python:3.8-slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
CMD ["flask"  , "run", "--host=0.0.0.0"]
#CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:flask_app"]