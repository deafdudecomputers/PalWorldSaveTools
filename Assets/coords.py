from collections import namedtuple
__transl_x = 123888
__transl_y = 158000
__scale = 459
Point = namedtuple('Point', ['x', 'y'])
def get_number_in_range(min_value, max_value):
    while True:
        try:
            number = int(input(f"Enter a number between {min_value} and {max_value}: "))
            if min_value <= number <= max_value:
                return number
            else:
                print("Number is out of range. Try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
def sav_to_map(x: float, y: float) -> Point:
    newX = x + __transl_x
    newY = y - __transl_y
    return Point(x=round(newY/__scale), y=round(newX/__scale))
def map_to_sav(x: int, y: int) -> Point:
    newX = x * __scale
    newY = y * __scale
    return Point(x=newY - __transl_x, y=newX + __transl_y)
def main():
    print("1. Convert .sav to in-game")
    print("2. Convert in-game to .sav")
    intUserChoice = get_number_in_range(1, 2)
    if intUserChoice == 1:
        try:
            sav_x = int(input("Enter Sav X coordinate: "))
            sav_y = int(input("Enter Sav Y coordinate: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
        print(sav_to_map(sav_x ,sav_y))
    if intUserChoice == 2:
        try:
            game_x = int(input("Enter In-game X coordinate: "))
            game_y = int(input("Enter In-game Y coordinate: "))
        except ValueError:
            print("Invalid input. Please enter an integer.")
        print(map_to_sav(game_x ,game_y))
if __name__ == "__main__":
    main()