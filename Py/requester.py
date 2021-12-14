from html.parser import HTMLParser

import requests

ltiUrl = ""
payload = {}


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global payload  # PYTHON WHY THE FUCK
        global ltiUrl
        # print(tag, ": ", attrs)
        if tag == 'input':
            payload[attrs[0][1]] = attrs[1][1]
        elif tag == 'form':
            for attr in attrs:
                if attr[0] == 'action':
                    ltiUrl = attr[1]

    def error(self, message):
        print(message)
        print("no bloody clue")


session = requests.Session()


class Digi4SchoolCommunicator:

    @staticmethod
    def get_file(file_url):
        # login begin

        email = "sascha.gottsbacher@aon.at"
        password = "BOnqRqMyP1PKWdD8OOtZ"
        session.post("https://digi4school.at/br/xhr/login", {"email": email, "password": password})
        # login end

        # get lti form begin
        answer = session.get(file_url)
        # get lti form end

        # request until cookies have been obtained
        for i in range(5):

            try:
                session.cookies["digi4p"]
                return answer

            except KeyError:
                # translate lti form into request
                string = answer.text
                parser = MyHTMLParser()
                parser.feed(string)
                # translate lti form into request

                # post lti form
                # payload["resource_link_id"] = "5134"
                answer = session.post(ltiUrl, data=payload)
                # post lti form
        # request until cookies have been obtained

        # return requested file  in bytes
        return "404"

