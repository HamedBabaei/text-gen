FROM python:3

RUN mkdir /app

COPY ./requirenments.txt /app/requirenments.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirenments.txt

COPY . .

ENTRYPOINT ["python3"]

CMD ["app.py"]