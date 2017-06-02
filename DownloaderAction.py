import json
import urlparse
import swiftclient.client as swiftclient
import requests


def main(args):
    url_to_download = args.get("url", "")
    msg = {"url":url_to_download}
    result = json.dumps(msg)
    response = requests.get(url_to_download)
    filename = str(url_to_download).rsplit('/')[-1]
    swift('podcast_container', filename, response.content)
    return {"body": result}

def swift(container_name, file_name, file_content):
    with open("VCAP_SERVICES.json") as data:
        content = json.load(data)
        cloudant_service = content['Object-Storage'][0]
        objectstorage_creds = cloudant_service['credentials']

        if objectstorage_creds:
            auth_url = objectstorage_creds['auth_url'] + '/v3'
            project_name = objectstorage_creds['project']
            password = objectstorage_creds['password']
            user_domain_name = objectstorage_creds['domainName']
            project_id = objectstorage_creds['projectId']
            user_id = objectstorage_creds['userId']
            region_name = objectstorage_creds['region']

        # Get a Swift client connection object
        conn = swiftclient.Connection(key=password,
                                      authurl=auth_url,
                                      auth_version='3',
                                      os_options={"project_id": project_id,
                                                  "user_id": user_id,
                                                  "region_name": region_name})

        hascontainername = False
        # List your containers
        for container in conn.get_account()[1]:
            print container['name']
            if container['name'] == container_name:
                hascontainername = True
                print "\n Container name %s already existed." % container_name

        if not hascontainername:
            conn.put_container(container_name)
            print "\nContainer %s created successfully." % container_name

        # Create a file for uploading
        conn.put_object(container_name, file_name, file_content, len(file_content))

