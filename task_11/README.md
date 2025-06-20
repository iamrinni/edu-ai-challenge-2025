# Audio Analyzer

A console application that transcribes audio using OpenAI's Whisper API, summarizes the transcription using GPT, and extracts custom analytics.

## Features

- **Speech-to-Text**: Transcribe audio files using OpenAI's Whisper-1 model
- **Text Summarization**: Generate comprehensive summaries using GPT-4
- **Analytics Extraction**: Extract word count, speaking speed, and frequently mentioned topics
- **File Management**: Automatically save transcriptions, summaries, and analytics with timestamps
- **Multi-format Support**: Works with various audio file formats supported by Whisper

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- Internet connection for API calls

## Installation

1. **Clone or download the project files**

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**
   
   **Option 1: Environment Variable (Recommended)**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Option 2: Pass as parameter when running the script**
   ```bash
   python audio_analyzer.py audio_file.mp3 --api-key "your-api-key-here"
   ```

## Usage

### Basic Usage

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the analyzer
python audio_analyzer.py path/to/your/audio/file.mp3
```

### Advanced Usage

```bash
# Specify custom output directory
python audio_analyzer.py audio_file.mp3 --output-dir my_outputs

# Pass API key as parameter
python audio_analyzer.py audio_file.mp3 --api-key "your-api-key-here"

# Combine options
python audio_analyzer.py audio_file.mp3 --output-dir custom_outputs --api-key "your-api-key-here"
```

### Command Line Arguments

- `audio_file`: Path to the audio file to analyze (required)
- `--output-dir`: Directory to save output files (default: "outputs")
- `--api-key`: OpenAI API key (optional if set as environment variable)

## Output Files

The application generates three types of output files, each with a timestamp:

1. **Transcription File** (`transcription_YYYYMMDD_HHMMSS.md`)
   - Complete transcript of the audio
   - Formatted in Markdown with metadata

2. **Summary File** (`summary_YYYYMMDD_HHMMSS.md`)
   - Concise summary of the main points
   - Formatted in Markdown with metadata

3. **Analytics File** (`analysis_YYYYMMDD_HHMMSS.json`)
   - Structured JSON containing:
     - Word count
     - Speaking speed (words per minute)
     - Frequently mentioned topics with mention counts

## Sample Output Files

This repository includes sample output files for the provided `CAR0004.mp3` audio file:

- `transcription.md` - Sample transcription output
- `summary.md` - Sample summary output  
- `analysis.json` - Sample analytics output

These files demonstrate the expected format and structure of the application's output.

## Example Output

### Console Output
```
Starting audio analysis for: CAR0004.mp3
==================================================
Transcribing audio file: CAR0004.mp3
Transcription completed successfully!
Transcription saved to: outputs/transcription_20241201_143022.md
Generating summary using GPT...
Summary generated successfully!
Summary saved to: outputs/summary_20241201_143022.md
Extracting analytics from transcript...
Analytics extracted successfully!
Analytics saved to: outputs/analysis_20241201_143022.json

==================================================
ANALYSIS RESULTS
==================================================
Word Count: 1280
Speaking Speed: 132 WPM

Frequently Mentioned Topics:
  - Customer Onboarding: 6 mentions
  - Q4 Roadmap: 4 mentions
  - AI Integration: 3 mentions

==================================================
SUMMARY
==================================================
[Summary content here]

All files saved successfully!
Transcription: outputs/transcription_20241201_143022.md
Summary: outputs/summary_20241201_143022.md
Analytics: outputs/analysis_20241201_143022.json
```

### Analytics JSON Example
```json
{
  "word_count": 1280,
  "speaking_speed_wpm": 132,
  "frequently_mentioned_topics": [
    {"topic": "Customer Onboarding", "mentions": 6},
    {"topic": "Q4 Roadmap", "mentions": 4},
    {"topic": "AI Integration", "mentions": 3}
  ]
}
```

## Testing

Run the test script to verify the application setup:

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python test_audio_analyzer.py
```

The test script will verify:
- File structure
- Dependencies installation
- Module imports
- Class functionality
- File operations

## Supported Audio Formats

The application supports all audio formats that OpenAI's Whisper API supports, including:
- MP3
- MP4
- Mpeg
- MPGA
- M4A
- WAV
- WebM

## Error Handling

The application includes comprehensive error handling for:
- Missing audio files
- Invalid API keys
- Network connectivity issues
- API rate limits
- File permission issues

## Security Notes

- **Never commit your API key to version control**
- Use environment variables for API keys in production
- The application does not store API keys in any files
- All API calls are made securely over HTTPS

## Troubleshooting

### Common Issues

1. **"OpenAI API key is required" error**
   - Set the OPENAI_API_KEY environment variable
   - Or pass the API key using the --api-key parameter

2. **"Audio file not found" error**
   - Check the file path is correct
   - Ensure the file exists and is readable

3. **"Error transcribing audio" error**
   - Check your internet connection
   - Verify your API key is valid
   - Ensure the audio file is in a supported format

4. **Permission denied errors**
   - Check file permissions for the audio file
   - Ensure write permissions for the output directory

5. **"externally-managed-environment" error**
   - Use a virtual environment as described in the installation section
   - Don't install packages globally on macOS

### Getting Help

If you encounter issues:
1. Check the error messages for specific details
2. Verify your API key is valid and has sufficient credits
3. Ensure the audio file is not corrupted
4. Check your internet connection
5. Make sure you're using a virtual environment

## API Usage and Costs

- **Whisper API**: Charged per minute of audio processed
- **GPT-4 API**: Charged per token used for summarization and analytics
- Monitor your OpenAI usage dashboard for cost tracking

## License

This project is created for educational purposes as part of the AI Challenge 2025.