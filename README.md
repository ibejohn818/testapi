# MT AWS API

Visit confluence for more:
https://confluence.godaddy.com/display/managedAWS/MT+AWS+API


## Local Dev

Local dev using `docker-compose` [click here for docs](docker/README.md)
 
## SQS
More on the SQS implementation can be found [here](SQS.md)

 
## AWS / Nimbi
 
 The AWS infra is defined in a `nimbi` infra.py file.  
 To build & deploy the api to lambda use the following make command:  
 `make build-lambda`

