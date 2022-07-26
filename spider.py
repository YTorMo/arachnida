import re
from bs4 import *
import requests
import os
from requests.exceptions import ConnectionError
requests.packages.urllib3.disable_warnings() 


def main(url_ln):
    full_list = []
    full_list.append(url_ln)
    full_list = get_full_listurl(full_list, 0)
    print("Enlaces obtenidos:      " + str(len(full_list)))
    full_img_list = get_ful_image_url_list(full_list)
    print("Enlaces de imagenes:     " + str(len(full_img_list)))
    folder_create(full_img_list)


def get_full_listurl(urls, depth):
    full_list = urls
    alrd_vstd = []
    while depth > 0:
        part_list = []
        urls_raw = []
        for url_ln in full_list:
            list_url = []
            if(url_ln.startswith("file")):
                with open(url_ln[7:], "r") as f:
                    page = f.read()
                list_url = page.split("\n")
                for url in list_url:
                    if (url.find('href') != -1 and (url.find('<a') != -1 or url.find('<link') != -1)):
                            url_splt = url.split('"')
                            for url_s in url_splt:
                                if(url_s.startswith(url_ln) or url_s.startswith("//") or url_s.startswith("/")):# or url_s.startswith("https")
                                    part_list.append(url_converter(url_ln, url_s))
            elif(url_ln not in alrd_vstd and url_ln.startswith("https")):
                r = requests.get(url_ln, verify=False)
                soup = BeautifulSoup(r.text, 'html.parser')
                list_url = soup.findAll('link') + soup.findAll('a')#
                for url in list_url:
                    if url.has_key('href'):
                        urls_raw.append(url['href'])
                urls = []
                for url in urls_raw:
                    if(url.startswith(url_ln) or url.startswith("//") or url.startswith("/")): #
                        urls.append(url_converter(url_ln, url))
                for url in urls:
                    if(url not in full_list and url not in part_list):
                        part_list.append(url)
                alrd_vstd.append(url_ln)
        for url in part_list:
            full_list.append(url)
        depth -= 1
    return full_list


def get_ful_image_url_list(full_list):
    part_list = []
    for url_ln in full_list:
        urls_raw = []
        list_url = []
        if(url_ln.startswith("file")):
                with open(url_ln[7:], "r") as f:
                    page = f.read()
                list_url = page.split("\n")
                for url in list_url:
                    if (url.find('src') != -1 or url.find('href') != -1):
                            url_splt = url.split('"')
                            for url_s in url_splt:
                                if(url_s.find("jpg") != -1 or url_s.find("jpeg") != -1 or url_s.find("gif") != -1 or url_s.find("png") != -1):
                                    part_list.append(url_s)
        else:
            r = requests.get(url_ln, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            list_url = soup.findAll('link') + soup.findAll('img')
            for url in list_url:
                if (url.has_key('href')):
                    urls_raw.append(url['href'])
                elif (url.has_key('src')):
                    urls_raw.append(url['src'])
            for url in urls_raw:
                if(url.find("jpg") != -1 or url.find("jpeg") != -1 or url.find("gif") != -1 or url.find("png") != -1):
                    if(url not in part_list):
                        part_list.append(url)
    return part_list


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
            print("Broken link.")
            continue
        with open(folder_name + "/" + filename.group(1), 'wb') as f:
            response = requests.get(url)
            f.write(response.content)


def url_converter(base_url, url):
    if (url.startswith("//")):
        url = "https:" + url
    elif (url.startswith("/")):
        url = base_url + url
    return url


if __name__ == "__main__":
    #input("Enter site URL:")
    url = "file:///System/Volumes/Data/sgoinfre/goinfre/Perso/ytoro-mo/arachnida/ejemplo.html"
    if(url.startswith("http")):
        try:
            requests.get(url)
            main(url)
        except ConnectionError:
            print ('Failed to open url.')
    elif(url.startswith("file")):
        try:
            open(url[7:], "r")
            main(url)
        except:
            print("Failed to open file url.")
    else:
        print("Invalid URL")

#https://stackoverflow.com
#https://www.airbnb.es
#https://www.codespeedy.com
#https://elpais.com
#file:///System/Volumes/Data/sgoinfre/goinfre/Perso/ytoro-mo/arachnida/ejemplo.html