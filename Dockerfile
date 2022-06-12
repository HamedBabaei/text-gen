FROM python:3

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirenments1.txt
RUN python -m spacy download en_core_web_sm

ENTRYPOINT ["python3"]

CMD ["python", "test_app.py", "runserver", "0.0.0.0:5000"]