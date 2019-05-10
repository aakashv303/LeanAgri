import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
import re
from pandas import DataFrame

urlmain = "http://www.agriculture.gov.au/"
urlImg = "http://www.agriculture.gov.au"
url = "http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases"
export_path = r'C:\Users\Aakash Vaghela\Desktop\LeanAgri_Task\LeanAgri\data.xlsx'

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page,'html.parser')
li_tags=soup.find('ul',class_="flex-container")

originList = []
diseaseList = []
imgList = []
exoticList = []
pestList = []
titleList = []

for img in li_tags.find_all("img"):
    imageName = img.get("src").rsplit('/', 1)[-1]
    imgList.append(urlImg+img.get("src")) # Get Image Link
    urllib.request.urlretrieve(urlImg+img.get("src"), imageName) #Download Image

for a in li_tags.find_all("a"):
    diseaseList.append(a.text) # Disease Name
    appendurl = a.get("href")
    if not appendurl.startswith("http"):
        redirecturl = urlmain + appendurl
        nextpage = urllib.request.urlopen(redirecturl)
        soup2 = BeautifulSoup(nextpage,'html.parser')
        div_tags=soup2.find('div',class_="pest-header-content")
        try:
            p = div_tags.find_all("p")[0:1]
        except Exception as e:
            pass
        for x1 in p:
            try:
                e = x1.text
                e = e.replace('\n', '')
                if "Australia" in e:
                    exoticList.append(e) #Exotics
                else:
                    pass
            except:
                pass
        paragraphs = []
        try:
            p = div_tags.find_all("p")[-1]
        except Exception as e:
            pass
        for x in p:
            paragraphs.append(str(x))
        origin = paragraphs[paragraphs.index('<strong>Origin: </strong>')+1]
        originList.append(origin) # Origin List
        pestList.append("NA")
    else:
        try:
            nextpage = urllib.request.urlopen(appendurl)
            soup3 = BeautifulSoup(nextpage,'html.parser')
        except:
            pass
        h1_tags=soup3.find('h1',class_="page_title")
        for title in h1_tags:
            titleList.append(title)
            originList.append("NA")
            exoticList.append("NA")
        div_tag=soup3.find('div',class_="content") 
        pests = []
        try:
            p2 = div_tag.find_all("p")[2:3]
        except Exception as e:
            pass
        for x in p2:
            text = str(x)
            if '<strong>High priority pest of:</strong>' in text:
                m = re.search('<strong>High priority pest of:</strong>(.+?)</p>', text)
                found = m.group(1)
                pestList.append(found) #Pest List
            else:
                pestList.append("NA")
for i in range(5):
    exoticList.append("NA")
pestList.append("NA")

dict = {
    'Disease name':diseaseList,
    'Image link':imgList,
    'Origin':originList,
    'Pest':pestList,
    'Exotic':exoticList  
}

df = DataFrame(dict, columns= ['Disease name', 'Image link', 'Origin', 'Pest', 'Exotic'])

export_excel = df.to_excel (export_path, index = None, header=True) #Export data into excel


    

