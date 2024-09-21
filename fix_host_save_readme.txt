
How to use my tool:

Step 1:
Navigate to: C:\Users\YOURUSERNAME\AppData\Local\Pal\Saved\SaveGames, then open the folder with your saves. For example, mine is: 76561198324966967. The full path looks like this: C:\Users\Administrator\AppData\Local\Pal\Saved\SaveGames\76561198324966967.

Inside that folder, you'll find several subfolders for your different worlds. To easily find the one you want to transfer, log into that world, return to this folder, and sort by date. The top folder is the one you'll want to work with.

For example:
C:\Users\Administrator\AppData\Local\Pal\Saved\SaveGames\76561198324966967\E6FFFC26414D717DD932C3BB25B22B8F
This is the world I'll be working with. Your folder will have a different name. 

Copy the Players folder and Level.sav from that folder.

Go to my tool, and paste the copied Players folder and Level.sav into LocalWorldSave.

Step 2:
Set up a dedicated server. Make sure it's fresh, with no Level.sav or Players folder. Let it start up THEN generate new serverid. It should look like this: \Pal\Saved\SaveGames\0\47E9DBAD4E29B36ED30DBFA3597301C5.

After that, shut down the server.

Delete all contents within "47E9DBAD4E29B36ED30DBFA3597301C5" folder.

Copy the Players folder and Level.sav from LocalWorldSave and paste them into this "47E9DBAD4E29B36ED30DBFA3597301C5" folder. The server's Players folder should initially only have one save: 00000000000000000000000000000001.sav. This can be with an exception of your buddies who plays on that server. Just make note of what these saves are. 

Step 3:
Start up the server. Join the server and create your character. After setting up and spawning into the world, pick up an item (wood, rock, etc.) to trigger an auto-save. By default, it should save every 30 seconds.

Step 4:
Check the server's Players folder. You should now see two save files: 00000000000000000000000000000001.sav and a new one, such as 4E6DACB6000000000000000000000000.sav. This can be with an exception of your buddies who plays on that server. Just make note of what these saves are. 

Step 5:
Shut down the server. 
Copy the server’s Players folder and Level.sav.

Step 6:
Paste the server’s Players folder and Level.sav into LocalWorldSave, and confirm any prompts to overwrite files.

Step 7:
Run fix_host_save.cmd from my tool.
Enter 4E6DACB6000000000000000000000000 as your "new GUID," and 00000000000000000000000000000001 as your "old GUID."
The tool will download/extract assets if it hasn’t been run before. After backing up your files (just in case), hit enter to complete the merge.

Step 8:
Verify that the Players folder in LocalWorldSave no longer contains 00000000000000000000000000000001.sav, and only the new save file remains, like 4E6DACB6000000000000000000000000.sav. This can be with an exception of your buddies who plays on that server. Just make note of what these saves are. 

Step 9:
Copy everything in LocalWorldSave.

Step 10:
Go to your server's save location, "47E9DBAD4E29B36ED30DBFA3597301C5", and delete all existing files.

Step 11:
Paste the contents of LocalWorldSave into that folder, "47E9DBAD4E29B36ED30DBFA3597301C5".

Step 12:
Go into the Players folder and confirm there is only one save file. This can be with an exception of your buddies who plays on that server. Just make note of what these saves are. 

Step 13:
Start the server, log into the game, and your character should load with everything intact—pals, palbox, bases, etc.

Enjoy your dedicated server with your host save! 😎