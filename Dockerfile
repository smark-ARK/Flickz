# 1. Specify a base image
FROM python:3.8.16
# 2. Set a working directory
WORKDIR /app  

# 3. Copy requirements file
COPY requirements.txt requirements.txt  

# 4. Install dependencies
RUN pip install -r requirements.txt  

# 5. Copy application code
COPY . .  

# 6. Expose the port for the API
EXPOSE 8000  



# 7. Define the command to start the API
ENTRYPOINT ["sh", "./entrypoint.sh"]
