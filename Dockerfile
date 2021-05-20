FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python git 
RUN git clone https://github.com/pursuitdan/integration
WORKDIR /yuting/integration
cmd ["ls"]
# run python integration.py
# CMD ["python", "integration.py"]
