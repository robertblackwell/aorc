# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /aorc

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY aorc/ ./aorc

copy runner.py ./runner.py

# command to run on container start
CMD [ "python", "./runner.py" ] 