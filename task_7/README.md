# Sea Battle Game

A modern implementation of the classic Battleship game, where you play against a computer opponent.

## Prerequisites

Before you can run the game, you need to install:

1. **Node.js**: 
   - Go to [Node.js website](https://nodejs.org/)
   - Download and install the "LTS" (Long Term Support) version
   - To verify installation, open a terminal/command prompt and type:
     ```
     node --version
     ```
   - You should see a version number (e.g., v18.17.0)

## Installation

1. Open a terminal/command prompt
2. Navigate to the game directory (where this README is located)
3. Install dependencies by running:
   ```
   npm install
   ```
   This will install all necessary packages.

## Running the Game

1. In the terminal/command prompt, make sure you're in the game directory
2. Build and start the game:
   ```
   npm start
   ```

## How to Play

1. The game displays two 10x10 boards:
   - Left board: Your opponent's ships (hidden)
   - Right board: Your ships (visible)

2. Board symbols:
   - `~` : Empty water
   - `S` : Your ship
   - `X` : Hit
   - `O` : Miss

3. Making moves:
   - Enter coordinates as two digits (row then column)
   - Example: `34` means row 3, column 4
   - Valid coordinates are 00 through 99

4. Game flow:
   - You and the CPU take turns
   - Hit all enemy ships to win
   - Protect your ships from being hit

## Example Game Session

```
   --- OPPONENT BOARD ---          --- YOUR BOARD ---
  0 1 2 3 4 5 6 7 8 9       0 1 2 3 4 5 6 7 8 9
0 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     0 ~ S S S ~ ~ ~ ~ ~ ~
1 ~ ~ O ~ ~ ~ ~ ~ ~ ~     1 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
2 ~ ~ ~ X ~ ~ ~ ~ ~ ~     2 ~ ~ ~ ~ ~ S S S ~ ~
3 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     3 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~     4 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

Enter your guess (e.g., 34 for row 3, column 4): 25
HIT! You found an enemy ship!
```

## Running Tests

To run the test suite and see coverage:
```
npm test
```

## Files and Structure

- `src/Game.ts`: Main game controller
- `src/GameLogic.ts`: Core game mechanics
- `src/GameUI.ts`: Display and user interface
- `src/types.ts`: Type definitions
- `tests/`: Test files
- `dist/`: Compiled JavaScript (created after build)

## Troubleshooting

1. If you see "command not found: npm":
   - Make sure Node.js is installed
   - Try closing and reopening your terminal

2. If installation fails:
   - Make sure you have internet connection
   - Try running `npm cache clean --force` then retry installation

3. If the game doesn't start:
   - Make sure you ran `npm install` first
   - Check that you're in the correct directory
   - Try running `npm run build` then `node dist/Game.js` 