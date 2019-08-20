import requests
import sys
import argparse
import pathlib

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from functions import functions

hosts = {
    'all': 0,
    'clipwatching': 49,
    'gounlimited': 51,
    'openload': 1,
    'streamango': 37,
    'streamcherry': 39,
    'verystream': 55,
    'vidoza': 41,
}

versions = {
    'all': 0,
    'dub': 6,
    'org': 1,
    'sub': 3,
}


def command_line_operations():
    parser = argparse.ArgumentParser(description='Movie downloader')

    parser.add_argument('-v', '--version', type=str, nargs=1, action="store",
                        help='Version of movie ({})'.format(', '.join(versions)), default=['all'])

    parser.add_argument('-s', '--source', type=str, nargs=1, action="store",
                        help='Source of movie ({})'.format(', '.join(hosts)), default=['all'])

    parser.add_argument('-t', '--title', type=str, nargs='+', action="store",
                        help='Title of movie', required=True)

    parser.add_argument('-d', '--download', help='If -d the file will be downloaded',
                        required=False, action='store_true')

    args = parser.parse_args()

    version = args.version[0]
    source = args.source[0]
    download = args.download
    title = ' '.join(args.title)

    assert version in versions
    assert source in hosts

    return version, source, title, download


def get_movies_list(name, host, version):

    if host == 'all':
        host = list(hosts.keys())[1:]
    else:
        host = [host]

    if version == 'all':
        version = list(versions.keys())[1:]
    else:
        version = [version]

    number_zero = []
    for h in host:
        for v in version:
            query = 'http://szukajka.tv/?q={}&s={}&h={}&v={}&a={}'.format(
                name.lower().replace(' ', '%20'),
                5,
                hosts[h],
                versions[v],
                '#')

            res = requests.get(query)
            soup = bs(res.content, 'html.parser')
            number_zero += soup.findAll('a', ['link'], href=True)

    return number_zero


def get_movie_url(query, host):
    options = Options()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get('http://szukajka.tv/')
    driver.add_cookie({'name': 'rodo', 'value': 'accepted'})
    driver.get(query)
    soup = bs(driver.page_source, 'html.parser')

    query = soup.find('iframe')['src']
    driver.get(query)

    query = None
    if host in functions:
        query = functions[host](driver)

    driver.quit()
    return query


def download(query, file_name):
    pathlib.Path('download/').mkdir(parents=True, exist_ok=True) 
    
    file_name = file_name.replace(' ', '_')+'.mp4'
    with open('download/'+file_name, "wb") as f:
        response = requests.get(query, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            print('Progressbar is not available')
            f.write(response.content)
        else:
            for data in tqdm(response.iter_content(chunk_size=4096), desc=file_name, total=int(total_length)//4096+1):
                f.write(data)


def get_source_url(link):
    query = 'http://szukajka.tv/link/{}'.format(
        link['href'].split('/')[-1].split('-')[0])
    return query


def main():
    version, host, name, down = command_line_operations()
    print('>> Search: {} in {}'.format(name, host))
    movies = get_movies_list(name, host, version)
    print('>> Found {} movies'.format(len(movies)))
    for i, link in enumerate(movies):
        try:
            print('>> Try {}/{}'.format(i+1, len(movies)))
            movie = get_source_url(link)
            url = get_movie_url(movie, host)
        except Exception as e:
            continue

        print('>> File: {}'.format(url))
        if down:
            download(url, name)
        return

if __name__ == "__main__":
    main()
