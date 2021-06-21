
# GLOBAL VARIABLES
genres = ["Sandbox", "Real-time strategy (RTS)", "Shooters (FPS and TPS)", "Multiplayer online battle arena (MOBA)", "Role-playing (RPG, ARPG, and More)", "Simulation and sports", "Puzzlers and party games", "Action-adventure", "Survival and horror", "Platformer"]

game_types = {
    "Minecraft": [5, genres[0], genres[8]],
    "Valorant": [4, genres[1], genres[2]],
    "Pokemon Shield & Sword": [6, genres[4]],
    "Battlefield 4": [3, genres[2]],
    "Mario Kart": [1, genres[6], genres[7]]
}
def main():
    is_on = True

    while is_on:
        prompt = input("[Add], [Find] games of a specific genre, [Get Rank] of game, or [Quit]: ")
        if prompt == "Add":
            user_game = input("Game: ")
            user_upvotes = int(input("Number of upvotes: "))
            user_genres = input("Genres: ")
            game_types[user_game] = [user_upvotes, user_genres]
        elif prompt == "Find":
            prompt2 = input("Genre: ")
            print(recommender(prompt2))
        elif prompt == "Get Rank":
            prompt2 = int(input("Top (number): "))
            if prompt2 <= len(game_types):
                print(game_ranker(prompt2))
            else:
                print("Rank exceeds number of games.")
        elif prompt == "Quit":
            is_on = False

def game_ranker(search_ranks):
    ranked_list = []
    if search_ranks > len(game_types):
        print("Number too high.")
    else:
        #search_ranks < len(game_types):
        game_types_fixed = sorted(game_types, key=game_types.get, reverse=True)
        for y in game_types_fixed:
            if search_ranks > len(ranked_list):
                ranked_list.append(y)
        return ranked_list


def recommender(genre):
    games_recommended = []
    for game, data in game_types.items():
        if genre in data:
            games_recommended.append(game)
    return games_recommended

main()
# if __name__ == '__main__':
#     sys.exit(main())