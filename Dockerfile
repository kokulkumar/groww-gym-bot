FROM python:3.11-slim
WORKDIR /srv
COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r /srv/requirements.txt
COPY mvp /srv/mvp
ENV PORT=7860
CMD ["sh", "-c", "uvicorn mvp.server:app --host 0.0.0.0 --port ${PORT}"]
