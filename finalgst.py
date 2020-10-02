from urllib.request import urlopen
import re, csv
from bs4 import BeautifulSoup
import urllib, requests, json



def scrap():
    name = str(input('Enter Your Name : '))
    html = urlopen('https://cloud.octa.in/gstin?q=' + name)
    soup = BeautifulSoup(html.read())
    page = soup.find('p').getText()
    pages = re.findall("of\s\d\d?\d?", page)
    pagestr = ''.join(pages)
    pageno = pagestr[3:7]
    print(pageno)
    final_num = int(pageno) + 1

    for x in range(1, int(final_num)):
        # print('https://cloud.octa.in/gstin?q='+name+'&adv=False&p='+str(x))
        html1 = urlopen('https://cloud.octa.in/gstin?q=' + name + '&adv=False&p=' + str(x))
        soup1 = BeautifulSoup(html1.read())
        links = []
        for link in soup1.find_all('a'):
            links.append(link.get('href'))

        finalString = ''.join(links)
        gst = re.findall("\d\d\w\w\w\w\w\d\d\d\d\w\d\w\w?", finalString)
        for w in gst:
            gsst(w)


def gsst(w):
    header = {
        'Host': 'app.sahigst.com',
        'Connection': 'keep-alive',
        'Content-Length': '21',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRFToken': 'Pb7sHq1bP8Q4UrEqP0E44ooeTWOLVxVG',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://app.sahigst.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.sahigst.com/search-taxpayer',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    cookie = {
        'sstoken': 'Pb7sHq1bP8Q4UrEqP0E44ooeTWOLVxVG',
    }

    data = "gstin=" + w

    response = requests.post('https://app.sahigst.com/ajax/do_search_single_gstin', headers=header, cookies=cookie,
                             data=data, verify=False)
    data = response.content
    obj = json.loads(data)
    suss = (obj['success'])
    if suss == True:
        gstin = (obj['data']['api_property']['gstin'])
        sts = (obj['data']['api_property']['sts'])
        legal_name = (obj['data']['legal_name'])
        if  sts =='Active' :
            
            try:
                space = re.findall("\s",legal_name)
                if space[0] == " ":
                    ctb = (obj['data']['api_property']['ctb'])
                    if ctb =='Proprietorship' :
                        legal_name = (obj['data']['legal_name'])
                        gstin = (obj['data']['api_property']['gstin'])
                        
                        with open('gst.csv', 'a+', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([gstin,legal_name])
            except :print(gstin)
            
               
if __name__ == "__main__":
    
    scrap()