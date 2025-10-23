FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY flask_api.py .
COPY optimized_research_agent.py .

# Expose port
EXPOSE 5000

# Set environment variable (override at runtime)
ENV ANTHROPIC_API_KEY=""

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "flask_api:app"]
