#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import pandas as pd
import csv
import datetime
import os
import sys


# In[2]:


"""

There are two parameters to set;
category: (str), options: "all", "hospital compare", "Nursing home compare", ... 
(please find category on the website: https://data.medicare.gov/)
search_key_word: the keyword you want to refine, if none, input "".
"""
# category = "hospital compare"  ###set example; if no specific category, set it "all"
# search_key_word = "MRI" ###if none, input ''
 
category = sys.argv[1]  ###set example; if no specific category, set it "all"
search_key_word = sys.argv[2] ###if none, input ''

#get time for this search
currentDT = datetime.datetime.now()
YMD = "{}{}{}".format(currentDT.year,currentDT.month,currentDT.day)
HMS = "{}{}{}".format(currentDT.hour, currentDT.minute, currentDT.second)


# Please do not change the code below!

# In[3]:


"""

the folder will be created under your current way 
with the name of category, keyword and time(year,month,day)
all data will be saved in that folder
"""
category_folder= category.replace(" ","+")
search_key_word_folder = search_key_word.replace(" ","+")
save_folder = "./{}_{}_{}/".format(category, search_key_word, YMD)
os.mkdir(save_folder)


# In[4]:


if category == "all":
    base_url = "https://data.medicare.gov/browse/embed?q=&sortBy=relevance"
else:
    category_embed = category.replace(" ","+")
    search_key_word_embed = search_key_word.replace(" ","+")
    base_url = "https://data.medicare.gov/browse/embed?category={}&q={}&sortBy=relevance".format(category_embed,search_key_word_embed)
print("base_url: ",base_url)
page = urlopen(base_url)
soup = BS(page)


# In[5]:


all_links = soup.find_all('a',class_="browse2-result-name-link")


# In[6]:


titles = []
links = []
for i in all_links:
    only_title = i.text.strip()
    titles.append(only_title)
    print("title:",only_title)
    link = i.get('href')
    csv_link = "https://data.medicare.gov/resource/" + link.split('/')[-1] + ".csv"
    print("link:",csv_link)
    links.append(csv_link)
    data = pd.read_csv(csv_link)
    data.to_csv(save_folder + "{}.csv".format(only_title))
    


# In[7]:


info_df = pd.DataFrame({"title":titles,"link":links})
info_df.to_csv(save_folder + "info.csv")


# Complete
