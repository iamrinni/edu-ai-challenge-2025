const readline = require('readline');

const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

function mod(n, m) {
  return ((n % m) + m) % m;
}

const ROTORS = [
  { wiring: 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', notch: 'Q' }, // Rotor I
  { wiring: 'AJDKSIRUXBLHWTMCQGZNPYFVOE', notch: 'E' }, // Rotor II
  { wiring: 'BDFHJLCPRTXVZNYEIWGAKMUSQO', notch: 'V' }, // Rotor III
];

// UKW-B reflector wiring
const REFLECTOR = 'YRUHQSLDPXNGOKMIEBFZCWVJAT';

function plugboardSwap(c, pairs) {
  for (const [a, b] of pairs) {
    if (c === a) return b;
    if (c === b) return a;
  }
  return c;
}

class Rotor {
  constructor(wiring, notch, ringSetting = 0, position = 0) {
    this.wiring = wiring;
    this.notch = notch;
    this.ringSetting = ringSetting;
    this.position = position;
    
    // Create reverse wiring map for backward pass
    this.reverseWiring = Array(26).fill('');
    for (let i = 0; i < 26; i++) {
      this.reverseWiring[alphabet.indexOf(this.wiring[i])] = alphabet[i];
    }
  }

  step() {
    this.position = mod(this.position + 1, 26);
  }

  atNotch() {
    return alphabet[mod(this.position, 26)] === this.notch;
  }

  forward(c) {
    // Input through position offset
    let pos = alphabet.indexOf(c);
    pos = mod(pos + this.position - this.ringSetting, 26);
    
    // Through rotor wiring
    let contact = alphabet[pos];
    contact = this.wiring[alphabet.indexOf(contact)];
    
    // Output through position offset
    pos = alphabet.indexOf(contact);
    pos = mod(pos - this.position + this.ringSetting, 26);
    
    return alphabet[pos];
  }

  backward(c) {
    // Input through position offset
    let pos = alphabet.indexOf(c);
    pos = mod(pos + this.position - this.ringSetting, 26);
    
    // Through reverse rotor wiring
    let contact = alphabet[pos];
    contact = this.reverseWiring[alphabet.indexOf(contact)];
    
    // Output through position offset
    pos = alphabet.indexOf(contact);
    pos = mod(pos - this.position + this.ringSetting, 26);
    
    return alphabet[pos];
  }
}

class Enigma {
  constructor(rotorIDs, rotorPositions, ringSettings, plugboardPairs) {
    this.rotors = rotorIDs.map(
      (id, i) =>
        new Rotor(
          ROTORS[id].wiring,
          ROTORS[id].notch,
          ringSettings[i],
          rotorPositions[i],
        ),
    );
    this.plugboardPairs = plugboardPairs;
  }

  stepRotors() {
    // Implement double-stepping mechanism
    const willMiddleRotorStep = this.rotors[1].atNotch();
    const willRightRotorStep = true; // Always steps
    
    // Middle rotor steps if it's at its notch or if right rotor is at its notch
    if (willMiddleRotorStep) {
      this.rotors[0].step(); // Left rotor steps
      this.rotors[1].step(); // Middle rotor steps
    } else if (this.rotors[2].atNotch()) {
      this.rotors[1].step(); // Middle rotor steps
    }
    
    if (willRightRotorStep) {
      this.rotors[2].step(); // Right rotor always steps
    }
  }

  encryptChar(c) {
    if (!alphabet.includes(c)) return c;
    
    this.stepRotors();
    
    // Through plugboard
    c = plugboardSwap(c, this.plugboardPairs);
    
    // Through rotors right to left
    for (let i = this.rotors.length - 1; i >= 0; i--) {
      c = this.rotors[i].forward(c);
    }
    
    // Through reflector
    c = REFLECTOR[alphabet.indexOf(c)];
    
    // Through rotors left to right
    for (let i = 0; i < this.rotors.length; i++) {
      c = this.rotors[i].backward(c);
    }
    
    // Through plugboard again
    return plugboardSwap(c, this.plugboardPairs);
  }

  process(text) {
    return text
      .toUpperCase()
      .split('')
      .map((c) => this.encryptChar(c))
      .join('');
  }
}

function promptEnigma() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter message: ', (message) => {
    rl.question('Rotor positions (e.g. 0 0 0): ', (posStr) => {
      const rotorPositions = posStr.split(' ').map(Number);
      rl.question('Ring settings (e.g. 0 0 0): ', (ringStr) => {
        const ringSettings = ringStr.split(' ').map(Number);
        rl.question('Plugboard pairs (e.g. AB CD): ', (plugStr) => {
          const plugPairs =
            plugStr
              .toUpperCase()
              .match(/([A-Z]{2})/g)
              ?.map((pair) => [pair[0], pair[1]]) || [];

          const enigma = new Enigma(
            [0, 1, 2],
            rotorPositions,
            ringSettings,
            plugPairs,
          );
          const result = enigma.process(message);
          console.log('Output:', result);
          rl.close();
        });
      });
    });
  });
}

if (require.main === module) {
  promptEnigma();
}

module.exports = { Enigma, Rotor, plugboardSwap, alphabet };
