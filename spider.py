import re
from bs4 import *
import requests
import os
requests.packages.urllib3.disable_warnings() 


def main(url_ln):
    full_list = []
    full_list.append(url_ln)
    full_list = get_full_listurl(full_list, 2)
    print(len(full_list))
    full_img_list = get_ful_image_url_list(full_list)
    print(len(full_img_list))
    folder_create(full_img_list)


def get_full_listurl(urls, depth):
    full_list = urls
    alrd_vstd = []
    while depth > 0:
        part_list = []
        for url_ln in full_list:
            if(url_ln not in alrd_vstd):
                r = requests.get(url_ln, verify=False)
                soup = BeautifulSoup(r.text, 'html.parser')
                list_url = []
                list_url = soup.findAll('a')#soup.findAll('link') +
                urls_raw = []
                for url in list_url:
                    if url.has_key('href'):
                        urls_raw.append(url['href'])
                urls = []
                for url in urls_raw:
                    if(url.startswith("https://") or url.startswith("//") or url.startswith("/")): #
                        urls.append(url_converter(url_ln, url))
                for url in urls:
                    if(url not in full_list and url not in part_list):
                        part_list.append(url)
                        #print(url + "\n")
                alrd_vstd.append(url_ln)
        for url in part_list:
            full_list.append(url)
        depth -= 1
    return full_list


def get_ful_image_url_list(full_list):
    part_list = []
    for url_ln in full_list:
        r = requests.get(url_ln, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        list_url = []
        list_url = soup.findAll('link') + soup.findAll('img')
        urls_raw = []
        for url in list_url:
            if (url.has_key('href')):
                urls_raw.append(url['href'])
            elif (url.has_key('src')):
                urls_raw.append(url['src'])
        urls = []
        for url in urls:
            part_list.append(url)
            #print(url + "\n")
    for url in part_list:
        full_list.append(url)
    return full_list


def folder_create(urls):
    folder_name = input("Enter name of folder: ")
    if(not folder_name):
        folder_name = "data"
    os.mkdir(folder_name)
    download_images(urls, folder_name)


def download_images(urls, folder_name):#, site
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg|gif|png))', url)
        if not filename:
            #print("Regular expression didn't match with the url: {}".format(url))
            continue
        with open(folder_name + "/" + filename.group(1), 'wb') as f:
            #if 'http' not in url:
            #    url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)


def url_converter(base_url, url):
    if (url.startswith("//")):
        url = "https:" + url
    elif (url.startswith("/")):
        url = base_url + url
    return url


if __name__ == "__main__":
    url = "https://www.codespeedy.com" 
    #input("Enter site URL:")
    main(url)


#https://stackoverflow.com
#https://www.airbnb.es
#https://www.codespeedy.com
#https://elpais.com/