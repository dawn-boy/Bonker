# ---IMPORTS---
from colorthief import ColorThief
import os
from random import randint

# CHOSES A RANDOM IMAGE.
randomInt = randint(0,18)
image = '/home/Dew/Pictures/.walls/{}.jpg'.format(randomInt)

# ---FUNCTIONS---
def colorGen(image):
    colorThief = ColorThief(image)
    pallete = colorThief.get_palette(color_count=15)
    return pallete
def hexer(colorList):
    rgbSumList = [sum(color) for color in colorList]
    rgbDict = {}
    for index in range(len(rgbSumList)):
        rgbDict[rgbSumList[index]] = colorList[index]
    sortedRBGList = sorted(rgbDict.items())
    hexList = ["{:02x}{:02x}{:02x}".format(rgbVal[0], rgbVal[1], rgbVal[2]) for rgbSum, rgbVal in sortedRBGList]
    return hexList  
def lineFinder(searchStr,file):
    for index,line in enumerate(file):
        if searchStr in line:
            return index

# GENERATES A COLOR(HEXADECIMAL) LIST.
colorList = colorGen(image)
hexList = hexer(colorList)

# READS THE config.py FILE FOR QTILE.
path = '/home/Dew/.config/qtile/'
with open(path+'config.py','r') as qtileFile:
    qtileContents = qtileFile.readlines()

# BACKING UP THE config.py FOR QTILE.
qtileBackUp = qtileContents.copy()

# CHECKING FOR PRE_EXISTING colors LIST AND DELETING IF SO.
if 'global' in qtileContents[0]:
    qtileContents.pop(0)
    qtileContents.pop(0)

# PREPARING THE DATA.
finalQtileContents = ["global colors\ncolors = {}\n".format(hexList)]
finalQtileContents.extend(qtileContents)

# WRITING THE config.bak FILE FOR QTILE.
with open(path+'config.bak','w') as qtileBackUpFile:
    qtileBackUpFile.writelines(qtileBackUp)
# WRITING THE config.py FILE FOR QTILE.
with open(path+'config.py','w') as qtileFile:
    qtileFile.writelines(finalQtileContents)

# READING THE alacritty.yml CONFIG FILE FOR ALACRITTY.
path='/home/Dew/.config/alacritty/'
with open(path+'alacritty.yml','r') as alacrittyFile:
    alacrittyContents = alacrittyFile.readlines()
# BACKING UP THE alacritty.yml FILE FOR ALACRITTY.
alacrittyBackUpList = alacrittyContents.copy()

# FIND THE LINE WHERE THE PROPERTY IS.
index = lineFinder('background', alacrittyContents)
# EDITING THE PROPERTY.
alacrittyContents[index] = "      background: '#{}'\n".format(hexList[0])

# WRITING THE BACKUP alacritty.bak FILE FOR ALACRITTY
with open(path+'alacritty.bak','w') as alacrittyBackUp:
    alacrittyBackUp.writelines(alacrittyBackUpList)
# WRITING THE CONFIG alacritty.yml FILE FOR ALACRITTY
with open(path+'alacritty.yml','w') as alacrittyFile:
    alacrittyFile.writelines(alacrittyContents)
