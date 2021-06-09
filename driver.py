from tools import *
import os
import pathlib


class driver:

    def URL2File():
        while True:
            inputURL = input(str("Enter the URL of the JSON Object: "))
            JSONfunc = queryJSON(inputURL)
            if JSONfunc.saveData(inputURL) == True:
                return JSONfunc.saveData(inputURL)

    def getIndexandSearch(file):
        print("Downloading object...")
        JSONfunc = queryJSON(file)
        print(JSONfunc.index(file))
        while True:
            inputQuery = input("Search: ")
            print(JSONfunc.search(file, inputQuery))
            searchAgain = input(str("Search Again? (y/n): "))
            if searchAgain.lower() != "y":
                break

    print("Welcome to The JSON Query Program by Eli Jaghab!")

    inputURL = ""
    while True:
        file = pathlib.Path("data.json")
        if file.exists():
            os.remove("data.json")

        URL2File()
        getIndexandSearch("data.json")

        moreFiles = input(str("Query another file? (y/n): "))
        if moreFiles.lower() == "y":
            os.remove("data.json")
        else:
            break


driver()
