# * last update 15/04/2023 7:37PM
# today I separated the move method into few minor methods to make it easier to read

# * what should I do next?
# 1. Making queen movement and capturing (bcs of obvious reasons)

from game import Game

def main():
    game = Game()
    game.game_loop()

if __name__ == "__main__":
    main()