import requests
import getdata
import os
import re

# Steam API endpoint and fetching the list of all Steam apps
url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
response = requests.get(url)
data = response.json()


def search_steam_game(game_name):
    try:
        # Searching for the game name in the list
        app_list = data["applist"]["apps"]
        matched_games = []
        for app in app_list:
            if game_name.lower() in app["name"].lower():
                matched_games.append(app)

        # Game not found
        if len(matched_games) == 0:
            return None

        return matched_games

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)
        return None


def display_search_results(matched_games):
    total_games = len(matched_games)

    if total_games == 0:
        print("No games found.")
        return

    print("Search Results:")
    for i, game in enumerate(matched_games):
        print(f"{i}. {game['name']} - App ID: {game['appid']}")

    print(f"\nSelect a game (0 to {total_games - 1})")
    print("Options: [r] research, [m] main menu, [q] quit\n")

    # game = matched_games[current_index]
    # print(f"Selected Game: {game['name']} - App ID: {game['appid']}")


while True:
    def main():
        menu = input("1. Search game name\n2. Enter app id\n3. Paste Steam url\nInput: ")
        if menu == "1":
            game_name = input("Enter the game name: ")
            matched_games = search_steam_game(game_name)
            display_search_results(matched_games)

            option = input("Input: ")
            if option.isdigit():
                selected_index = int(option)
                if 0 <= selected_index < len(matched_games):
                    game = matched_games[selected_index]
                    app_id = game['appid']
                    getdata.table_result(app_id)
                    # print(f"Selected App ID: {app_id}")
                    option = input("Back? [y/n]")
                    if option == "y":
                        main()
                    os.system('cls')
                else:
                    print("Invalid game index. Try again.")
            elif option == "q":
                print("thanks for using :)")
            elif option == "m":
                main()
            elif option == "r":
                main()
            else:
                print("Invalid option. Try again.")
                main()
            os.system('cls||clear')

        elif menu == "2":
            app_id = input("Enter the app id: ")
            getdata.table_result(app_id)
            option = input("Back? [y/n]")
            if option == "y":
                main()
            os.system('cls||clear')

        elif menu == "3":
            link = input("Enter url: ")
            app_id = re.search(r'/(\d+)/', link).group(1)
            getdata.table_result(app_id)
            option = input("Back? [y/n]")
            if option == "y":
                main()
            os.system('cls||clear')
        
    os.system('cls||clear')
    main()
    print("Program terminated.")
    break
