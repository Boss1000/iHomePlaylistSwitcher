# MediaMonkay Database Modifier
# Started 25 June 2014
# By Ross Llewallyn

import sqlite3

def MM_DB_Mod(DB_Loc, New_PL):
    """Accesses the MediaMonkey database to replace the iHome playlist with the selection for the given weekday"""

    # From Sproaticus: http://www.mediamonkey.com/forum/viewtopic.php?f=2&t=25637#p144852
    # define IUNICODE collation function
    def iUnicodeCollate(s1, s2):
        return s1.lower() == s2.lower()
    
    try:
        # Access database
        conn = sqlite3.connect(DB_Loc)
        c = conn.cursor()
        
        # From Sproaticus: http://www.mediamonkey.com/forum/viewtopic.php?f=2&t=25637#p144852
        # register our custom IUNICODE collation function
        conn.create_collation('IUNICODE', iUnicodeCollate)
        
        # Get playlist IDs from new and old list
        c.execute('''SELECT IDPlaylist FROM Playlists WHERE PlaylistName=?''', (New_PL,))
        
        # Find index of playlist ID
        I = -1
        for key in c.fetchone():
            I += 1
            if key == 'IDPlaylist':
                break
        
        New_PL_ID = c.fetchone()[I]
        
        c.execute('''SELECT IDPlaylist FROM Playlists WHERE PlaylistName=?''', ('iHome',))
        iHome_PL_ID = c.fetchone()[I]
        
        # Remove old iHome playlist songs
        c.execute('''DELETE FROM PlaylistSongs WHERE IDPlaylist=?''', str(iHome_PL_ID))
        
        # Obtain new playlist songs
        c.execute('''SELECT * FROM PlaylistSongs WHERE IDPlaylist=?''', str(New_PL_ID))
        
        # Create a list and collect all songs for the new playlist
        # with modified playlist ID for "iHome"
        row_List = list()
        
        row = c.fetchone()

        if row is None:
            print("Playlist was not found: ", New_PL)
            return

        # Find index of playlist ID
        I = -1
        for key in row:
            I += 1
            if key == 'IDPlaylist':
                break
        
        while row != None:
            row[I] = iHome_PL_ID
            row_List.append(row)
            
            row = c.fetchone()
        
        # Insert new list (copied from old), now connected to "iHome" playlist
        c.execute('''INSERT INTO PlaylistSongs''', row_List)
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    
MM_DB_Mod("C:\\Users\\Ross the boss\\Desktop\\TestMusic\\MM.DB", "Arrows")
