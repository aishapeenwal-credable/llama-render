FROM debian:bullseye-slim

WORKDIR /app

# Install dependencies
RUN apt update && apt install -y \
    build-essential cmake curl git python3 python3-pip wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Clone llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && \
    make LLAMA_CUBLAS=1

# Copy API server
COPY server.py .

# Optionally copy model
COPY models/ ./models/

EXPOSE 8000

CMD ["python3", "server.py"]
