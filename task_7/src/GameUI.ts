import * as readline from 'readline';
import { GameState } from './types';

export class GameUI {
  private rl: readline.Interface;

  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
  }

  public displayBoards(state: GameState): void {
    console.log('\n   --- OPPONENT BOARD ---          --- YOUR BOARD ---');
    
    // Print column headers
    let header = '  ';
    for (let i = 0; i < state.cpuBoard.length; i++) {
      header += i + ' ';
    }
    console.log(header + '     ' + header);

    // Print rows
    for (let i = 0; i < state.cpuBoard.length; i++) {
      let rowStr = i + ' ';
      
      // CPU board
      for (let j = 0; j < state.cpuBoard[i].length; j++) {
        rowStr += state.cpuBoard[i][j] + ' ';
      }
      
      rowStr += '    ' + i + ' ';
      
      // Player board
      for (let j = 0; j < state.playerBoard[i].length; j++) {
        rowStr += state.playerBoard[i][j] + ' ';
      }
      
      console.log(rowStr);
    }
    console.log('\n');
  }

  public async getPlayerGuess(): Promise<string> {
    return new Promise((resolve) => {
      this.rl.question('Enter your guess (e.g., 34 for row 3, column 4): ', (answer) => {
        resolve(answer.trim());
      });
    });
  }

  public displayMessage(message: string): void {
    console.log(message);
  }

  public displayGameOver(winner: 'player' | 'cpu'): void {
    console.log('\n=== GAME OVER ===');
    console.log(winner === 'player' ? 'Congratulations! You won!' : 'CPU wins! Better luck next time!');
  }

  public close(): void {
    this.rl.close();
  }
} 