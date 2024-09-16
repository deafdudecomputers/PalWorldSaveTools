Author: MagicBear
License: MIT License
Updated by: Pylar and Techdude
Map pictures provided by: Kozejin
Testers/helpers: Lethe


Current Features:

One of fastest parsing/reading tools out there.
Ability to fix 40k pal limits by parsing out the inactive pals.
Ability to fix the left mouse bug.
Ability to list all players/guilds.
Ability to list all pals(All/Deleted/Kept pals).
Ability to show last online.
Ability to log players and their relative information into players.log.
Ability to sort and then delete players relating to level and last online.
Ability to log and sort the players based on how many pals they have.
Ability to delete players based off how many pals they have.
Ability to automatically download and install required assets(images/fonts) - in internal_libs folder.
Ability to automatically download and install required libaries(packages) - in external_libs folder.
Ability to automatically download and install the missing palworld_save_tools folder. Altho, this will have no % progression like my personalized version. And has some weird "errors", but still usable.
Ability to test thru linux environment via fix_save.sh and fix_world.sh files.
Ability to drag and drag thru world versions of files.
Ability to double click thru save versions of files.
Ability to see which bases on map via bases.cmd.
Ability to transfer from dedicated server to single/coop world.
Ability to transfer from single/coop world to dedicated server.

***In order to be able to transfer from local to server, you have to use fix_host_save.cmd. Make sure to copy everything from your world from: C:\Users\USERNAME\AppData\Local\Pal\Saved\SaveGames\RANDOMID\ and put it in your server. Start it up, and create a new character, then pick up an item/etc, wait for it to save. Afterwards, copy everything from that server save, then paste everything into LocalWorldSave in my tool. Click on fix_host_save.cmd and input your actual UID, then old UID(from local), and it'll progress everything for you. Then delete the saves from server, and paste the updated files in LocalWorldSave and you're good to go.***

***Make sure to use clean_up.cmd every time you update the tool, it'll ensure the best performance.***


***How to automate delete players saves based off inactive days***

***Method One***
1)Copy the whole Players folder in your server folder(\Pal\Saved\SaveGames\0\RANDOMSERVERID\) into same location as Players folder in my tool(PalworldSaveTools\).
2)Double click on fix_world.cmd.
3)Double click on sort_players.cmd and/or delete_pals_save.cmd.
4)Copy the Players folder from my tool(PalworldSaveTools\).
5)Delete the Players folder from server(\Pal\Saved\SaveGames\0\RANDOMSERVERID\).
6)Paste the copied Players folder into same place you deleted Players folder from(\Pal\Saved\SaveGames\0\RANDOMSERVERID\).
7)Profit?

***Method Two***
1)Copy the files within my tool that has Players folder(PalworldSaveTools\).
2)Paste the copied files into your server save folder(\Pal\Saved\SaveGames\0\RANDOMSERVERID\).
3)Double click on fix_world.cmd.
4)Double click on sort_players.cmd and/or delete_pals_save.cmd.
6)Profit?

Explaination: 
*Days is the variable where it tracks the oldest players starting: IE: 30 days is where players haven't been logged since 30 days and older.
*Level is the variable where it tracks the players starting at max of specified level: IE: 30 level, or lower.
*Delete players based on amount of pals. IE: 10 is players with 10 or less pals will get automatically deleted.
*Fixed save(PalworldSaveTools\fixed\Level.sav) is useless after patch v0.3+. Please do not try to use it, it'll change nothing. Thanks for understanding!
*As of v0.5.5 update, you will be able to get total pals caught/owned. The requirement to grab that data is to get server's Players folder and copy it over into the tool Players folder.


![Screenshot1](.github/images/screenshot1.png)


![Screenshot2](.github/images/screenshot2.png)