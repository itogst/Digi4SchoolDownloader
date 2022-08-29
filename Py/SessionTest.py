import cairosvg
from svglib.svglib import *
from PyPDF2 import PdfFileMerger
from all_svg2pdf import *
from requester import Digi4SchoolCommunicator
import time

run_Download = True
run_SVG_2_PDF = True
run_PDF_merger = True

# URL to download
print("Book number: ")
bookNr = input()

print("Book length: ")
bookLength = int(input())

Digi4SchoolCommunicator.get_credentials()

bookUrl = 'https://a.digi4school.at/ebook/' + bookNr + "/"
urlParts = bookUrl.split("/")

outputString = '.\\files\\output\\'
# Paths from URL
bookPath = "./files/" + bookNr + "/"

png = urlParts[urlParts.__len__() - 1]

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

        for image in range(1, 64):

            png = str(image) + ".png"
            imageUrl = pageUrl + "/img/" + str(image) + ".png"

            answer = Digi4SchoolCommunicator.get_file(imageUrl)

            if answer == "404" or answer.text.__contains__("Fehler"):
                break
            print("\t image: " + png + " 200 OK")
            os.makedirs(imagePath, 0o777, True)
            open(imagePath + png, 'wb').write(answer.content)

        for shade in range(1, 200):

            shading = str(shade) + ".png"
            imageUrl = pageUrl + "/shade/" + str(shade) + ".png"

            answer = Digi4SchoolCommunicator.get_file(imageUrl)

            if answer == "404" or answer.text.__contains__("Fehler"):
                break
            print("\t shade: " + shading + " 200 OK")
            os.makedirs(pagePath + "/shade", 0o777, True)
            open(pagePath + "/shade/" + shading, 'wb').write(answer.content)

        answer = Digi4SchoolCommunicator.get_file(svgUrl)
        name = (3 - str(page).__len__()) * "0" + str(page)

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
