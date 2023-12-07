FROM python:latest
LABEL authors="ppdkk"
LABEL description="TRSPO"

WORKDIR /opt/project
COPY . /opt/project

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 12345

# Run app.py when the container launches
CMD ["python", "main.py"]
