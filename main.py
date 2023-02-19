import json
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

special_headers = {

}
search_parameters = {}
found_pages = []


def find_search_parameters(url):
    print(url)
    soup = BeautifulSoup(requests.Session().get(
        url, headers=req_headers).content, 'lxml')
    pattern = re.compile(r'usersSearchTerm')
    json_script = soup.find('script', text=pattern).text.strip()[4:-3]
    json_data = json.loads(json_script)
    search_parameters = json_data
    print('Finished')


def find_pages(search_url):
    soup = BeautifulSoup(requests.Session().get(
        search_url, headers=req_headers).content, 'lxml')
    for pages in soup.find_all('li', class_='PaginationNumberItem-c11n-8-37-0__bnmlxt-0 ekGcXR'):
        next_page = pages.find('a')['href']
        new_url = f'https://www.zillow.com{next_page}'
        found_pages.append(new_url)


def load_page_data():
    for x in found_pages:
        soup = BeautifulSoup(requests.Session().get(
            x, headers=req_headers).content, 'lxml')
        # Regular Expression Search For json search script
        pattern = re.compile(r'usersSearchTerm')
        # Clean up script to output pure json
        json_script = soup.find('script', text=pattern).text.strip()[4:-3]
        # load json to dataframe
        z = json.loads(json_script)
        # df2 = pd.DataFrame(z['cat1']['searchResults']['listResults'])
        print(soup.title)


def load_data(url):
    soup = BeautifulSoup(requests.Session().get(
        search_url, headers=req_headers).content, 'lxml')
    pattern = re.compile(r'usersSearchTerm')
    json_script = soup.find('script', text=pattern).text.strip()[4:-3]
    json_data = json.loads(json_script)['queryState']
    search_parameters = json.dumps(json_data)

    with requests.Session() as req:
        params = {
            # "searchQueryState": '{usersSearchTerm":"Providence, RCoI","mapBounds":{"west":-71.472667,"east":-71.376432,"south":41.772414,"north":41.861571},"regionSelection":[{"regionId":26637,"regionType":6}],"isMapVisible":true,"filterState":{"isAllHomes":{"value":true},"sortSelection":{"value":"globalrelevanceex"}},"isListVisible":true,"mapZoom":9}',
            "searchQueryState": f'{search_parameters}',
            "wants": '{"cat1":["mapResults"]}'
        }
        r = req.get(url, params=params, headers=headers)
        print(r.url)
        # URL not blocked
        df = pd.DataFrame(r.json()['cat1']['searchResults']['mapResults'])
        # Because we get blocked sometimes
        # df = pd.DataFrame(pd.read_json('homes.json')['cat1']['searchResults']['mapResults'])
        print('Cleaning Data')
        return df


if __name__ == '__main__':
    search = input('Search Zillow : ')
    search_url = 'https://www.zillow.com/' + 'homes/' + search + '_rb/'
    data = load_data('https://www.zillow.com/search/GetSearchPageState.htm')
    data.to_csv(f'{search}.csv')
    print(f'output {search}.csv')
