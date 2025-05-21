FROM python:3.12-slim

WORKDIR /app

COPY . .

# Note that if deployment port is adjusted then EC2 NGINX reverse-proxy configuration should also be updated
EXPOSE 8001

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]