FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# Install system deps and Python requirements
COPY requirements.txt /workspace/requirements.txt
RUN apt-get update \
    && apt-get install -y build-essential curl \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --upgrade pip setuptools \
    && pip install -r /workspace/requirements.txt

# Copy the workspace
COPY . /workspace

EXPOSE 8888

ENV JUPYTER_TOKEN=secret

CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=$JUPYTER_TOKEN --NotebookApp.allow_origin='*'"]
