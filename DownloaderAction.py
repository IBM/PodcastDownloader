import wget
import json

def main(args):
    url_to_download = args.get("url","")
    print(url_to_download)
    download(url_to_download)
    msg = {"url":url_to_download}
    result = json.dumps(msg)
    return {"body": result}

def download(url):
    wget.download(url)