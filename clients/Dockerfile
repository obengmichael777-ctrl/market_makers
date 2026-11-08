FROM python:3.11-slim

WORKDIR /app

# Copy dependency manifest and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy client code and configuration
COPY client.py .
COPY client.cfg .

# Run the client
CMD ["python", "client.py"]