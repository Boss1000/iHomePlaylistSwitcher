iHomePlaylistSwitcher
=====================

"Checks the day of the week and changes the playlist in MediaMonkey called 'iHome' to whatever is configured for that day"

Purpose
-------

iHome products are commonly clock radios that can use mp3 players (specifically iPods) to play music (or podcasts). They are not made by Apple, however: http://www.ihomeaudio.com/

I enjoy the one that I received several years ago. It allows the user to create a kind of "alarm playlist" to wake up to in the morning. This is done by creating a playlist in iTunes called "iHome", filling it with any songs desired, loading it onto the iPod, and placing it on the iHome. I've been doing this for a long while.

The purpose of this program is to allow the user to have multiple playlists that work in as the "alarm playlist" by switching out the iHome playlist for another based on a configuration file and different days of the week. It is designed to be run each day at some point before syncing your iPod.

Its purpose is fairly narrow and likely just for me and my routine and hardware. But anyone can use it!

Notes
-----

__Make a copy of your MediaMonkey database before using this program, just in case!__

The playlists you list in the config file are only copied into the iHome playlist. They are not renamed or at risk of being lost. The iHome playlist, however, will be wiped repeatedly!

Any extra spaces in the config file may cause errors in parsing.

This program was made with the following software and hardware:
 - Windows 8
 - Python 3.4
 - MediaMonkey 4.1.3
 - iPod Classic
 - iHome clock radio

(Variations from this I can't guarantee will work.)

Instructions
------------

1. Clone this repo. You need:
 - iHomePlaylistSwitcher.py
 - MM_DB_Mod.py
 - iHomePlaylistSwitcher.cfg

2. Make a shortcut to iHomePlaylistSwitcher.py. Place it in the Startup folder in Windows. For Windows 8, that's the following location: C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

3. Open iHomePlaylistSwitcher.cfg for editing:
 - Change the "MM_DB_Loc" parameter to your MediaMonkey database location, which may be just a user name swap.
 - Assign days of the week certain playlists.
   - Any days you do not include will leave the previous day's intact.
 - Select whether you want to be notified that the playlist switch is complete each day (True) or not (False).
 - Set your average waking hour (24-hour time), which will ensure that if this program is run after that time, it will load tomorrow's playlist for the next morning.
 - (Further explanations of parameters are in that file.)

4. Try it out! Either restart to test it automatically running or run it immediately.

Development
-----------

This is another early dive into Python coding for me!

After substantial initial work trying to edit an iTunes library XML file, I learned that this file does not affect iTunes, and that the actual database (.itl) is proprietary and not stable to try to modify. I learned a lot about element trees while writing the code, which I saved in "ElementTreeTraverse.py". But I was extremely disappointed that most of my program was useless.

After some time (and some friendly encouragement), I began to investigate other programs that could possibly allow my program vision to happen. I had honestly never used Winamp before (llamas and all), and had also been recommended MediaMonkey in the past. I've been a big podcast listener for years, so iTunes feels most familiar and comfortable.

After looking more, I realized that MediaMonkey could work! Not only for the program, but for my entire music organization and listening experience. It has good documentation that describes their database structure, which was absolutely essential for accomplishing my goal: http://www.mediamonkey.com/wiki/index.php/MediaMonkey_Database_structure

This too was only perhaps my second major attempt at SQL-ish commands and database manipulation. Helpful documentation and tutorials online helped me accomplish what I set out to do!

Please let me know if this could be of better use to you with some changes! I'd be stoked to learn someone else is using it. Or go after the problem yourself! Most of this was totally new to me. :)
