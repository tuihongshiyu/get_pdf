import requests
import re
from bs4 import BeautifulSoup

def get_urls(url):
    page = requests.get(url)
    soup = str(BeautifulSoup(page.text, 'lxml'))
    # print(soup)
    pat = re.compile(r'(?<=href=\")(.+?)\.pdf')  # 匹配地址
    pdf_url = pat.findall(soup)
    return pdf_url

def download_pdf(urls):
    for url in urls:
        # print(url)
        name = re.split(r'\/',url)[-1]
        print(name)
        pdf = requests.get(url,stream=True)
        print(pdf.content)
        with open(str(name), 'wb') as f:
            for chunk in pdf.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()


def download_pdf_ti(urls,names):
    # print(urls,names)
    for i in range(len(urls)):
        name=names[i]
        number = re.split(r'\/',urls[i])[-1]
        url='http://www.ti.com.cn/general/cn/docs/lit/getliterature.tsp?baseLiteratureNumber='+number+'&fileType=pdf'
        page = requests.get(url, stream=True)
        soup = str(BeautifulSoup(page.text, 'lxml'))
        url=re.search(pattern=r'(?<=URL=)(.+?).pdf',string=soup)
        pdf = requests.get(url.group(0), stream=True)
        with open(str(name)+'.pdf', 'wb') as f:
            for chunk in pdf.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()

def get_urls_ti(url):
    page = requests.get(url)
    soup = str(BeautifulSoup(page.text, 'lxml'))
    # print(soup)
    pat = re.compile(r'(?<=href=\")(.+?)\"(.+?)> (.+?)</a>')  # 匹配地址
    list = pat.findall(soup)
    # print(list)
    pdf_url=[]
    pdf_name=[]
    for i in list:

        if '/pdf/' in i[0] :
            # print(i)
            pdf_url.append(i[0])
            pdf_name.append(i[-1])
    # print(pdf_url,pdf_name)
    return pdf_url,pdf_name

# get_urls_ti('http://www.ti.com.cn/product/cn/TM4C1294NCPDT/technicaldocuments')
# download_pdf(['http://www.ti.com.cn/general/cn/docs/lit/getliterature.tsp?baseLiteratureNumber=spmu298&fileType=pdf'])
# pdf_url,pdf_name=get_urls_ti('http://www.ti.com.cn/product/cn/TM4C1294NCPDT/technicaldocuments')
# download_pdf_ti(pdf_url,pdf_name)

def get_pdf(url,site):
    if site=='ti' :
        pdf_url, pdf_name = get_urls_ti(url)
        download_pdf_ti(pdf_url, pdf_name)
    else:
        download_pdf(get_urls())

# get_pdf(url='http://www.ti.com.cn/product/cn/TM4C1294NCPDT/technicaldocuments',site='ti')