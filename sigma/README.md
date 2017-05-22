# Sigma
Turns TV on and off. Run on a raspberry pi 3 connected to TV via HDMI.

# Services Used
* [SQS](https://console.aws.amazon.com/sqs/home)
* [Alexa Skills Kit](https://developer.amazon.com/edw/home.html#/skills/list)

# Example Invocation
> Alexa, tell TV to turn off.

# How to Run

## Install CEC
sudo apt-get update
sudo apt-get cec-utils

## Start service
nohup python sigma.py &
