FROM python:3.8

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY btb_world_maker /app

EXPOSE 8080
CMD [ "python", "worldmaker.py" ]
