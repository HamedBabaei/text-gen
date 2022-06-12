FROM python:3

RUN mkdir /app

WORKDIR /app


COPY . /app/

RUN pip install --no-cache-dir -r requirenments1.txt

ENTRYPOINT ["python3"]

CMD ["python", "test_app.py", "runserver", "0.0.0.0:5000"]