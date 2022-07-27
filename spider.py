import re
from bs4 import *
import requests
import os
import argparse
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError
requests.packages.urllib3.disable_warnings() 


def main(arg):
    rec_lvl = 0
    url_list_f.append(arg.get("URL"))
    if arg.get("r"):
        rec_lvl = 4
        if arg.get("l"):
            rec_lvl = int(arg.get("l")) - 1
    depth = int(rec_lvl)
    while (depth > 0):
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(get_list_url, url_list_f)
        depth -= 1
    print("Visited URLs:      " + str(len(url_list_f)))
    folder_create(arg)
    print(url_list_f)
    with ThreadPoolExecutor(max_workers=100) as executor:
    	executor.map(test_img_url, url_list_f)


def parse():
	parser = argparse.ArgumentParser(
		prog = "python3 spider.py", 
		description = "The spider program will allow you to extract all the images from a website"
	)
	parser.add_argument("-r", action="store_true", help="Option -r : recursively downloads the images in a URL received as a parameter", default = False)
	parser.add_argument("-l", help ="Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.", default = 0)
	parser.add_argument("-p", help="Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.", default="./data")
	parser.add_argument("URL", help="URL from a website")
	args = parser.parse_args()
	return args.__dict__


def get_list_url(url_ln):
        list_url = []
        if(url_list_f[0].startswith("file:///")):
            if(url_ln.startswith("file:///")):
                with open(url_ln[7:], "r") as f:
                    page = f.read()
                list_url = page.split("\n")
                for url in list_url:
                    if (url.find('href') != -1 and (url.find('<a') != -1 or url.find('<link') != -1)):
                            url_splt = url.split('"')
                            for url_s in url_splt:
                                if(url_s.startswith(url_base) or url_s.startswith("//") or url_s.startswith("/") or url_s.startswith("https")):
                                    url_list_f.append(url_converter(url_ln, url_s))
            else:
                web_requester(url_ln)
        else:
            web_requester(url_ln)

def web_requester(url_ln):
    urls_raw = []
    list_url = []
    r = requests.get(url_ln, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    list_url = soup.findAll('link') + soup.findAll('a')#
    for url in list_url:
        if url.has_key('href'):
            urls_raw.append(url['href'])
    urls = []
    for url in urls_raw:
        if(url.startswith(url_base) or url.startswith("//") or url.startswith("/")): #
            urls.append(url_converter(url_base, url))
    for url in urls:
        if(url not in url_list_f):
            url_list_f.append(url)


def test_img_url(url_ln):
    urls_raw = []
    list_url = []
    part_list = []
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
    download_images(part_list, arg.get("p"))

def folder_create(arg):
    folder_name = arg.get("p")
    os.mkdir(folder_name)


def download_images(urls, folder_name):
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg|gif|png))', url)
        if not filename:
            print("Broken link. ")
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
    arg = parse()
    url_base = arg.get("URL")
    url_list_f = []
    if(url_base.startswith("http")):
        try:
            requests.get(url_base)
            main(arg)
            print("Download finish. \n" + str(len(os.listdir(arg.get("p")))) + " images has been downloaded.")
        except ConnectionError:
            print ('Failed to open url.')
    elif(url_base.startswith("file")):
        try:
            open(url_base[7:], "r")
            main(arg)
        except:
            print("Failed to open file url.")
    else:
        print("Invalid URL")

#https://stackoverflow.com
#https://www.airbnb.es
#https://www.codespeedy.com
#https://elpais.com
#file:///System/Volumes/Data/sgoinfre/goinfre/Perso/ytoro-mo/arachnida/ejemplo.html
#https://www.billerickson.net/how-long-does-it-take-to-build-a-website/