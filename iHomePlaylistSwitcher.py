# iHome Playlist Switcher
# Started 19 June 2014
# By Ross Llewallyn

# NOTES: Starting with just days of week
#        Ideally only load the relevant day/time/value

import time
from enum import Enum
import MM_DB_Mod

def iHomePlaylistSwitcher():
    """Checks the day of the week and changes the playlist in iTunes called "iHome" to whatever is pre-set for that day"""
    
    ##################
    # MEMBER METHODS #
    ##################
    
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
    Alerts       = False

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
                
                if Param is '' or Value is '':
                    continue
                
                if   "MM_DB_Loc"    in Param:
                    MM_DB_Loc = Value
                elif "Alerts"       in Param:
                    if Value == 'True':
                        Alerts = True
                    else:
                        Alerts = False
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
    Weekday = time.localtime(time.time()).tm_wday
    
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
    
    Success = MM_DB_Mod.MM_DB_Mod(MM_DB_Loc, DayPLStr)
    
    ########################
    # PRINT STATUS/RESULTS #
    ########################
    
    if Success:
        if Alerts:
            input(str.format("iHome playlist switch to \"{0}\" succeeded! Press Enter to continue.", DayPLStr))
        else:
            print(str.format("iHome playlist switch to \"{0}\" succeeded!", DayPLStr))
    else:
        if Alerts:
            input(str.format("iHome playlist switch to \"{0}\" failed. Press Enter to continue.", DayPLStr))
        else:
            print(str.format("iHome playlist switch to \"{0}\" failed.", DayPLStr))
    
    return

# ---

if __name__ == "__main__":
    iHomePlaylistSwitcher()
