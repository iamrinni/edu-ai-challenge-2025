#!/usr/bin/env python3
"""
Audio Analyzer - A console application that transcribes audio using OpenAI's Whisper API,
summarizes the transcription using GPT, and extracts custom analytics.
"""

import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import openai
from openai import OpenAI


class AudioAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the AudioAnalyzer with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it as parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI's Whisper API.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        print(f"Transcribing audio file: {audio_file_path}")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            print("Transcription completed successfully!")
            return transcript
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise
    
    def save_transcription(self, transcription: str, output_dir: str = "outputs") -> str:
        """
        Save transcription to a file with timestamp.
        
        Args:
            transcription: Transcribed text
            output_dir: Directory to save the file
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Save transcription
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Audio Transcription\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Transcript\n\n")
            f.write(transcription)
        
        print(f"Transcription saved to: {filepath}")
        return filepath
    
    def summarize_transcript(self, transcription: str) -> str:
        """
        Summarize the transcription using GPT.
        
        Args:
            transcription: Transcribed text
            
        Returns:
            Summary of the transcription
        """
        print("Generating summary using GPT...")
        
        prompt = f"""
        Please provide a comprehensive summary of the following audio transcription. 
        Focus on the main points, key insights, and important details.
        
        Transcription:
        {transcription}
        
        Summary:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries of audio transcriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            print("Summary generated successfully!")
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise
    
    def save_summary(self, summary: str, output_dir: str = "outputs") -> str:
        """
        Save summary to a file with timestamp.
        
        Args:
            summary: Summary text
            output_dir: Directory to save the file
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Save summary
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Audio Summary\n\n")
            f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Summary\n\n")
            f.write(summary)
        
        print(f"Summary saved to: {filepath}")
        return filepath
    
    def analyze_transcript(self, transcription: str) -> Dict[str, Any]:
        """
        Extract analytics from the transcription using GPT.
        
        Args:
            transcription: Transcribed text
            
        Returns:
            Dictionary containing analytics
        """
        print("Extracting analytics from transcript...")
        
        prompt = f"""
        Analyze the following audio transcription and extract the following analytics in JSON format:
        
        1. word_count: Total number of words in the transcription
        2. speaking_speed_wpm: Estimated speaking speed in words per minute (assume 2-3 minutes for short clips, 5-10 for longer ones)
        3. frequently_mentioned_topics: List of top 3+ frequently mentioned topics with their mention counts
        
        Return ONLY valid JSON with this exact structure:
        {{
            "word_count": <number>,
            "speaking_speed_wpm": <number>,
            "frequently_mentioned_topics": [
                {{"topic": "<topic_name>", "mentions": <count>}},
                ...
            ]
        }}
        
        Transcription:
        {transcription}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a data analyst that extracts structured analytics from text. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            analytics_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            analytics = json.loads(analytics_text)
            print("Analytics extracted successfully!")
            return analytics
            
        except Exception as e:
            print(f"Error extracting analytics: {e}")
            raise
    
    def save_analytics(self, analytics: Dict[str, Any], output_dir: str = "outputs") -> str:
        """
        Save analytics to a JSON file with timestamp.
        
        Args:
            analytics: Analytics dictionary
            output_dir: Directory to save the file
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Save analytics
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, indent=2, ensure_ascii=False)
        
        print(f"Analytics saved to: {filepath}")
        return filepath
    
    def process_audio(self, audio_file_path: str, output_dir: str = "outputs") -> Dict[str, str]:
        """
        Process audio file: transcribe, summarize, and analyze.
        
        Args:
            audio_file_path: Path to the audio file
            output_dir: Directory to save output files
            
        Returns:
            Dictionary with paths to generated files
        """
        print(f"Starting audio analysis for: {audio_file_path}")
        print("=" * 50)
        
        # Step 1: Transcribe audio
        transcription = self.transcribe_audio(audio_file_path)
        transcription_file = self.save_transcription(transcription, output_dir)
        
        # Step 2: Generate summary
        summary = self.summarize_transcript(transcription)
        summary_file = self.save_summary(summary, output_dir)
        
        # Step 3: Extract analytics
        analytics = self.analyze_transcript(transcription)
        analytics_file = self.save_analytics(analytics, output_dir)
        
        # Display results
        print("\n" + "=" * 50)
        print("ANALYSIS RESULTS")
        print("=" * 50)
        print(f"Word Count: {analytics['word_count']}")
        print(f"Speaking Speed: {analytics['speaking_speed_wpm']} WPM")
        print("\nFrequently Mentioned Topics:")
        for topic in analytics['frequently_mentioned_topics']:
            print(f"  - {topic['topic']}: {topic['mentions']} mentions")
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(summary)
        
        return {
            'transcription': transcription_file,
            'summary': summary_file,
            'analytics': analytics_file
        }


def main():
    """Main function to run the audio analyzer."""
    parser = argparse.ArgumentParser(description='Audio Analyzer - Transcribe, summarize, and analyze audio files')
    parser.add_argument('audio_file', help='Path to the audio file to analyze')
    parser.add_argument('--output-dir', default='outputs', help='Directory to save output files (default: outputs)')
    parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    
    args = parser.parse_args()
    
    # Check if audio file exists
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file '{args.audio_file}' not found.")
        return 1
    
    try:
        # Initialize analyzer
        analyzer = AudioAnalyzer(api_key=args.api_key)
        
        # Process audio
        results = analyzer.process_audio(args.audio_file, args.output_dir)
        
        print(f"\nAll files saved successfully!")
        print(f"Transcription: {results['transcription']}")
        print(f"Summary: {results['summary']}")
        print(f"Analytics: {results['analytics']}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 