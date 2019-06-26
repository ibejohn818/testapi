## Local Dev w/Docker

------------
#### *Docker-Sync

There is an optimized for mac docker-compose setup using `docker-sync`.   
docker-sync can reduce loads by using container volumes and syncing w/UNISON (APFS/HFS are junk with read/write docker volumes)

*we suggest installing RMV (virtualenv for ruby) to negate having to install global gems* [RMV Install](https://rvm.io/rvm/install).   

Install docker-sync:   
`gem docker-sync`

Before starting the container stack, from the root of the repo start docker-sync.  
`docker-sync start`

After sync has initialized and entered the background you can build/start your docker-compose stacks by pointing to the mac specific yaml

IE: `docker-compose -f docker-compose-mac.yml build|up|down|etc`

Just point to the mac specific yaml for all docker-compose commands.   
When done dev'ing you can stop the docker-sync bg proc.   
`docker-sync stop`

*For linux, use the default docker-compose yaml as docker is optimized for EXT\* file systems*

--------------

Build docker-compose containers

`docker-compose build`

Launch the container stack

`docker-compose up`

Swagger UI can be accessed via:  
`http://0.0.0.0/api/swagger-ui`

DynamoDB Admin Interface.  
`http://0.0.0.0:8001`

SQS Browser Interface.  
`http://0.0.0.0:9325`

#### DynamoDB Local
After starting the container stack, run the following command to create the dynamodb tables locally.  
` docker exec -it $(docker container list --format="{{ .Names }}" | grep api) python local_dynamo.py create`


#### UWSGI
The `api` container is running `uwsgi` in forked (4 procs) and hot-reload mode (IE: `uwsgi` will reload when detecting a file has updated on disk). However you may need to kick the process due to a fatal/parsing error.  IE:   
`--- no python application found, check your startup logs for errors ---`   
To do so, enter the `api` container using the following command.  

`docker exec -it $(docker container list --format="{{ .Names }}" | grep api) /bin/bash`.  

Then kill PID 1 to restart the `uwsgi` handler.  

`kill 1`