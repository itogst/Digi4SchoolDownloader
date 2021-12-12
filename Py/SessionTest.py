import requests

from html.parser import HTMLParser

# Global variables
url = ""
payload = {}


# no file for this class because python doesnt like me (variables are fucked)
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global payload  # PYTHON WHY THE FUCK
        global url
        print(tag, ": ", attrs)
        if tag == 'input':
            payload[attrs[0][1]] = attrs[1][1]
        elif tag == 'form':
            for attr in attrs:
                if attr[0] == 'action':
                    url = attr[1]


# url to download
pngUrl = 'https://a.digi4school.at/ebook/5134/26/img/2.png'

# Start the session
session = requests.Session()
# Add auth cookie, because stupid
session.cookies.set("digi4s",
                    '"143836%2c1639334468%2c1639346112%20{12%200%20C231768D4B3305A40EBF12696521425E8902CFE8}"',
                    domain="digi4school.at")
# First request to get form
request = session.get(pngUrl)

# Parse data from form
string = request.text
parser = MyHTMLParser()
parser.feed(string)

# Output of Parse
print(url)
print(payload)

# Send POST to defined URL
request = session.post(url, data=payload)

# Do this whole shit again because it doesnt work the first time
s = request.text

parser.feed(s)
print(url)
print(payload)

# open("7.html", 'wb').write(r.content)
request = session.post(url, data=payload)

# Presto, we got an image
open("1.png", 'wb').write(request.content)
