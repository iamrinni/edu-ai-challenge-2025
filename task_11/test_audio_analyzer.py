#!/usr/bin/env python3
"""
Test script for Audio Analyzer - Tests the application structure and imports
without requiring actual API calls.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import openai
        from openai import OpenAI
        print("✓ OpenAI module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import OpenAI: {e}")
        return False

def test_audio_analyzer_class():
    """Test that the AudioAnalyzer class can be instantiated."""
    try:
        # Import the class
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from audio_analyzer import AudioAnalyzer
        
        # Test instantiation (will fail without API key, but that's expected)
        try:
            analyzer = AudioAnalyzer()
            print("✓ AudioAnalyzer class instantiated successfully")
        except ValueError as e:
            if "API key is required" in str(e):
                print("✓ AudioAnalyzer class works correctly (API key validation working)")
            else:
                print(f"✗ Unexpected error: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to test AudioAnalyzer class: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    required_files = [
        'audio_analyzer.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ {file} exists")
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    return True

def test_requirements():
    """Test that requirements.txt contains necessary dependencies."""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_deps = ['openai']
        missing_deps = []
        
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)
            else:
                print(f"✓ {dep} found in requirements.txt")
        
        if missing_deps:
            print(f"✗ Missing dependencies: {missing_deps}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed to read requirements.txt: {e}")
        return False

def test_output_directory_creation():
    """Test that the output directory creation works."""
    try:
        test_dir = "test_outputs"
        
        # Import the class
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from audio_analyzer import AudioAnalyzer
        
        # Create a mock analyzer (will fail API calls but we can test file operations)
        analyzer = AudioAnalyzer(api_key="test_key")
        
        # Test directory creation
        Path(test_dir).mkdir(exist_ok=True)
        
        # Test file saving (mock data)
        test_transcription = "This is a test transcription."
        test_summary = "This is a test summary."
        test_analytics = {
            "word_count": 100,
            "speaking_speed_wpm": 120,
            "frequently_mentioned_topics": [
                {"topic": "Test Topic", "mentions": 5}
            ]
        }
        
        # Test transcription saving
        transcription_file = analyzer.save_transcription(test_transcription, test_dir)
        if os.path.exists(transcription_file):
            print("✓ Transcription file saving works")
        else:
            print("✗ Transcription file saving failed")
            return False
        
        # Test summary saving
        summary_file = analyzer.save_summary(test_summary, test_dir)
        if os.path.exists(summary_file):
            print("✓ Summary file saving works")
        else:
            print("✗ Summary file saving failed")
            return False
        
        # Test analytics saving
        analytics_file = analyzer.save_analytics(test_analytics, test_dir)
        if os.path.exists(analytics_file):
            print("✓ Analytics file saving works")
        else:
            print("✗ Analytics file saving failed")
            return False
        
        # Clean up test files
        import shutil
        shutil.rmtree(test_dir)
        print("✓ Test files cleaned up")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test file operations: {e}")
        return False

def main():
    """Run all tests."""
    print("Running Audio Analyzer Tests")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Module Imports", test_imports),
        ("AudioAnalyzer Class", test_audio_analyzer_class),
        ("File Operations", test_output_directory_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}")
        print("-" * 20)
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} test failed")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The application is ready to use.")
        print("\nTo run the application:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        print("2. Run: python audio_analyzer.py CAR0004.mp3")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 