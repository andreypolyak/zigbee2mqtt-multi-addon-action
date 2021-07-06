FROM python:3.8-slim-buster
ADD . /app
WORKDIR /app
RUN pip install --target=/app PyGithub

CMD ["python3", "/app/main.py"]