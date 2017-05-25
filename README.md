# Disclaimer
This is just a sample program to help demo a small distributed app, which
also utilized [OpenWhisk](https://openwhisk.org) platform. Just for training and demo purpose.

# Purpose of the project
To demo how to compose a microservices style app, and utilize the power of [IBM/Openwhisk](https://openwhisk.org)
platform.

# Prerequisite
Make sure you have a [Bluemix](https://console.ng.bluemix.net) account.
Suppose you're familiar with Basic OpenWhisk programming [Model and idea](https://github.com/IBM/openwhisk-action-trigger-rule)

## Installation requirements:
- Python2.7 Installed.
- pip install -r requirements.txt
- Mysql DB server instance installed locally or provisioned on remote cloud server.
- curl command tool or similar tools available.

# How it works
![Architecture](pics/11111.png)

# How to use it
Below section explained how to run the apps.

## Create database
Provision a mysql dabatase instance, use the podcasts_downloader.sql to create the database
tables.
Use curl to create the users, subscriptions, and podcasts.
For example, suppose your podcast manager api server runs locally and listen on port 5000.
- create a user. `curl -X POST "http://localhost:5000/customer?name=liu"`
- create a podcast. `curl -X POST "http://localhost:5000/podcast?podname=google&url=https://www.ted.com/talks/rss"`
- create a subscription. `curl -X POST "http://localhost:5000/sub?customerid=2&podid=2"`
## Server side
Start the podcasts manager api server.

- `export FLASK_APP=podcasts_manager.py`
- `export FLASK_DEBUG=1`
- `flask run`

## create a zip python action.
Make sure you have docker installed locally and you have openwhisk/python2action
docker images already built successfully.
- `cp DownloaderAction.py  __main__.py`

Make the zip python aciton.
- `docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh \
-c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"`

- `zip -r wgetPython.zip virtualenv __main__.py`
## Deploy Downloader action to openwhisk platform as a web action

`wsk action create /david.liu@cn.ibm.com_dliu/demo/wgetPython   --kind python:2 --web true wgetPython.zip`

## Invoke downloader action from podcast manager.
` curl -X POST  -m 50 "http://localhost:5000/download?customername=liu&downloader_url=https://openwhisk.ng.bluemix.net/api/v1/web/david.liu@cn.ibm.com_dliu/demo/wgetPython"` 

## Future enhancements
- Split the manager to different actions or APIs.
- Use sqlarchimy instead of plain sql scripts which is error-prone.
- Investigate how to persist the downloads/contents in the downloader, such as object storage, Nosql DB as attachments etc.
- Message Hub for distributed components communication.
- Scheduler action for periodic automatic subscription downloading etc.
- Web Page UI.
- ...

## License
Apache 2.0

## Thanks
Thanks to [IBM/OpenWhisk](https://openwhisk.org) team for providing such a wonderful product and Powerful Serverless platform.
