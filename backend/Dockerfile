# Stage 1: Build
FROM python:3.13-alpine AS builder

WORKDIR /app

COPY requirements.txt .

# Installiamo tutto ciò che serve per compilare pacchetti Python
RUN apk add --no-cache gcc musl-dev libffi-dev

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runtime
FROM python:3.13-alpine

WORKDIR /app

# Installiamo netcat per il wait-for-postgres
RUN apk add --no-cache netcat-openbsd

# Copiamo solo i pacchetti installati
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app .

# Copiamo anche lo script di attesa
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/wait-for-postgres.sh"]
