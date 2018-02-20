FROM python:3.6

MAINTAINER "Eugene Alekseev"

RUN pip install tensorflow numpy

WORKDIR /app

COPY . /app

EXPOSE 80

ENTRYPOINT ["python", "21.py"]

CMD ["--up", "7", "--down", "5", "--right", "6", "--left", "5"]