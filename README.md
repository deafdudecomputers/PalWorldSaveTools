# Palworld Save Tools

# Working as of v0.3.7 patch.

- **Author:** MagicBear and cheahjs 
- **License:** MIT License  
- **Updated by:** Pylar and Techdude  
- **Map Pictures Provided by:** Kozejin 
- **Testers/Helpers:** Lethe and Choi-Jungwoo

## Remember to use `clean_up.cmd` after every update for the best performance!

## If it hangs on this picture, or gives error message concerning the cityhash, please attempt this:
![Screenshot3](.github/images/screenshot3.png)
- Install Visual Studios from https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Tick the option that says Desktop development with C++
- Then ensure the following components are selected under the Desktop development with C++: MSVC v142 - VS 2019 C++ x64/x86 build tools, Windows 10/11 SDK(depending on your OS), and C++ CMake tools for Windows
- Afterwards, use clean_up.cmd and try again. Thank you! :)

## Current Features
- **Fast parsing/reading tool**—one of the quickest out there.
- Fixes the 40k pal limit by parsing out inactive pals. **(OBSOLETE, OFFICIALLY FIXED ON 22nd August 2024)**
- Fixes the left mouse bug.
- Lists all players/guilds.
- Lists all pals (All/Deleted/Kept).
- Shows last online time for players.
- Logs players and their relevant information into `players.log`.
- Sorts and deletes players based on level and last online time.
- Logs and sorts players by the number of pals they own.
- Deletes players based on the number of pals.
- Automatically downloads and installs required assets (images/fonts) into the `internal_libs` folder.
- Automatically downloads and installs required libraries (packages) into the `external_libs` folder.
- Automatically downloads and installs the missing `palworld_save_tools` folder (no progress bar and might show "errors" but still usable).
- Allows testing in a Linux environment via `fix_save.sh` and `fix_world.sh`.
- Enables drag-and-drop functionality for world versions of files.
- Enables double-click functionality for save versions of files.
- Provides a base map view through `bases.cmd`.
- Transfers saves between dedicated server and single/coop world.
- Look up the palworld id via steam id by convertids.

## Transferring Local Saves to Server
_read the fix_host_save_readme.txt for instructions and make sure to check the fix_host_save_screenshots for clear images on how to do the instructions properly_

## How to Automatically Delete Player Saves Based on Inactivity
1. Copy everything from your server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`) into the same location within the tool (`PalworldSaveTools\`).
2. Run `fix_save.cmd`.
3. Run `sort_players.cmd` and/or `delete_pals_save.cmd`.
4. Copy the `Players` folder from the tool.
5. Delete the original `Players` folder from the server (`\Pal\Saved\SaveGames\0\RANDOMSERVERID\`).
6. Paste the copied `Players` folder into the server folder.
7. Profit?

## Additional Notes
- **Days:** Tracks players inactive for a specified number of days (e.g., 30 days and older).
- **Level:** Tracks players up to a specified level (e.g., level 30 or lower).
- **Pals:** Deletes players based on the number of pals (e.g., 10 or fewer pals).
- The fixed save (`PalworldSaveTools\fixed\Level.sav`) is no longer functional after patch v0.3+.
- As of update v0.5.5, you can view the total number of pals caught/owned. To do so, copy the server's `Players` folder into the tool's `Players` folder.

![Screenshot1](.github/images/screenshot1.png)
![Screenshot2](.github/images/screenshot2.png)