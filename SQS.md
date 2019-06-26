## SQS


### Local SQS
Local SQS is ran in the sqs docker-compose service container. The lambda handlers is ran in the sqsrunner docker-compose service container that executes commands in ./src/local_sqs_runner.py. Uncommenting the sqsrunner in the docker-compose yaml will run a consumer for all queues configured in the `mtaws.data.sqs.QueueUrls` enum. The consumer sends the sqs messages to the sqs_handler.py lambda handler in the same format as on AWS. You can also leave the sqsrunner off and start a consumer for a specific queue by running a cli command in the api container.    
` docker exec -it $(docker container list --format="{{ .Names }}" | grep api) python local_sqs_runner.py start-listener {NAME-OF-QUEUE}`

NOTE: that since the local_sqs_runner.py runs in memory you will need to restart the consumer for any changes made to SQS code. If using the sqsrunner docker-compose service just restart that specific service.   

`docker-compose.yaml restart -t 1 sqsrunner`   

if using mac specific docker-compose yaml   

`docker-compose -f docker-compose-mac.yml restart -t 1 sqsrunner`

### Add new queue to local SQS
To add a new SQS queue locally edit the elasticmq.conf file located at:   
`./docker/sqs/conf/elasticmq.conf`   
Then rebuild the docker-comppose container stack for the new queue to start running