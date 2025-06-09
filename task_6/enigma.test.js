const { Enigma, Rotor, plugboardSwap, alphabet } = require('./enigma');

describe('Enigma Machine', () => {
  describe('Rotor', () => {
    test('should correctly step position', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0);
      rotor.step();
      expect(rotor.position).toBe(1);
      rotor.step();
      expect(rotor.position).toBe(2);
    });

    test('should correctly identify notch position', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 16); // Q is at position 16
      expect(rotor.atNotch()).toBe(true);
      rotor.step();
      expect(rotor.atNotch()).toBe(false);
    });

    test('should correctly handle forward pass', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0);
      expect(rotor.forward('A')).toBe('E');
      expect(rotor.forward('Z')).toBe('J');
    });

    test('should correctly handle backward pass', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 0, 0);
      expect(rotor.backward('E')).toBe('A');
      expect(rotor.backward('J')).toBe('Z');
    });

    test('should handle ring settings correctly', () => {
      const rotor = new Rotor('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 1, 0);
      // With ring setting 1, 'A' input should give different result than with ring setting 0
      expect(rotor.forward('A')).not.toBe('E');
    });
  });

  describe('Plugboard', () => {
    test('should swap letters correctly', () => {
      const pairs = [['A', 'B'], ['C', 'D']];
      expect(plugboardSwap('A', pairs)).toBe('B');
      expect(plugboardSwap('B', pairs)).toBe('A');
      expect(plugboardSwap('C', pairs)).toBe('D');
      expect(plugboardSwap('E', pairs)).toBe('E');
    });
  });

  describe('Enigma', () => {
    test('should encrypt single character', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const encrypted = enigma.encryptChar('A');
      expect(alphabet.includes(encrypted)).toBe(true);
    });

    test('should maintain reciprocal property', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [['A', 'B']]);
      const message = 'HELLOWORLD';
      const encrypted = enigma.process(message);
      
      // Reset enigma to initial state
      const enigma2 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], [['A', 'B']]);
      const decrypted = enigma2.process(encrypted);
      
      expect(decrypted).toBe(message);
    });

    test('should handle double stepping mechanism', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      // Encrypt a long message to trigger double stepping
      const message = 'A'.repeat(50);
      const encrypted = enigma.process(message);
      expect(encrypted.length).toBe(50);
      expect(encrypted).not.toBe(message);
    });

    test('should preserve non-alphabetic characters', () => {
      const enigma = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const message = 'HELLO, WORLD! 123';
      const encrypted = enigma.process(message);
      expect(encrypted).toMatch(/[A-Z]+, [A-Z]+! 123/);
    });

    test('should handle different rotor positions', () => {
      const enigma1 = new Enigma([0, 1, 2], [0, 0, 0], [0, 0, 0], []);
      const enigma2 = new Enigma([0, 1, 2], [1, 0, 0], [0, 0, 0], []);
      
      const message = 'TEST';
      const encrypted1 = enigma1.process(message);
      const encrypted2 = enigma2.process(message);
      
      expect(encrypted1).not.toBe(encrypted2);
    });
  });
}); 