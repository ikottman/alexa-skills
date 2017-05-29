# Sigma
Turns TV on and off. Run on a Raspberry Pi 3 connected to TV via HDMI.

# Services Used
* [SQS](https://console.aws.amazon.com/sqs/home)
* [AWS Lambda](https://console.aws.amazon.com/lambda/home)
* [Alexa Skills Kit](https://developer.amazon.com/edw/home.html#/skills/list)

# Example Invocation
> Alexa, tell TV to turn off.

# Setting up the Lambda
* Create new lambda using the code in `lambda.py`
* It has no extra dependencies so you can edit the code inline.
* Give the lambda a role that can write to SQS.
* Configure the `queue` environment variable with the URL of the SQS queue.

# How to Run Local Service

## Install CEC
sudo apt-get update
sudo apt-get cec-utils

## Start service
nohup python sigma.py &

# Useful links
* [Tool for creating CEC commands](http://www.cec-o-matic.com/)
* [What brand TVs support CEC](http://libcec.pulse-eight.com/vendor/support)
