import requests
from bs4 import BeautifulSoup

recruitpage = 1
URL = f"https://www.saramin.co.kr/zf_user/search/recruit?searchword=python&recruitPageCount=100"

def scrapper(URL):
    r = requests.get(URL).text
    soup = BeautifulSoup(r, "html.parser")
    return soup

def get_last_page(URL):

    global recruitpage
    URL = URL + f"&recruitPage={recruitpage}"
    pagination = scrapper(URL).find("div", {"class":"pagination"})
    anchors = pagination.find_all("a")

    if anchors[-1].text == "다음":
        recruitpage += 10
        get_last_page(URL)
    else:
        global last_page
        last_page = int(pagination.find("span").text)
    return last_page


def extract_jobs(recruit):
    title = recruit.find("h2").text.strip()
    company  = recruit.find("div", {"class":"area_corp"}).find("a").text
    location = recruit.find("div", {"class":"job_condition"}).find("span").text
    link = recruit["value"]

    LINK_URL = f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={link}&recommend_ids=eJxdkMkRQyEMQ6vJ3atsn1MI%2FXcRfhIMw403EkJICyJUGA5%2BxVsL7B48QPJFd5nHEYYLh%2F3sipB5u3Bh68ozzssvXDrByLfe%2BNethD0GVr5Ise86SarUCLGnWYdNM%2FE2B4OtqxoHvPa%2FKelQNSI5ewYzaHojlDP0fCjzGCmVK45NFn4AS5hQFw%3D%3D&view_type=search&searchword=python&searchType=search&gz=1&t_ref_content=generic&t_ref=search&paid_fl=n#seq=0"
    
    return {"title" : title, "company" : company, "location" : location, "link" : LINK_URL}
    
def enter_page(last_page):
    jobs = []
    for page in range(last_page):
        recruits = scrapper(URL+f"&recruitPage={page+1}").find_all("div", {"class":"item_recruit"})
        for recruit in recruits:
            infos = extract_jobs(recruit)
            jobs.append(infos)
    return jobs

def start_scrapper():
    last_page = get_last_page(URL)
    jobs = enter_page(last_page)
    return jobs
