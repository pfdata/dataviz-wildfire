#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv


# In[12]:


class Crawler():
    def __init__(self, _url):
        self.url = _url
        self.url_list = get_url_list()
        self.data = get_data(url_list)
        
    def get_url_list():
        url_list = []
        
        for x in range (1,13):
            if x < 10:
                url_list.append("https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/air_temperature_mean/regional_averages_tm_" + "0" + str(x) + ".txt")
            else:
                url_list.append("https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/air_temperature_mean/regional_averages_tm_" + str(x) + ".txt")
                
        return url_list
    
    def get_data(url_list):
        Data = []
        for url in url_list:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            Data.append(text)
        return Data


# In[13]:


def csvwriter(Data):

    with open('crawler_output.csv', 'w', newline='') as csvfile:
        articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        articlewriter.writerow(Data)


# In[14]:


datareturn()
parser()
csvwriter(Data)


# In[ ]:




