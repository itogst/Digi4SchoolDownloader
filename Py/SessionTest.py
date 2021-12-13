import os
import shutil
import sys
from html.parser import HTMLParser

import requests

# Global variables
from Py.requester import Digi4SchoolCommunicator
from Py.all_svg2pdf import *

# URL to download
bookUrl = 'https://a.digi4school.at/ebook/5134/'
urlParts = bookUrl.split("/")

# Paths from URL
bookPath = "./" + urlParts[urlParts.__len__() - 2] + "/" + urlParts[urlParts.__len__() - 1]
# png = urlParts[urlParts.__len__()-1]

# Start the session
if os.path.exists(bookPath) and os.path.isdir(bookPath):
    shutil.rmtree(bookPath)

for page in range(1, 404):

    print(page)
    pagePath = bookPath + str(page)
    pageUrl = bookUrl + str(page)
    imagePath = pagePath + "/img/"
    svgUrl = pageUrl + "/" + str(page) + ".svg"
    svgPath = pagePath + "/" + str(page) + ".svg"

    for image in range(1, 64):
        png = str(image) + ".png"
        imageUrl = pageUrl + "/img/" + png

        answer = Digi4SchoolCommunicator.get_file(imageUrl)

        if answer == "404" or answer.text.__contains__("Fehler"):
            break
        print("\t" + png + " 200 OK")
        os.makedirs(imagePath, 0o777, True)
        open(imagePath + png, 'wb').write(answer.content)

    answer = Digi4SchoolCommunicator.get_file(svgUrl)

    if answer == "404" or answer.text.__contains__("Fehler"):
        break
    print("\t" + str(page) + ".png 200 OK")
    os.makedirs(pagePath, 0o777, True)
    open(svgPath, 'wb').write(answer.content)
