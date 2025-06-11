import { Game } from './Game';

// Start the game when this file is run directly
const game = new Game();
game.start().catch(console.error); 