import re
import json
import requests
from bs4 import BeautifulSoup as bs

with open("supported_sites.json", "r") as file:
    websites = json.load(file)

# IMAGE PARSER FOR HTTPS://READCOMIC.NET/
def get_img_src_one(url, amount):
    # if number of /s is less than 5 then add a /full at the end of the url
    # this will allow us to get every image in one fell swoop
    if url.count("/") < 5:
        url += "/full"
    all_imgs = []
    try:
        while amount > 0:
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            print(f"Current url processing: {url}")
            img_tags = soup.find_all("img", class_="lazyload chapter_img")
            imgs = [img.get("data-original") for img in img_tags]
            all_imgs.append(imgs)
            amount -= 1

            url = soup.find("a", class_="nav next").get("href")
            # print(url)
        return all_imgs
    except Exception as e:
        print(f"An error has occurred: {e}")
        print(f"Something went wrong with processing url: {url}")
        return []

# Determine if url is valid and select correct funtion depending on website
def get_img_urls(url, amount):
    valid_website = False
    for website in websites:
        if website in url:
            valid_website = True
            break
    if not valid_website:
        print("Incorrect URL based on supported websites")
        return
    
    # url followed by dedicated function name to call
    parser = {
        r"https://readcomic.net/": get_img_src_one
    }

    for pattern, func in parser.items():
        if re.match(pattern, url):
            return func(url, amount)