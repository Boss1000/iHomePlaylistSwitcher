# iHome Playlist Switcher
# Started 19 June 2014
# By Ross Llewallyn

# NOTE: Starting with just days of week

import time
import calendar

def iHomePlaylistSwitcher():
    """Checks the day of the week and changes the playlist in iTunes called "iHome" to whatever is pre-set for that day."""
    
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
        
        DayOfWeek = Monday
        PlaylistStr = ""

    def GetParamValue(inStr):
        return inStr[(inStr.find("=") + 1):len(inStr)]

# ---
    
    iTunesLibraryLocation = ""
    DayPlaylists = list()
    
    # Load configuration file
    f = open('iHomePlaylistSwitcher.cfg', 'r')

    for line in f:
        if   "iTunesLibraryLocation" in line:
            iTunesLibraryLocation = GetParamValue(line)
        elif "Monday"    in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Monday,    GetParamValue(line)))
        elif "Tuesday"   in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Tuesday,   GetParamValue(line)))
        elif "Wednesday" in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Wednesday, GetParamValue(line)))
        elif "Thursday"  in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Thursday,  GetParamValue(line)))
        elif "Friday"    in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Friday,    GetParamValue(line)))
        elif "Saturday"  in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Saturday,  GetParamValue(line)))
        elif "Sunday"    in line:
            DayPlaylists.append(DayPlaylist(DayOfWeekType.Sunday,    GetParamValue(line)))

        
    
    # Get day of the week
    Weekday = time.gmtime(time.time()).tm_wday
    
    
