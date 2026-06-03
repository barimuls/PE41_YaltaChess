# 1. Use an official Python runtime as a base image
FROM python:3.14-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your dependency file first (for better caching)
COPY requirements.txt .

# 4. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Run your python file when the container starts
CMD ["python", "Code/Evaluation_classement.py"]
