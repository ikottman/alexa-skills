# Office Hours
Determines if a local business is open.

# Services Used
* [AWS Lambda](https://console.aws.amazon.com/lambda/home)
* [Alexa Skills Kit](https://developer.amazon.com/edw/home.html#/skills/list)
* [AWS Key Management Service](https://aws.amazon.com/kms/)

# Example Invocation
> Alexa, ask office hours if taco bell is open.

# Deployment Commands
Adding code dependencies:

`pip install <package> -t ./dependencies/`

Zip code and dependencies:

`zip -r office_hours.zip ./`
