import urllib.request
import requests
from bs4 import BeautifulSoup


def scrape_apply_btns(urls):
    results = []
    for starturl in urls:
        if 'indeed' in starturl:
            res = urllib.request.urlopen(starturl)
            final_url = res.geturl()
            response = requests.get(final_url)
        else:
            response = requests.get(start_url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup = BeautifulSoup(r.content, "html.parser")
        a_elements = soup.find_all('a')
        found = False
        apply_url = None
        for a in a_elements:
            if 'apply' in a.text.lower():
                apply_url = a['href']
                found = True
        if not found:
            results.append(starturl)
        else:
            results.append(apply_url)
    else:
        results.append(starturl)

    return results
