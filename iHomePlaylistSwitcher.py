# iHome Playlist Switcher
# Started 19 June 2014
# By Ross Llewallyn

# NOTE: Starting with just days of week
# Ideally only load the relevant day/time/value

import time
from enum import Enum
import xml.etree.ElementTree as ET # Use cElementTree?

def iHomePlaylistSwitcher():
    """Checks the day of the week and changes the playlist in iTunes called "iHome" to whatever is pre-set for that day"""
    
    class DayOfWeekType(Enum):
        Monday    = 0
        Tuesday   = 1
        Wednesday = 2
        Thursday  = 3
        Friday    = 4
        Saturday  = 5
        Sunday    = 6
    
    class DayPlaylist:
    
        def __init__(self, DayOfWeek, PlaylistStr):
            self.DayOfWeek   = DayOfWeek
            self.PlaylistStr = PlaylistStr
        
        DayOfWeek = DayOfWeekType.Monday
        PlaylistStr = ""
    
    def LineAComment(inStr):
        return (inStr.lstrip()).startswith('#')
    
    def LineEmpty(inStr):
        return (inStr.strip() is '')
    
    def GetParam(inStr):
        return inStr[:inStr.find("=")]
    
    def GetValue(inStr):
        return inStr[(inStr.find("=") + 1):]
    
# ---
    
    MM_DB_Loc    = ""
    DayPlaylists = list()
    DayPLStr     = ""
    iHomePLEle   = None
    DayPLEle     = None

    #######################
    # CONFIG FILE PARSING #
    #######################
    
    # Load configuration file
    with open('iHomePlaylistSwitcher.cfg', 'r') as f1:
        # Parse config file
        for line in f1:
            if   LineAComment(line):
                continue
            elif LineEmpty(line):
                continue
            elif '=' in line:
                Param = GetParam(line)
                Value = GetValue(line).strip()
                
                if   "MM_DB_Loc"    in Param:
                    MM_DB_Loc = Value
                elif "Alerts"       in Param:
                    Value
                elif "Monday"       in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Monday,    Value))
                elif "Tuesday"      in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Tuesday,   Value))
                elif "Wednesday"    in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Wednesday, Value))
                elif "Thursday"     in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Thursday,  Value))
                elif "Friday"       in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Friday,    Value))
                elif "Saturday"     in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Saturday,  Value))
                elif "Sunday"       in Param:
                    DayPlaylists.append(DayPlaylist(DayOfWeekType.Sunday,    Value))
    
    # Config file closed

    #########################
    # DAY PLAYLIST MATCHING #
    #########################
    
    # Get day of the week
    Weekday = time.gmtime(time.time()).tm_wday
    
    for day in DayPlaylists:
        if DayOfWeekType(Weekday) is day.DayOfWeek:
            DayPLStr = day.PlaylistStr
            break

    if DayPLStr is "":
        print("Today does not have a new playlist. iHome playlist not updated.")
        return
    
    ###############################
    # MEDIAMONKEY DATABASE ACCESS #
    ###############################
    
    MM_DB_Mod(MM_DB_Loc, DayPLStr)
    
    return
    
# --- Old, unused stuff for iTunes
    
    ##########################
    # ITUNES LIBRARY PARSING #
    ##########################
    
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
    

# ---

iHomePlaylistSwitcher()
