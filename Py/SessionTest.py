import os
import sys
from html.parser import HTMLParser

import requests

# Global variables
url = ""
payload = {}
email = "sascha.gottsbacher@aon.at"
password = "BOnqRqMyP1PKWdD8OOtZ"


# no file for this class because python doesnt like me (variables are fucked)
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global payload  # PYTHON WHY THE FUCK
        global url
        # print(tag, ": ", attrs)
        if tag == 'input':
            payload[attrs[0][1]] = attrs[1][1]
        elif tag == 'form':
            for attr in attrs:
                if attr[0] == 'action':
                    url = attr[1]


# URL to download
bookUrl = 'https://a.digi4school.at/ebook/5134/'
urlParts = bookUrl.split("/")

# Paths from URL
bookPath = "./" + urlParts[urlParts.__len__()-2] + "/" + urlParts[urlParts.__len__()-1]
# png = urlParts[urlParts.__len__()-1]

# Start the session
session = requests.Session()

# Send auth request. No manual cookies anymore, hurray!
session.post("https://digi4school.at/br/xhr/login", {"email": email, "password": password})
for page in range(24, 34):
    print(page)
    pagePath = bookPath + "/" + str(page)
    pageUrl = bookUrl + "/" + str(page)

    for image in range(1, 10):
        png = str(image) + ".png"
        imagePath = pagePath + "/img/"
        imageUrl = pageUrl + "/img/" + png
        #png = "1.png"
        # print(png)

        pngPath = pagePath + png
        # First request to get form
        request = session.get(imageUrl)

        # Parse data from form
        string = request.text
        parser = MyHTMLParser()
        parser.feed(string)

        # Output of Parse
        # print(url)
        # print(payload)

        # Send POST to defined URL
        request = session.post(url, data=payload)

        # Do this whole shit again because it doesnt work the first time
        s = request.text

        parser.feed(s)
        # print(url)
        # print(payload)

        # open("7.html", 'wb').write(r.content)
        session.post(url, data=payload)
        request = session.get(imageUrl)
        # Presto, we got an image
        if request.status_code == 200:

            print("\t" + png + " 200 OK")
            os.makedirs(imagePath, 0o777, True)
            open(imagePath + "/" + png, 'wb').write(request.content)
        else:
            break
