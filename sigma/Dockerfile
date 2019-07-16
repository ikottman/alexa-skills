FROM blakeblackshear/rpi-hdmi-cec-rest

WORKDIR /opt/sigma/

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install boto3

COPY sigma.py /opt/sigma/

CMD ["/usr/bin/python3", "/opt/sigma/sigma.py"]