import cairosvg
from svglib.svglib import *
from PyPDF2 import PdfFileMerger
from all_svg2pdf import *
from requester import Digi4SchoolCommunicator
import time

run_Download = True
run_SVG_2_PDF = True
run_PDF_merger = True
# TODO - make for loops  into while
# DONE - multithread download
# URL to download
print("Book number: ")
bookNr = input()

print("Book length: ")
bookLength = int(input())

Digi4SchoolCommunicator.get_credentials()

file_extensions = [".png", ".jpg"]

bookUrl = 'https://a.digi4school.at/ebook/' + bookNr + "/"
urlParts = bookUrl.split("/")

outputString = '.\\files\\output\\'
# Paths from URL
bookPath = "./files/" + bookNr + "/"

imageString = urlParts[urlParts.__len__() - 1]

if run_Download:
    if os.path.exists(bookPath) and os.path.isdir(bookPath):
        shutil.rmtree(bookPath)

    for page in range(1, bookLength):

        print(page)
        pagePath = bookPath + str(page)
        pageUrl = bookUrl + str(page)
        imagePath = pagePath + "/img/"

        name = (3 - str(page).__len__()) * "0" + str(page)
        svgUrl = pageUrl + "/" + str(page) + ".svg"
        svgPath = pagePath + "/" + name + ".svg"
        skip = [False, False]
        image = 1
        while not all(skip):
            for i in range(0, file_extensions.__len__()):

                # skip extension if there are no previous
                #if skip[i]:
                    #continue

                imageString = str(image) + file_extensions[i]
                imageUrl = pageUrl + "/img/" + imageString

                answer = Digi4SchoolCommunicator.get_file(imageUrl)

                # skip if no image has been found
                if answer == "404" or answer.text.__contains__("Fehler"):
                    skip[i] = True
                    continue

                skip[i] = False
                print("\t image: " + imageString + " 200 OK")
                os.makedirs(imagePath, 0o777, True)
                open(imagePath + imageString, 'wb').write(answer.content)

            image += 1

        skip = [False, False]
        shade = 1
        while not all(skip):
            for i in range(0, file_extensions.__len__()):
                shadeString = str(shade) + file_extensions[i]
                imageUrl = pageUrl + "/shade/" + shadeString

                answer = Digi4SchoolCommunicator.get_file(imageUrl)

                if answer == "404" or answer.text.__contains__("Fehler"):
                    skip[i] = True
                    continue

                skip[i] = False
                print("\t shade: " + shadeString + " 200 OK")
                os.makedirs(pagePath + "/shade", 0o777, True)
                open(pagePath + "/shade/" + shadeString, 'wb').write(answer.content)

            shade += 1

        answer = Digi4SchoolCommunicator.get_file(svgUrl)
        name = (3 - str(page).__len__()) * "0" + str(page)

        if answer == "404" or answer.text.__contains__("Fehler"):
            answer = Digi4SchoolCommunicator.get_file(bookUrl + str(page) + ".svg")
            svgPath = bookPath + "/" + name + ".svg"
            if answer == "404" or answer.text.__contains__("Fehler"):
                break
        print("\t" + name + ".svg" + " 200 OK")
        os.makedirs(pagePath, 0o777, True)
        open(svgPath, 'wb').write(answer.content)

Digi4SchoolCommunicator.close_session()


def threaded_svg_converter(svgList):
    startTime = time.time()
    for svg in svgList:
        svgParts = str(svg).split("\\")

        input = svg
        output = outputString + \
                 svgParts[1].split(".")[0] + ".pdf"

        cairosvg.svg2pdf(file_obj=open(input, "rb+"), write_to=output)
        print(svg)
    print(time.time() - startTime)


if run_SVG_2_PDF:

    if os.path.exists(outputString) and os.path.isdir(outputString):
        shutil.rmtree(outputString)

    os.makedirs(outputString, 0o777, True)

    svgList = get_file_list("./files/" + bookNr + "/", ".svg")
    # thread1 = threading.Thread(target=threaded_svg_converter, args=(svgList[0:int(nr/4)],)).start()
    # thread2 = threading.Thread(target=threaded_svg_converter, args=(svgList[int(nr/4)+1:int(nr/4)*2],)).start()
    # thread3 = threading.Thread(target=threaded_svg_converter, args=(svgList[int(nr/4)*2+1:int(nr/4)*3],)).start()
    # thread4 = threading.Thread(target=threaded_svg_converter, args=(svgList[int(nr/4)*3+1:int(nr/4)*4],)).start()

    threaded_svg_converter(svgList)

if run_PDF_merger:

    merger = PdfFileMerger()

    for pdf in get_file_list("./", ".pdf"):
        merger.append(pdf)

    merger.write("./files/result.pdf")
    merger.close()
