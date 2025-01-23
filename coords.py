import math
def convert_coordinates():
    transl_x = 123888
    transl_y = 158000
    scale = 459
    print("--- Convert .sav to In-Game Coordinates ---")
    sav_x = int(input("Enter .sav X coordinate: "))
    sav_y = int(input("Enter .sav Y coordinate: "))
    temp_x = sav_x + transl_x
    temp_y = sav_y - transl_y
    in_game_x = round(temp_y / scale)
    in_game_y = round(temp_x / scale)
    print(f"In-game coordinates: X = {in_game_x}, Y = {in_game_y}\n")
    print("--- Convert In-Game to .sav Coordinates ---")
    game_x = int(input("Enter in-game X coordinate: "))
    game_y = int(input("Enter in-game Y coordinate: "))
    temp_x_sav = game_x * scale
    temp_y_sav = game_y * scale
    sav_x_out = round(temp_y_sav - transl_x)
    sav_y_out = round(temp_x_sav + transl_y)
    print(f".sav coordinates: X = {sav_x_out}, Y = {sav_y_out}\n")
convert_coordinates()