# MediaMonkey Database Modifier
# Started 25 June 2014
# By Ross Llewallyn

# NOTES: Possibly an issue with using only higher-numbered values for IDPlaylistSong.
#        Not sure of severity or details.

import sqlite3

def MM_DB_Mod(DB_Loc, New_PL):
    """Accesses the MediaMonkey database to replace the iHome playlist with the selection for the given weekday"""

    iHomeStr = 'iHome'
    
    # From Sproaticus: http://www.mediamonkey.com/forum/viewtopic.php?f=2&t=25637#p144852
    # define IUNICODE collation function
    def iUnicodeCollate(s1, s2):
        return s1.lower() != s2.lower()
    
    try:
        # Access database
        conn = sqlite3.connect(DB_Loc)
        
        # From Sproaticus: http://www.mediamonkey.com/forum/viewtopic.php?f=2&t=25637#p144852
        # register our custom IUNICODE collation function
        conn.create_collation('IUNICODE', iUnicodeCollate)
        
        conn.row_factory = sqlite3.Row
        
        c = conn.cursor()
        
        # Get playlist IDs from new and old list
        c.execute('''SELECT IDPlaylist FROM Playlists WHERE PlaylistName=?''', (New_PL,))
        
        fetched = c.fetchone()
        if fetched:
            New_PL_ID = fetched['IDPlaylist']
        else:
            print("Selected playlist for today could not be found: \"" + New_PL + "\"")
            return False
        
        c.execute('''SELECT IDPlaylist FROM Playlists WHERE PlaylistName=?''', (iHomeStr,))
        iHome_PL_ID = c.fetchone()['IDPlaylist']
        
        # Remove old iHome playlist songs
        c.execute('''DELETE FROM PlaylistSongs WHERE IDPlaylist=?''', (iHome_PL_ID,))
        
        # Find current highest IDPlaylistSong value to start from
        c.execute('''SELECT MAX(IDPlaylistSong) FROM PlaylistSongs''')
        
        IDPLS = c.fetchone()[0] + 1
        
        # Obtain new playlist songs
        c.execute('''SELECT * FROM PlaylistSongs WHERE IDPlaylist=?''', (New_PL_ID,))
        
        # Create a list and collect all songs for the new playlist
        # with modified playlist ID for "iHome"
        row_List = list()
        
        row = c.fetchone()
        
        if row is None:
            print("Playlist songs were not found: \"" + New_PL + "\"")
            return False
        
        # ['IDPlaylistSong', 'IDPlaylist', 'IDSong', 'SongOrder']
        
        while row != None:
            row_List.append((IDPLS, iHome_PL_ID, row[2], row[3]))
            IDPLS += 1
            row = c.fetchone()
        
        # Insert new list (copied from old), now connected to "iHome" playlist
        c.executemany('''INSERT INTO PlaylistSongs VALUES (?,?,?,?)''', row_List)
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e
    
    return False

if __name__ == '__main__':
    MM_DB_Mod("C:\\Users\\Ross the boss\\AppData\\Roaming\\MediaMonkey\\MM.db", "Rock")
