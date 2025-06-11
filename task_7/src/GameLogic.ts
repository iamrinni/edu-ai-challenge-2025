import { Board, CellState, Coordinate, GameConfig, GameState, Position, Ship } from './types';

export class GameLogic {
  private state: GameState;
  private config: GameConfig;

  constructor(config: GameConfig = { boardSize: 10, numShips: 3, shipLength: 3 }) {
    this.config = config;
    this.state = this.initializeGameState();
  }

  private initializeGameState(): GameState {
    const playerBoard = this.createEmptyBoard();
    const cpuBoard = this.createEmptyBoard();

    return {
      playerBoard,
      cpuBoard,
      playerShips: [],
      cpuShips: [],
      playerNumShips: this.config.numShips,
      cpuNumShips: this.config.numShips,
      guesses: [],
      cpuGuesses: [],
      cpuMode: 'hunt',
      cpuTargetQueue: [],
    };
  }

  private createEmptyBoard(): Board {
    return Array(this.config.boardSize)
      .fill(null)
      .map(() => Array(this.config.boardSize).fill('~' as CellState));
  }

  public placeShipsRandomly(isPlayer: boolean): void {
    const board = isPlayer ? this.state.playerBoard : this.state.cpuBoard;
    const ships = isPlayer ? this.state.playerShips : this.state.cpuShips;
    let placedShips = 0;

    while (placedShips < this.config.numShips) {
      const orientation = Math.random() < 0.5 ? 'horizontal' : 'vertical';
      const startPos = this.getRandomStartPosition(orientation);
      const shipLocations = this.calculateShipLocations(startPos, orientation);

      if (this.isValidPlacement(shipLocations, board)) {
        const newShip: Ship = {
          locations: shipLocations,
          hits: Array(this.config.shipLength).fill(''),
        };

        if (isPlayer) {
          shipLocations.forEach(loc => {
            const [row, col] = this.coordinateToPosition(loc);
            board[row][col] = 'S';
          });
        }

        ships.push(newShip);
        placedShips++;
      }
    }
  }

  private getRandomStartPosition(orientation: 'horizontal' | 'vertical'): Position {
    const maxRow = orientation === 'horizontal' ? this.config.boardSize : this.config.boardSize - this.config.shipLength + 1;
    const maxCol = orientation === 'horizontal' ? this.config.boardSize - this.config.shipLength + 1 : this.config.boardSize;

    return {
      row: Math.floor(Math.random() * maxRow),
      col: Math.floor(Math.random() * maxCol),
    };
  }

  private calculateShipLocations(startPos: Position, orientation: 'horizontal' | 'vertical'): Coordinate[] {
    const locations: Coordinate[] = [];
    for (let i = 0; i < this.config.shipLength; i++) {
      const row = orientation === 'horizontal' ? startPos.row : startPos.row + i;
      const col = orientation === 'horizontal' ? startPos.col + i : startPos.col;
      locations.push(`${row}${col}` as Coordinate);
    }
    return locations;
  }

  private isValidPlacement(locations: Coordinate[], board: Board): boolean {
    return locations.every(loc => {
      const [row, col] = this.coordinateToPosition(loc);
      return row < this.config.boardSize && col < this.config.boardSize && board[row][col] === '~';
    });
  }

  public processPlayerGuess(guess: string): boolean {
    if (!this.isValidGuess(guess)) {
      return false;
    }

    const coordinate = guess as Coordinate;
    if (this.state.guesses.includes(coordinate)) {
      return false;
    }

    this.state.guesses.push(coordinate);
    const [row, col] = this.coordinateToPosition(coordinate);
    const hitResult = this.processHit(coordinate, this.state.cpuShips, this.state.cpuBoard, row, col);

    if (hitResult.isHit) {
      if (hitResult.isSunk) {
        this.state.cpuNumShips--;
      }
    } else {
      this.state.cpuBoard[row][col] = 'O';
    }

    return true;
  }

  public processCPUTurn(): void {
    let guess: Coordinate;
    let isValidGuess = false;

    while (!isValidGuess) {
      if (this.state.cpuMode === 'target' && this.state.cpuTargetQueue.length > 0) {
        guess = this.state.cpuTargetQueue.shift()!;
      } else {
        guess = this.getRandomGuess();
        this.state.cpuMode = 'hunt';
      }

      if (!this.state.cpuGuesses.includes(guess)) {
        isValidGuess = true;
        this.state.cpuGuesses.push(guess);
        const [row, col] = this.coordinateToPosition(guess);
        const hitResult = this.processHit(guess, this.state.playerShips, this.state.playerBoard, row, col);

        if (hitResult.isHit) {
          if (hitResult.isSunk) {
            this.state.playerNumShips--;
            this.state.cpuMode = 'hunt';
            this.state.cpuTargetQueue = [];
          } else {
            this.state.cpuMode = 'target';
            this.addAdjacentPositions(row, col);
          }
        }
      }
    }
  }

  private processHit(
    coordinate: Coordinate,
    ships: Ship[],
    board: Board,
    row: number,
    col: number
  ): { isHit: boolean; isSunk: boolean } {
    for (const ship of ships) {
      const index = ship.locations.indexOf(coordinate);
      if (index >= 0) {
        if (ship.hits[index] !== 'hit') {
          ship.hits[index] = 'hit';
          board[row][col] = 'X';
          return { isHit: true, isSunk: this.isSunk(ship) };
        }
        return { isHit: true, isSunk: false };
      }
    }
    return { isHit: false, isSunk: false };
  }

  private addAdjacentPositions(row: number, col: number): void {
    const adjacent: Position[] = [
      { row: row - 1, col },
      { row: row + 1, col },
      { row, col: col - 1 },
      { row, col: col + 1 },
    ];

    adjacent
      .filter(pos => this.isValidPosition(pos))
      .forEach(pos => {
        const coord = `${pos.row}${pos.col}` as Coordinate;
        if (!this.state.cpuGuesses.includes(coord)) {
          this.state.cpuTargetQueue.push(coord);
        }
      });
  }

  private isValidPosition(pos: Position): boolean {
    return pos.row >= 0 && pos.row < this.config.boardSize && pos.col >= 0 && pos.col < this.config.boardSize;
  }

  private getRandomGuess(): Coordinate {
    let row: number, col: number;
    do {
      row = Math.floor(Math.random() * this.config.boardSize);
      col = Math.floor(Math.random() * this.config.boardSize);
    } while (this.state.cpuGuesses.includes(`${row}${col}` as Coordinate));
    return `${row}${col}` as Coordinate;
  }

  private isSunk(ship: Ship): boolean {
    return ship.hits.every(hit => hit === 'hit');
  }

  private isValidGuess(guess: string): boolean {
    if (guess.length !== 2) return false;
    const [row, col] = this.coordinateToPosition(guess as Coordinate);
    return this.isValidPosition({ row, col });
  }

  private coordinateToPosition(coordinate: Coordinate): [number, number] {
    return [parseInt(coordinate[0]), parseInt(coordinate[1])];
  }

  public getGameState(): Readonly<GameState> {
    return { ...this.state };
  }

  public isGameOver(): boolean {
    return this.state.playerNumShips === 0 || this.state.cpuNumShips === 0;
  }

  public getWinner(): 'player' | 'cpu' | null {
    if (!this.isGameOver()) return null;
    return this.state.playerNumShips === 0 ? 'cpu' : 'player';
  }
} 