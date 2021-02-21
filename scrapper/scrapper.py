import requests
from bs4 import BeautifulSoup

URL = "https://www.saramin.co.kr/zf_user/search/recruit?searchword=python&recruitPageCount=100"

recruitpage = 1

def scrapper(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r, "html.parser")
    return soup


def get_last_page(URL):  

    global recruitpage
    URL = URL+f"&recruitPage={recruitpage}"

    pagination = scrapper(URL).find("div", {"class":"pagination"})
    anchors = pagination.find_all("a")

    if anchors[-1].text == "다음":
        recruitpage += 10
        get_last_page(URL)
    else:
        global last_page
        last_page = int(pagination.find("span").text)
    return last_page


last_page = get_last_page(URL)

def extract_jobs():
    recruit = scrapper(URL).find_all("div", {"class":"item_recruit"})
    