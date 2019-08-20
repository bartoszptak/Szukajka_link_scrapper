import re
from bs4 import BeautifulSoup as bs

def get_clipwatching(driver):
    driver.find_element_by_tag_name('body').click()
    soup = bs(driver.page_source, 'html.parser')

    return soup.video['src']

def get_gounlimited(driver):
    page = driver.page_source
    params = re.findall(r'h\|mp4|\|\w+\|fs\w+\|', page)[0].split('|')

    query = 'https://{}.gounlimited.to/{}/v.mp4'.format(*params[-2:0:-1])
    return query


def get_openload(driver):
    driver.find_element_by_tag_name('body').click()
    soup = bs(driver.page_source, 'html.parser')

    params = soup.video['src'].split('?')[0]
    return 'https://openload.co{}'.format(params)


def get_streamango(driver):
    driver.find_element_by_tag_name('body').click()
    soup = bs(driver.page_source, 'html.parser')

    params = soup.video['src']
    return 'https:{}'.format(params)


def get_streamcherry(driver):
    driver.find_element_by_tag_name('body').click()
    soup = bs(driver.page_source, 'html.parser')

    params = soup.video['src']
    return 'https:{}'.format(params)


def get_verystream(driver):
    driver.find_element_by_tag_name('body').click()
    soup = bs(driver.page_source, 'html.parser')

    params = soup.video['src']
    return 'https://verystream.com{}'.format(params)


def get_vidoza(driver):
    page = driver.page_source
    return re.findall(r'https:\/\/\w+\.vidoza\.\w+\/\w+\/v.mp4', page)[0]


functions = {
    'clipwatching': get_clipwatching,
    'gounlimited': get_gounlimited,
    'openload': get_openload,
    'streamango': get_streamango,
    'streamcherry': get_streamcherry,
    'verystream': get_verystream,
    'vidoza': get_vidoza,
}
