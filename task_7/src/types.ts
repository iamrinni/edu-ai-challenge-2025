export type CellState = '~' | 'S' | 'X' | 'O';
export type Coordinate = `${number}${number}`;
export type Board = CellState[][];
export type CPUMode = 'hunt' | 'target';

export interface Ship {
  locations: Coordinate[];
  hits: ('hit' | '')[];
}

export interface GameConfig {
  boardSize: number;
  numShips: number;
  shipLength: number;
}

export interface GameState {
  playerBoard: Board;
  cpuBoard: Board;
  playerShips: Ship[];
  cpuShips: Ship[];
  playerNumShips: number;
  cpuNumShips: number;
  guesses: Coordinate[];
  cpuGuesses: Coordinate[];
  cpuMode: CPUMode;
  cpuTargetQueue: Coordinate[];
}

export interface Position {
  row: number;
  col: number;
} 