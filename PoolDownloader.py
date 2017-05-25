import wget
import requests
from pyPodcastParser.Podcast import Podcast
from multiprocessing import Pool

def download(url):
    wget.download(url)

def parse(podcast_url):
    response = requests.get(podcast_url)
    podcast = Podcast(response.content)
    urls_to_download = []
    for item in podcast.items:
        urls_to_download.append(item)
    return urls_to_download

if __name__ == '__main__':
    try:
        pool = Pool()
        pool.map(download,parse('urls'))
        pool.join()
    except Exception:
        pass
    finally:
        pool.close()


