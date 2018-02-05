[![Build Status](https://travis-ci.org/IBM/PodcastDownloader.svg?branch=master)](https://travis-ci.org/IBM/PodcastDownloader)
![IBM Cloud Deployments](https://metrics-tracker.mybluemix.net/stats/527357940ca5e1027fbf945add3b15c4/badge.svg)

# Create a podcast downloader using OpenWhisk
In this Code Pattern, we will demonstrate the use of OpenWhish by creating a podcast downloader.  A light weight Flask application is set up to request and download the content, which is then retained in OpenStack Swift object storage.

When the reader has completed this Code Pattern, they will understand how to:

* compose a microservices style app
* utilize the power of OpenWhisk
* make use of OpenStack Swift object storage

![Architecture](pics/11111.png)

## Flow
1. A local python app with MySQL backend is set up.
2. User packages Python Actions with a virtual environment in a zip file and uploads to IBM Cloud Functions.
3. User interacts with local app to invoke Action.
4. Data is stored in Object Storage OpenStack Swift.

## Included components
* [IBM Cloud Object Storage](https://console.bluemix.net/catalog/services/object-storage): Build and deliver cost effective apps and services with high reliability and fast speed to market in an unstructured cloud data store.
* [OpenWhisk](https://console.ng.bluemix.net/openwhisk): Execute code on demand in a highly scalable, serverless environment.

## Featured technologies
* [Microservices](https://www.ibm.com/developerworks/community/blogs/5things/entry/5_things_to_know_about_microservices?lang=en): Collection of fine-grained, loosely coupled services using a lightweight protocol to provide building blocks in modern application composition in the cloud.

# Watch the Video
[![](http://img.youtube.com/vi/95hDtAAzNnw/0.jpg)](https://www.youtube.com/watch?v=95hDtAAzNnw)

# Steps

## Run locally

1. [Clone the repo](1#-clone-the-repo)
2. [Create database](#2-create-database)
3. [Server side](#3-server-side)
4. [Create user, podcast, and subscription](#4-create-user-podcast-and-database)
5. [Create a zip python action](#5-create-a-zip-python-action)
6. [Deploy Downloader action to OpenWhisk platform](#6-deploy-downloader-action-to-openwhisk-platform)
7. [Invoke downloader action from podcast manager](#7-invoke-downloader-action-from-podcast-manager)

#### Prerequisite
Make sure you have a [Bluemix](https://console.ng.bluemix.net) account.
It also helpful if you are slightly familiar with basic OpenWhisk commands [Model and idea](https://github.com/IBM/openwhisk-action-trigger-rule) and have installed both the [Bluemix CLI](https://console.bluemix.net/docs/cli/reference/bluemix_cli/download_cli.html) and the Cloud Functions [Plugin](https://console.bluemix.net/openwhisk/learn/cli).

#### Installation requirements:
- Python2.7 Installed.
- pip install -r requirements.txt
- Mysql DB server instance installed locally or provisioned on remote cloud server.
- curl command tool or similar tools available.

### 1. Clone the repo
Clone the PodcastDownloader`locally.  In a terminal, run:
```
$ git clone https://github.com/IBM/PodcastDownloader
$ cd PodcastDownloader
```

### 2. Create database
Provision a mysql dabatase instance, using the provided podcasts_downloader.sql to create the database
tables.
```
$ mysql -u user -p < podcasts_downloader.sql
```

### 3. Server side
Start the podcasts manager api server.
```
$ export FLASK_APP=podcasts_manager.py
$ export FLASK_DEBUG=1
$ flask run
```
### 3. Create user, podcast, and subscription
Use curl to create the users, subscriptions, and podcasts.
For example, suppose your podcast manager api server runs locally and listen on port 5000.
- create a user. `curl -X POST "http://localhost:5000/customer?name=liu"`
- create a podcast. `curl -X POST "http://localhost:5000/podcast?podname=google&url=https://www.ted.com/talks/rss"`
- create a subscription. `curl -X POST "http://localhost:5000/sub?customerid=1&podid=1"`

### 4. create a zip python action.
Make sure you have docker installed locally and you have openwhisk/python2action
docker images already built successfully.
- `cp DownloaderAction.py  __main__.py`

#### Integrate Downloader action with the OpenStack swift client.
In order to persist the downloaded podcast content on storage, we now support integration
with [OpenStack](https://www.openstack.org) swift client, to persist the downloaded content on [IBM Object Storage](https://www.bluemix.com).
First, you need to provision an object storage service, and copy all your storage service
authentication information to VCAP_SERVICES.json, the Downloader Action will read the VCAP_SERVICES.json
file, to pass the storage services authentication.

Make the zip python aciton.
- `docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh
-c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"`

- `zip -r wgetPython.zip virtualenv __main__.py VCAP_SERVICES.json`

### 5. Deploy Downloader action to OpenWhisk platform

`bx wsk action create wgetPython --kind python:2 wgetPython.zip`

### 6. Invoke downloader action from podcast manager
` curl -X POST  -m 50 "http://localhost:5000/download?customername=liu&downloader_url=https://openwhisk.ng.bluemix.net/api/v1/namespaces/<cf_org>_<cf_space>/actions/wgetPython"` 

## Links

* [OpenWhisk](https://openwhisk.apache.org/)
* [OpenStack Swift](https://wiki.openstack.org/wiki/Swift)

## License
[Apache 2.0](LICENSE)
