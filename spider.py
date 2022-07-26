import re
from bs4 import *
import requests
import os
import argparse
from requests.exceptions import ConnectionError
requests.packages.urllib3.disable_warnings() 


def main(arg):
    full_list = []
    rec_lvl = 0
    full_list.append(arg.get("URL"))
    if arg.get("r"):
        rec_lvl = 5
        if arg.get("l"):
            rec_lvl = arg.get("l")
    full_list = get_full_listurl(full_list, int(rec_lvl))
    print("URLs:      " + str(len(full_list)))
    full_img_list = get_ful_image_url_list(full_list)
    folder_create(full_img_list, arg)


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


def folder_create(urls, arg):
    folder_name = arg.get("p")
    os.mkdir(folder_name)
    download_images(urls, folder_name)


def download_images(urls, folder_name):
    count = 0
    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|jpeg|gif|png))', url)
        if not filename:
            print("Broken link.")
            continue
        with open(folder_name + "/" + filename.group(1), 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
            count += 1
    print("Download finish. \n" + str(count) + " images has been downloaded.")


def url_converter(base_url, url):
    if (url.startswith("//")):
        url = "https:" + url
    elif (url.startswith("/")):
        url = base_url + url
    return url


if __name__ == "__main__":
    arg = parse()
    url = arg.get("URL")
    if(url.startswith("http")):
        try:
            requests.get(url)
            main(arg)
        except ConnectionError:
            print ('Failed to open url.')
    elif(url.startswith("file")):
        try:
            open(url[7:], "r")
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