import requests
from bs4 import BeautifulSoup
import os
import sys

url = "https://wall.alphacoders.com/search.php?search=flower&page={}"
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}

def wallpaper_spider(url):
    # connect to the web & grab the source code
    source_code = requests.get(url, header)
    if source_code.status_code != requests.codes.OK:
        print("request error. code: %d" % source_code.status_code)
        sys.exit()
    plain_text = source_code.text

    # crawler the images href & download them
    soup = BeautifulSoup(plain_text, "html.parser")

    if os.path.exists("./Alphawallpaper/") != True:    # create a file to store images
        os.mkdir("Alphawallpaper/")

    thumbs = soup.find_all('div', class_='thumb-container-big')  # dig the image data from class thumbs firstly
    for thumb in thumbs:
        boxcaption = thumb.find('div', class_='boxcaption')      # dig the boxcaption class
        overlay = boxcaption.find('div', class_='overlay')       # dig the overlay class
        download_url = overlay.find('span', class_='download-button')['data-href']  # find out the image download data

        # example : data-href = https://initiate.alphacoders.com/download/wallpaper/282628/images4/jpg/1703455236">
        id_name = download_url.split("wallpaper/")[1].split("/images")[0] # get the image's id

        print("start download %s" % download_url)   # download the images

        r = requests.get(download_url)              # read the downloaded images
        if r.status_code != requests.codes.OK:
            print("%s Download Failed Error")
            continue

        with open("./Alphawallpaper/%s.jpg" % id_name, "wb") as f:   # open the file and write on the downloaded images
            f.write(r.content)

wallpaper_spider(url.format(1))
