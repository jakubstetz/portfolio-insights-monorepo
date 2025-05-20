FROM python:3.12-slim

WORKDIR /app

COPY . .

EXPOSE 8001

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]