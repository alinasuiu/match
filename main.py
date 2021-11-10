from game import Game

def play_game():

    game = Game(2,"values")
    print(game.play())

    game = Game(2000, "values")
    print(game.play())

    game = Game(20000, "Both suits and values")
    print(game.play())

    game = Game(20000, "suits")
    print(game.play())

if __name__ == '__main__':
    play_game()

