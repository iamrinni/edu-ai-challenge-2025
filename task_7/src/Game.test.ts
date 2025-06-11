import { Game } from './Game';
import { GameLogic } from './GameLogic';
import { GameUI } from './GameUI';

jest.mock('./GameLogic');
jest.mock('./GameUI');

describe('Game', () => {
  let game: Game;
  let mockGameLogic: jest.Mocked<GameLogic>;
  let mockGameUI: jest.Mocked<GameUI>;

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Setup mock implementations
    (GameLogic as jest.Mock).mockImplementation(() => ({
      placeShipsRandomly: jest.fn(),
      processPlayerGuess: jest.fn(),
      processCPUTurn: jest.fn(),
      isGameOver: jest.fn().mockReturnValue(false),
      getGameState: jest.fn(),
      getWinner: jest.fn(),
    }));

    (GameUI as jest.Mock).mockImplementation(() => ({
      displayMessage: jest.fn(),
      displayBoards: jest.fn(),
      getPlayerGuess: jest.fn().mockResolvedValue('42'),
      displayGameOver: jest.fn(),
      close: jest.fn(),
    }));

    game = new Game();
    mockGameLogic = (GameLogic as unknown) as jest.Mocked<GameLogic>;
    mockGameUI = (GameUI as unknown) as jest.Mocked<GameUI>;
  });

  describe('start', () => {
    test('should initialize game correctly', async () => {
      await game.start();

      expect(mockGameUI.prototype.displayMessage).toHaveBeenCalledWith('=== SEA BATTLE ===\n');
      expect(mockGameLogic.prototype.placeShipsRandomly).toHaveBeenCalledTimes(2);
    });

    test('should handle game loop until game over', async () => {
      const mockIsGameOver = jest.fn()
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(true);
      
      (GameLogic as jest.Mock).mockImplementation(() => ({
        placeShipsRandomly: jest.fn(),
        processPlayerGuess: jest.fn().mockReturnValue(true),
        processCPUTurn: jest.fn(),
        isGameOver: mockIsGameOver,
        getGameState: jest.fn(),
        getWinner: jest.fn().mockReturnValue('player'),
      }));

      game = new Game();
      await game.start();

      expect(mockGameUI.prototype.displayBoards).toHaveBeenCalled();
      expect(mockGameUI.prototype.getPlayerGuess).toHaveBeenCalled();
      expect(mockGameUI.prototype.displayGameOver).toHaveBeenCalled();
      expect(mockGameUI.prototype.close).toHaveBeenCalled();
    });

    test('should handle invalid player guesses', async () => {
      const mockProcessPlayerGuess = jest.fn()
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(true);
      
      (GameLogic as jest.Mock).mockImplementation(() => ({
        placeShipsRandomly: jest.fn(),
        processPlayerGuess: mockProcessPlayerGuess,
        processCPUTurn: jest.fn(),
        isGameOver: jest.fn()
          .mockReturnValueOnce(false)
          .mockReturnValueOnce(true),
        getGameState: jest.fn(),
        getWinner: jest.fn(),
      }));

      (GameUI as jest.Mock).mockImplementation(() => ({
        displayMessage: jest.fn(),
        displayBoards: jest.fn(),
        getPlayerGuess: jest.fn()
          .mockResolvedValueOnce('invalid')
          .mockResolvedValueOnce('42'),
        displayGameOver: jest.fn(),
        close: jest.fn(),
      }));

      game = new Game();
      await game.start();

      expect(mockGameUI.prototype.displayMessage).toHaveBeenCalledWith('Invalid guess. Please try again.');
      expect(mockProcessPlayerGuess).toHaveBeenCalledTimes(2);
    });

    test('should handle CPU turn', async () => {
      const mockIsGameOver = jest.fn()
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(true);
      
      (GameLogic as jest.Mock).mockImplementation(() => ({
        placeShipsRandomly: jest.fn(),
        processPlayerGuess: jest.fn().mockReturnValue(true),
        processCPUTurn: jest.fn(),
        isGameOver: mockIsGameOver,
        getGameState: jest.fn(),
        getWinner: jest.fn(),
      }));

      game = new Game();
      await game.start();

      expect(mockGameUI.prototype.displayMessage).toHaveBeenCalledWith("\n--- CPU's Turn ---");
      expect(mockGameLogic.prototype.processCPUTurn).toHaveBeenCalled();
    });
  });
}); 