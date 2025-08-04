FROM python:3.11-slim
WORKDIR /app
COPY agent.py .
COPY config /app/config
RUN pip install requests
CMD ["python", "agent.py"]
