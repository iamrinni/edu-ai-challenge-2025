# Enigma Machine Implementation

This is a JavaScript implementation of the Enigma machine, a cipher device used for encryption and decryption. The implementation has been fixed to correctly handle rotor stepping, ring settings, and plugboard operations.

## Prerequisites

- Node.js (version 14 or higher)
- npm (Node Package Manager)

## Installation

1. Clone this repository or download the files
2. Open a terminal and navigate to the project directory
3. Install dependencies by running:
```bash
npm install
```

## Running the Tests

To run the test suite and see the coverage report:
```bash
npm test
```

This will run all tests and generate a coverage report showing how much of the code is tested.

## Using the Enigma Machine

You can use the Enigma machine through the command line interface:

1. Run the program:
```bash
node enigma.js
```

2. Follow the prompts:
   - Enter your message (any text, it will be converted to uppercase)
   - Enter rotor positions (three numbers from 0-25, separated by spaces)
   - Enter ring settings (three numbers from 0-25, separated by spaces)
   - Enter plugboard pairs (pairs of letters like "AB CD EF", or press Enter for none)

Example session:
```
Enter message: HELLO WORLD
Rotor positions (e.g. 0 0 0): 0 0 0
Ring settings (e.g. 0 0 0): 0 0 0
Plugboard pairs (e.g. AB CD): AB CD
```

## Understanding the Output

- The program will output the encrypted/decrypted message
- Non-alphabetic characters (spaces, punctuation, numbers) remain unchanged
- The same settings must be used for both encryption and decryption
- The machine is reciprocal - encrypting an encrypted message will decrypt it

## Example Usage

```javascript
const { Enigma } = require('./enigma');

// Create an Enigma machine with:
// - Rotors I, II, III in that order
// - Initial positions 0, 0, 0
// - Ring settings 0, 0, 0
// - Plugboard pairs A↔B and C↔D
const enigma = new Enigma(
  [0, 1, 2],           // Rotor selection
  [0, 0, 0],           // Initial positions
  [0, 0, 0],           // Ring settings
  [['A', 'B'], ['C', 'D']]  // Plugboard pairs
);

// Encrypt a message
const encrypted = enigma.process('HELLO WORLD');
console.log(encrypted);  // Will output encrypted text

// Create a new machine with the same settings to decrypt
const enigma2 = new Enigma(
  [0, 1, 2],
  [0, 0, 0],
  [0, 0, 0],
  [['A', 'B'], ['C', 'D']]
);

// Decrypt the message
const decrypted = enigma2.process(encrypted);
console.log(decrypted);  // Will output 'HELLO WORLD'
```

## Files in this Project

- `enigma.js` - The main Enigma machine implementation
- `enigma.test.js` - Comprehensive test suite
- `fix.md` - Detailed explanation of the bugs and fixes
- `README.md` - This file
- `package.json` - Project configuration and dependencies
