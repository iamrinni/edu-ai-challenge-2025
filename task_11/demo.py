#!/usr/bin/env python3
"""
Demo script for Audio Analyzer - Shows how to use the AudioAnalyzer class programmatically.
"""

import os
import sys
from audio_analyzer import AudioAnalyzer

def demo_without_api():
    """Demo the application structure without making API calls."""
    print("Audio Analyzer Demo")
    print("=" * 40)
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  No OpenAI API key found in environment variables.")
        print("   Set OPENAI_API_KEY environment variable to run with real API calls.")
        print("   For demo purposes, we'll show the application structure.\n")
        
        # Show the structure
        print("Application Structure:")
        print("- audio_analyzer.py - Main application")
        print("- requirements.txt - Dependencies")
        print("- README.md - Documentation")
        print("- test_audio_analyzer.py - Test suite")
        print("- demo.py - This demo script")
        print("- transcription.md - Sample transcription output")
        print("- summary.md - Sample summary output")
        print("- analysis.json - Sample analytics output")
        print("- CAR0004.mp3 - Provided audio file")
        
        print("\nTo run the application:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
        print("2. Activate virtual environment: source venv/bin/activate")
        print("3. Run: python audio_analyzer.py CAR0004.mp3")
        
        return
    
    # If API key is available, show how to use the class
    print("✅ OpenAI API key found!")
    print("\nExample usage:")
    
    try:
        # Initialize analyzer
        analyzer = AudioAnalyzer(api_key=api_key)
        print("✅ AudioAnalyzer initialized successfully")
        
        # Check if audio file exists
        audio_file = "CAR0004.mp3"
        if os.path.exists(audio_file):
            print(f"✅ Audio file found: {audio_file}")
            print(f"   File size: {os.path.getsize(audio_file) / (1024*1024):.1f} MB")
            
            print("\nTo process this audio file, run:")
            print(f"python audio_analyzer.py {audio_file}")
            
        else:
            print(f"❌ Audio file not found: {audio_file}")
            
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")

def show_sample_outputs():
    """Show the sample output files."""
    print("\nSample Output Files:")
    print("=" * 40)
    
    # Show transcription sample
    if os.path.exists("transcription.md"):
        print("📄 transcription.md - Sample transcription")
        with open("transcription.md", "r") as f:
            content = f.read()
            # Show first few lines
            lines = content.split('\n')[:10]
            for line in lines:
                print(f"   {line}")
            if len(content.split('\n')) > 10:
                print("   ...")
    
    # Show summary sample
    if os.path.exists("summary.md"):
        print("\n📄 summary.md - Sample summary")
        with open("summary.md", "r") as f:
            content = f.read()
            # Show first few lines
            lines = content.split('\n')[:8]
            for line in lines:
                print(f"   {line}")
            if len(content.split('\n')) > 8:
                print("   ...")
    
    # Show analytics sample
    if os.path.exists("analysis.json"):
        print("\n📄 analysis.json - Sample analytics")
        with open("analysis.json", "r") as f:
            content = f.read()
            print(f"   {content}")

def main():
    """Main demo function."""
    demo_without_api()
    show_sample_outputs()
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    print("\nNext steps:")
    print("1. Set your OpenAI API key")
    print("2. Activate the virtual environment")
    print("3. Run the application on CAR0004.mp3")
    print("4. Check the generated output files")

if __name__ == "__main__":
    main() 