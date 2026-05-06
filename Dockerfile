# Use a slim Python image to save space
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (this speeds up builds by caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]