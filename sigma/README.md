# Sigma
Turns TV on and off. Run on a Raspberry Pi 3 connected to TV via HDMI.

# Services Used
* [SQS](https://console.aws.amazon.com/sqs/home)
* [AWS Lambda](https://console.aws.amazon.com/lambda/home)
* [Alexa Skills Kit](https://developer.amazon.com/edw/home.html#/skills/list)

# Example Invocation
> Alexa, ask sigma to turn the TV off.

# Setting up the Lambda
* Create new lambda using the code in `lambda.py`
* It has no extra dependencies so you can edit the code inline.
* Give the lambda a role that can write to SQS.
* Configure the `queue` environment variable with the URL of the SQS queue.

# Run the local service
The local service is run with Docker on ARM architecture (a.k.a. raspberry pi)

## Create your local.env
The container is configured via an environment file. See `local.env` for an example of the keys that need to be configured.

## Build the image
`docker build . -t sigmapy`

## Setup crontab
To start the service on boot, edit crontab:

```
crontab -e 
@reboot /usr/bin/docker run --net=host --device=/dev/vchiq --env-file /absolute/path/to/your/local.env sigmapy:latest
```

# Useful links
* [Tool for creating CEC commands](http://www.cec-o-matic.com/)
* [What brand TVs support CEC](http://libcec.pulse-eight.com/vendor/support)
