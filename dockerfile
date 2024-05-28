FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all directory to container
COPY . /app

# Install addons from requirments 
RUN pip install --no-cache-dir -r requirements.txt

# PORT 5000 to the flask app
EXPOSE 5000

ENV FLASK_APP=main.py

# Start the app
CMD ["flask", "run", "--host=0.0.0.0"]
