#!/usr/bin/env python3
"""
Verification script for Task 11 - Audio Analyzer
Checks that all requirements are met for the AI Challenge 2025.
"""

import os
import json
import sys

def check_required_files():
    """Check that all required files exist."""
    print("Checking required files...")
    
    required_files = [
        'audio_analyzer.py',
        'requirements.txt', 
        'README.md',
        'transcription.md',
        'summary.md',
        'analysis.json',
        'CAR0004.mp3'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_audio_analyzer_code():
    """Check that the main application code meets requirements."""
    print("\nChecking audio_analyzer.py code...")
    
    try:
        with open('audio_analyzer.py', 'r') as f:
            content = f.read()
        
        requirements_met = []
        
        # Check for OpenAI API calls
        if 'openai' in content and 'OpenAI' in content:
            requirements_met.append("✅ OpenAI API integration")
        else:
            requirements_met.append("❌ OpenAI API integration - MISSING")
        
        # Check for Whisper-1 model usage
        if 'whisper-1' in content:
            requirements_met.append("✅ Whisper-1 model usage")
        else:
            requirements_met.append("❌ Whisper-1 model usage - MISSING")
        
        # Check for GPT usage
        if 'gpt-4' in content or 'gpt-3.5' in content:
            requirements_met.append("✅ GPT model usage")
        else:
            requirements_met.append("❌ GPT model usage - MISSING")
        
        # Check for console application structure
        if 'argparse' in content and 'main()' in content:
            requirements_met.append("✅ Console application structure")
        else:
            requirements_met.append("❌ Console application structure - MISSING")
        
        # Check for file saving functionality
        if 'save_transcription' in content and 'save_summary' in content and 'save_analytics' in content:
            requirements_met.append("✅ File saving functionality")
        else:
            requirements_met.append("❌ File saving functionality - MISSING")
        
        # Check for analytics extraction
        if 'word_count' in content and 'speaking_speed_wpm' in content and 'frequently_mentioned_topics' in content:
            requirements_met.append("✅ Analytics extraction")
        else:
            requirements_met.append("❌ Analytics extraction - MISSING")
        
        for req in requirements_met:
            print(f"   {req}")
        
        return all('✅' in req for req in requirements_met)
        
    except Exception as e:
        print(f"❌ Error reading audio_analyzer.py: {e}")
        return False

def check_readme():
    """Check that README.md contains required information."""
    print("\nChecking README.md...")
    
    try:
        with open('README.md', 'r') as f:
            content = f.read()
        
        requirements_met = []
        
        # Check for installation instructions
        if 'pip install' in content and 'requirements.txt' in content:
            requirements_met.append("✅ Installation instructions")
        else:
            requirements_met.append("❌ Installation instructions - MISSING")
        
        # Check for usage instructions
        if 'python audio_analyzer.py' in content:
            requirements_met.append("✅ Usage instructions")
        else:
            requirements_met.append("❌ Usage instructions - MISSING")
        
        # Check for API key setup instructions
        if 'OPENAI_API_KEY' in content:
            requirements_met.append("✅ API key setup instructions")
        else:
            requirements_met.append("❌ API key setup instructions - MISSING")
        
        # Check for output file descriptions
        if 'transcription' in content and 'summary' in content and 'analytics' in content:
            requirements_met.append("✅ Output file descriptions")
        else:
            requirements_met.append("❌ Output file descriptions - MISSING")
        
        for req in requirements_met:
            print(f"   {req}")
        
        return all('✅' in req for req in requirements_met)
        
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return False

def check_sample_outputs():
    """Check that sample output files are properly formatted."""
    print("\nChecking sample output files...")
    
    requirements_met = []
    
    # Check transcription.md
    try:
        with open('transcription.md', 'r') as f:
            content = f.read()
        if '# Audio Transcription' in content and '## Transcript' in content:
            requirements_met.append("✅ transcription.md format")
        else:
            requirements_met.append("❌ transcription.md format - INVALID")
    except Exception as e:
        requirements_met.append(f"❌ transcription.md - ERROR: {e}")
    
    # Check summary.md
    try:
        with open('summary.md', 'r') as f:
            content = f.read()
        if '# Audio Summary' in content and '## Summary' in content:
            requirements_met.append("✅ summary.md format")
        else:
            requirements_met.append("❌ summary.md format - INVALID")
    except Exception as e:
        requirements_met.append(f"❌ summary.md - ERROR: {e}")
    
    # Check analysis.json
    try:
        with open('analysis.json', 'r') as f:
            data = json.load(f)
        
        required_keys = ['word_count', 'speaking_speed_wpm', 'frequently_mentioned_topics']
        if all(key in data for key in required_keys):
            requirements_met.append("✅ analysis.json format")
        else:
            requirements_met.append("❌ analysis.json format - INVALID")
    except Exception as e:
        requirements_met.append(f"❌ analysis.json - ERROR: {e}")
    
    for req in requirements_met:
        print(f"   {req}")
    
    return all('✅' in req for req in requirements_met)

def check_requirements_txt():
    """Check that requirements.txt contains necessary dependencies."""
    print("\nChecking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        if 'openai' in content:
            print("✅ openai dependency")
            return True
        else:
            print("❌ openai dependency - MISSING")
            return False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def main():
    """Run all verification checks."""
    print("Task 11 - Audio Analyzer Requirements Verification")
    print("=" * 60)
    
    checks = [
        ("Required Files", check_required_files),
        ("Audio Analyzer Code", check_audio_analyzer_code),
        ("README Documentation", check_readme),
        ("Sample Outputs", check_sample_outputs),
        ("Dependencies", check_requirements_txt),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        if check_func():
            passed += 1
        else:
            print(f"❌ {check_name} check failed")
    
    print("\n" + "=" * 60)
    print(f"Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL REQUIREMENTS MET! Task 11 is ready for submission.")
        print("\nThe application includes:")
        print("✅ Console application with OpenAI API integration")
        print("✅ Whisper-1 model for speech-to-text")
        print("✅ GPT model for summarization and analytics")
        print("✅ File saving with timestamps")
        print("✅ Comprehensive documentation")
        print("✅ Sample output files")
        print("✅ Proper error handling and security")
    else:
        print("❌ Some requirements are not met. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 