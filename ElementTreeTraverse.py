# This is a code snippet from my original attempt to automate changing the iHome playlist.
# It was my first work in traversing an element tree, so I'm keeping it.

import xml.etree.ElementTree as ET # Use cElementTree?

##########################
# ITUNES LIBRARY PARSING #
##########################

iTunesLibLoc = 'iTunes.xml'

if iTunesLibLoc != '':
    with open(iTunesLibLoc, 'r+') as f2:
        tree = ET.parse(f2) # Probably lengthy
        root2 = tree.getroot()[0]
        plArray = None
        index = 0
        childList = root2.getchildren()
        for child in childList:
            if child.text == "Playlists":
                plArray = root2[index+1] # Playlist <array> element is after "<key>Playlists</key>"
                break
            index += 1

        if plArray is None:
            print("Could not find playlist list in iTunes library.")
            return
        
        for PL in plArray:
            if PL[1].tag == "string" and PL[2].text == "Playlist ID":
                if PL[1].text == "iHome":
                    iHomePLEle = PL
                if PL[1].text == DayPLStr:
                    DayPLEle   = PL
        
        if iHomePLEle is None:
            print("No iHome playlist found. Please create a blank one in iTunes and rerun.")
            return
        if DayPLEle   is None:
            print("Today's playlist not found: ", DayPLStr)
            return
        
        #####################################
        # SAVE & REPLACE OLD IHOME PLAYLIST #
        #####################################
        
        # TODO Save
        
        iHomeSongs = iHomePLEle.find("array")
        iHomeSongsIndex = iHomePLEle.getchildren().index(iHomeSongs)
        iHomePLEle[iHomeSongsIndex] = DayPLEle.find("array")
        
        tree.write(iTunesLibLoc)
        
        print("iHome playlist updated to: ", DayPLStr)

# Library file closed
