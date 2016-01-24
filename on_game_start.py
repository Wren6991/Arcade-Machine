from xml.dom.minidom import parse, parseString
from os import path
import sys
import shutil
import re

www_root = "/var/www"

log = open(www_root + "/scrapelog", "w")

def unescape(filename):
    return re.sub(r'(?<!\\)\\', '', filename)

def scrapegame(game):
    log.write("Game found.") 
    of = open(www_root + "/current_game.xml", "w")
    of.write(game.toprettyxml())
    of.close()
    imagenodelist = game.getElementsByTagName("image")
    imagepath = imagenodelist[0].firstChild.nodeValue if len(imagenodelist) > 0 else "" 
    imagepath = re.sub("^~", "/home/pi", imagepath)
    if path.exists(imagepath):
        log.write("copying game image: " + imagepath + "\n")
        shutil.copyfile(imagepath, www_root + "/current_game.jpg")    
    else:
        log.write("no game image, using default")
        shutil.copyfile(www_root + "/rpi_logo.jpg", www_root + "/current_game.jpg")
    log.write("Scrape complete.")

def setsensibledefaults():
    log.write("Some sort of error... Writing default info file.")
    of = open(www_root + "/current_game.xml", "w")
    of.write("<game><name>" + game_path + "</name></game>")
    of.close()
    shutil.copyfile(www_root + "/rpi_logo.jpg", www_root + "/current_game.jpg")

sys_name = sys.argv[1]
game_path = unescape(path.basename(sys.argv[2]))

try:
    gamelist_root = parse("/home/pi/.emulationstation/gamelists/" + sys_name + "/gamelist.xml")
    log.write('Scraping for game: "' + game_path + '"\n')
    log.write('Full path: "' + sys.argv[2] + '"\n')

    games = gamelist_root.getElementsByTagName("game")

    found = False
    for game in games:
        gamepathxml = game.getElementsByTagName("path")[0].firstChild.nodeValue
        log.write('Checking "' + gamepathxml + '"...')
        if game_path in gamepathxml:
            found=True
            scrapegame(game)
	    break

    if not found:
        log.write("Could not find game in " + sys_name + "/gamelist.xml")
        setsensibledefaults()
except Exception as e:
    setsensibledefaults()
    log.write("Exception string:\n" + str(e))
    print(str(e))
finally:
    of = open(www_root + "/in_game", "w")
    of.write("1")
    of.close()
    log.close()
