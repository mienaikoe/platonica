# platonica

A game of puzzles with platonic solids

Created By:
Alice Wong: https://github.com/9ae
Jesse Lee: https://github.com/mienaikoe

## Running the Game

- We're using Python 3 (This was built with Python 3.10.7)
- move into the game directory `cd game`
- pip install all of the requirements: `pip install -r requirements.txt`
- to run the game, `python main.py`

## "Hacking" the game with environment variables

We use some environment variables to run with special game modifiers. These are listed as follows:

- `SKIP_TUTORIAL=1` The game will skip the tutorial when launched
- `START_LEVEL=<number>` The game will start at a certain level, bypassing all previous levels, depending on which number you use. 0: tetrahedron, 1: cube, 2: octahedron, 3: icosahedron, 4: dodecahedron
- `OVER_EASY=1` Every puzzle will start out in the solved state. You'll have to rotate a face 3 times for this to register, however.

## Known Bugs

- Sometimes, clicking on the screen will stop working. To fix this, click out of the game window and back into it. We tried to fix this for several hours and nothing seemed to work. It could be a bug with pygame on mac?

- Sometimes rotation will stop working. This is probably our bug, but we couldn't get it to happen often enough to figure out how to solve it. You'll have to quit the game and restart it to fix this.

## Special Thanks

Special thanks to our playtesters!

- Percy Hsu
- Denise Sison
- Kevin Rejko
- Alex Browne
