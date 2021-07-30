#!/bin/bash

docker build . -t api-deployment
heroku container:login
heroku container:push web --app arnaud-durieux-api-deployment
heroku container:release web --app arnaud-durieux-api-deployment

