import { GameUI } from './GameUI';
import { GameState } from './types';
import * as readline from 'readline';

jest.mock('readline', () => ({
  createInterface: jest.fn().mockReturnValue({
    question: jest.fn(),
    close: jest.fn(),
  }),
}));

describe('GameUI', () => {
  let ui: GameUI;
  let mockConsoleLog: jest.SpyInstance;
  let mockQuestion: jest.Mock;

  beforeEach(() => {
    ui = new GameUI();
    mockConsoleLog = jest.spyOn(console, 'log').mockImplementation();
    mockQuestion = (readline.createInterface as jest.Mock)().question as jest.Mock;
  });

  afterEach(() => {
    mockConsoleLog.mockRestore();
    jest.clearAllMocks();
  });

  describe('displayBoards', () => {
    test('should display boards correctly', () => {
      const mockState: GameState = {
        playerBoard: [['~', 'S'], ['X', 'O']],
        cpuBoard: [['O', 'X'], ['~', '~']],
        playerShips: [],
        cpuShips: [],
        playerNumShips: 1,
        cpuNumShips: 1,
        guesses: [],
        cpuGuesses: [],
        cpuMode: 'hunt',
        cpuTargetQueue: [],
      };

      ui.displayBoards(mockState);

      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('OPPONENT BOARD'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('YOUR BOARD'));
    });
  });

  describe('getPlayerGuess', () => {
    test('should return trimmed player input', async () => {
      const mockInput = '  42  ';
      mockQuestion.mockImplementation((_, callback) => callback(mockInput));

      const result = await ui.getPlayerGuess();
      expect(result).toBe('42');
    });
  });

  describe('displayMessage', () => {
    test('should display message correctly', () => {
      const message = 'Test message';
      ui.displayMessage(message);
      expect(mockConsoleLog).toHaveBeenCalledWith(message);
    });
  });

  describe('displayGameOver', () => {
    test('should display player victory message', () => {
      ui.displayGameOver('player');
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Congratulations'));
    });

    test('should display CPU victory message', () => {
      ui.displayGameOver('cpu');
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('CPU wins'));
    });
  });

  describe('close', () => {
    test('should close readline interface', () => {
      const mockClose = (readline.createInterface as jest.Mock)().close;
      ui.close();
      expect(mockClose).toHaveBeenCalled();
    });
  });
}); 