import os
import sys
import lxml
import re

def parser(filename):
    lineList = []
    list = []
    with open(filename) as f:
        lineList = f.readlines()
    for line in lineList:
        try:
            list.append(re.findall(r'"(.*?)"', line)[0] + "\n")
        except Exception as e:
            pass
    with open("makeOptionsList.txt", 'w') as output:
        output.writelines(list)




if __name__ == "__main__":
    parser('makeOptions.txt')
