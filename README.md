[![Build Status](https://travis-ci.org/IBM/PodcastDownloader.svg?branch=master)](https://travis-ci.org/IBM/PodcastDownloader)
![IBM Cloud Deployments](https://metrics-tracker.mybluemix.net/stats/527357940ca5e1027fbf945add3b15c4/badge.svg)

# Create a podcast downloader using OpenWhisk
In this Code Pattern, we will a podcast downloader using Microservices and OpenWhisk. [Explain briefly how things work]. [Give acknowledgements to others if necessary]

When the reader has completed this Code Pattern, they will understand how to:

* compose a microservices style app
* utilize the power of OpenWhisk

![](images/architecture.png)

## Flow
1. Step 1.
2. Step 2.
3. Step 3.
4. Step 4.
5. Step 5.

## Included components
* [OpenWhisk](https://console.ng.bluemix.net/openwhisk): Execute code on demand in a highly scalable, serverless environment.

## Featured technologies
* [Microservices](https://www.ibm.com/developerworks/community/blogs/5things/entry/5_things_to_know_about_microservices?lang=en): Collection of fine-grained, loosely coupled services using a lightweight protocol to provide building blocks in modern application composition in the cloud.

# Watch the Video
[![](http://img.youtube.com/vi/Jxi7U7VOMYg/0.jpg)](https://www.youtube.com/watch?v=Jxi7U7VOMYg)

# Steps
Use the ``Deploy to IBM Cloud`` button **OR** create the services and run locally.

## Run locally

1. [Create database](#1-create-database)
2. [Server side](#2-server-side)
3. [Create a zip python action](#3-create-a-zip-python-action)
4. [Deploy Downloader action to openwhisk platform as a web action](#4-deploy-downloader-action-to-openwhisk-platform-as-a-web-action)
5. [Invoke downloader action from podcast manager](#5-invoke-downloader-action-from-podcast-manager)

#### Prerequisite
Make sure you have a [Bluemix](https://console.ng.bluemix.net) account.
Suppose you're familiar with Basic OpenWhisk programming [Model and idea](https://github.com/IBM/openwhisk-action-trigger-rule)

#### Installation requirements:
- Python2.7 Installed.
- pip install -r requirements.txt
- Mysql DB server instance installed locally or provisioned on remote cloud server.
- curl command tool or similar tools available.

### 1. Create database
Provision a mysql dabatase instance, use the podcasts_downloader.sql to create the database
tables.
Use curl to create the users, subscriptions, and podcasts.
For example, suppose your podcast manager api server runs locally and listen on port 5000.
- create a user. `curl -X POST "http://localhost:5000/customer?name=liu"`
- create a podcast. `curl -X POST "http://localhost:5000/podcast?podname=google&url=https://www.ted.com/talks/rss"`
- create a subscription. `curl -X POST "http://localhost:5000/sub?customerid=2&podid=2"`

### 2. Server side
Start the podcasts manager api server.

- `export FLASK_APP=podcasts_manager.py`
- `export FLASK_DEBUG=1`
- `flask run`

### 3. create a zip python action.
Make sure you have docker installed locally and you have openwhisk/python2action
docker images already built successfully.
- `cp DownloaderAction.py  __main__.py`

#### Integrate Downloader action with the OpenStack swift client.
In order to persist the downloaded podcast content on storage, now we support integrate
with [OpenStack](https://www.openstack.org) swift client, to persist the downloaded content on [IBM object storage](https://www.bluemix.com).
First, you need to provision an object storage service, and copy all your storage service
authentication information to VCAP_SERVICES.json, the Downloader Action will read the VCAP_SERVICES.json
file, to pass the storage services authentication.

Make the zip python aciton.
- `docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh \
-c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"`

- `zip -r wgetPython.zip virtualenv __main__.py VCAP_SERVICES.json`

### 4. Deploy Downloader action to openwhisk platform as a web action

`wsk action create /david.liu@cn.ibm.com_dliu/demo/wgetPython   --kind python:2 --web true wgetPython.zip`

### 5. Invoke downloader action from podcast manager
` curl -X POST  -m 50 "http://localhost:5000/download?customername=liu&downloader_url=https://openwhisk.ng.bluemix.net/api/v1/web/david.liu@cn.ibm.com_dliu/demo/wgetPython"` 

## License
[Apache 2.0](LICENSE)
