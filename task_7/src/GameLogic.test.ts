import { GameLogic } from './GameLogic';
import { GameConfig, Ship } from './types';

describe('GameLogic', () => {
  let game: GameLogic;
  const config: GameConfig = {
    boardSize: 5,
    numShips: 2,
    shipLength: 2,
  };

  beforeEach(() => {
    game = new GameLogic(config);
  });

  describe('Game Initialization', () => {
    test('should create empty boards of correct size', () => {
      const state = game.getGameState();
      expect(state.playerBoard.length).toBe(config.boardSize);
      expect(state.cpuBoard.length).toBe(config.boardSize);
      expect(state.playerBoard[0].length).toBe(config.boardSize);
      expect(state.cpuBoard[0].length).toBe(config.boardSize);
    });

    test('should initialize game with correct number of ships', () => {
      const state = game.getGameState();
      expect(state.playerNumShips).toBe(config.numShips);
      expect(state.cpuNumShips).toBe(config.numShips);
    });
  });

  describe('Ship Placement', () => {
    test('should place correct number of ships for player', () => {
      game.placeShipsRandomly(true);
      const state = game.getGameState();
      expect(state.playerShips.length).toBe(config.numShips);
    });

    test('should place correct number of ships for CPU', () => {
      game.placeShipsRandomly(false);
      const state = game.getGameState();
      expect(state.cpuShips.length).toBe(config.numShips);
    });

    test('should place ships with correct length', () => {
      game.placeShipsRandomly(true);
      const state = game.getGameState();
      state.playerShips.forEach(ship => {
        expect(ship.locations.length).toBe(config.shipLength);
        expect(ship.hits.length).toBe(config.shipLength);
      });
    });

    test('should mark player ships on board', () => {
      game.placeShipsRandomly(true);
      const state = game.getGameState();
      let shipCells = 0;
      state.playerBoard.forEach(row => {
        row.forEach(cell => {
          if (cell === 'S') shipCells++;
        });
      });
      expect(shipCells).toBe(config.numShips * config.shipLength);
    });
  });

  describe('Player Guesses', () => {
    test('should reject invalid guess format', () => {
      expect(game.processPlayerGuess('123')).toBe(false);
      expect(game.processPlayerGuess('a1')).toBe(false);
    });

    test('should reject out of bounds guesses', () => {
      expect(game.processPlayerGuess('55')).toBe(false);
      expect(game.processPlayerGuess('99')).toBe(false);
    });

    test('should reject repeated guesses', () => {
      game.processPlayerGuess('00');
      expect(game.processPlayerGuess('00')).toBe(false);
    });

    test('should process valid guess', () => {
      expect(game.processPlayerGuess('00')).toBe(true);
      const state = game.getGameState();
      expect(state.guesses).toContain('00');
    });
  });

  describe('CPU Behavior', () => {
    test('should make valid guesses', () => {
      game.processCPUTurn();
      const state = game.getGameState();
      expect(state.cpuGuesses.length).toBe(1);
      const guess = state.cpuGuesses[0];
      expect(guess.length).toBe(2);
      expect(parseInt(guess[0])).toBeLessThan(config.boardSize);
      expect(parseInt(guess[1])).toBeLessThan(config.boardSize);
    });

    test('should switch to target mode on hit', () => {
      // Create a new game instance to manipulate internal state
      const testGame = new GameLogic(config);
      const mockShip: Ship = {
        locations: ['00', '01'],
        hits: ['', ''],
      };
      
      // Add the ship to the player's ships
      (testGame as any).state.playerShips.push(mockShip);
      
      // Force CPU to hit the ship
      let hitMade = false;
      while (!hitMade) {
        testGame.processCPUTurn();
        const newState = testGame.getGameState();
        if (newState.playerBoard.some(row => row.includes('X'))) {
          hitMade = true;
          expect(newState.cpuMode).toBe('target');
          expect(newState.cpuTargetQueue.length).toBeGreaterThan(0);
        }
      }
    });
  });

  describe('Game Over Conditions', () => {
    test('should detect when game is not over', () => {
      expect(game.isGameOver()).toBe(false);
      expect(game.getWinner()).toBeNull();
    });

    test('should detect player victory', () => {
      // Create a new game instance to manipulate internal state
      const testGame = new GameLogic(config);
      (testGame as any).state.cpuNumShips = 0;
      expect(testGame.isGameOver()).toBe(true);
      expect(testGame.getWinner()).toBe('player');
    });

    test('should detect CPU victory', () => {
      // Create a new game instance to manipulate internal state
      const testGame = new GameLogic(config);
      (testGame as any).state.playerNumShips = 0;
      expect(testGame.isGameOver()).toBe(true);
      expect(testGame.getWinner()).toBe('cpu');
    });
  });
}); 