import { GameLogic } from './GameLogic';
import { GameUI } from './GameUI';

export class Game {
  private logic: GameLogic;
  private ui: GameUI;

  constructor() {
    this.logic = new GameLogic();
    this.ui = new GameUI();
  }

  public async start(): Promise<void> {
    this.ui.displayMessage('=== SEA BATTLE ===\n');
    this.ui.displayMessage('Setting up the game...');

    // Place ships
    this.logic.placeShipsRandomly(true);
    this.logic.placeShipsRandomly(false);
    this.ui.displayMessage('Ships placed. Game starting!\n');

    await this.gameLoop();
  }

  private async gameLoop(): Promise<void> {
    while (!this.logic.isGameOver()) {
      // Display game state
      this.ui.displayBoards(this.logic.getGameState());

      // Player's turn
      let validGuess = false;
      while (!validGuess) {
        const guess = await this.ui.getPlayerGuess();
        validGuess = this.logic.processPlayerGuess(guess);
        if (!validGuess) {
          this.ui.displayMessage('Invalid guess. Please try again.');
        }
      }

      // Check if game is over after player's turn
      if (this.logic.isGameOver()) break;

      // CPU's turn
      this.ui.displayMessage("\n--- CPU's Turn ---");
      const cpuMove = this.logic.processCPUTurn();
      
      // Display CPU move result
      const [row, col] = [cpuMove.coordinate[0], cpuMove.coordinate[1]];
      this.ui.displayMessage(`CPU fires at ${row},${col}: ${cpuMove.isHit ? 'HIT!' : 'Miss'}`);
      if (cpuMove.isSunk) {
        this.ui.displayMessage('CPU sunk one of your ships!');
      }
      this.ui.displayMessage(''); // Empty line for better readability
    }

    // Game over
    this.ui.displayBoards(this.logic.getGameState());
    const winner = this.logic.getWinner();
    if (winner) {
      this.ui.displayGameOver(winner);
    }
    this.ui.close();
  }
}

// Start the game if this file is run directly
if (require.main === module) {
  const game = new Game();
  game.start().catch(console.error);
} 