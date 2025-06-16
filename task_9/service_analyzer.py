import os
import openai
from dotenv import load_dotenv
import sys
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_analysis_prompt(input_text):
    """Generate the prompt for the AI analysis."""
    return f"""Analyze the following service or product and provide a comprehensive markdown-formatted report:

{input_text}

Please structure your response as a markdown document with the following sections:
1. Brief History
2. Target Audience
3. Core Features
4. Unique Selling Points
5. Business Model
6. Tech Stack Insights
7. Perceived Strengths
8. Perceived Weaknesses

Ensure the analysis is factual and well-structured."""

def analyze_service(input_text):
    """Analyze the service using OpenAI API."""
    try:
        if not input_text.strip():
            return "Error: Empty input provided. Please enter a service name or description."
            
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional service analyst who provides detailed, structured analysis of digital services and products."},
                {"role": "user", "content": generate_analysis_prompt(input_text)}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please check your .env file."
    except openai.error.RateLimitError:
        return "Error: OpenAI API rate limit exceeded. Please try again later."
    except openai.error.APIError as e:
        return f"Error: OpenAI API error occurred: {str(e)}"
    except Exception as e:
        return f"Error analyzing service: {str(e)}"

def save_to_file(content, filename):
    """Save the analysis to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving to file: {str(e)}")
        return False

def get_user_input():
    """Get input from user with better error handling."""
    print("\nEnter your input (or 'exit' to quit):")
    try:
        # For single line input
        user_input = input().strip()
        if user_input.lower() == 'exit':
            return None
        return user_input
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None
    except Exception as e:
        print(f"Error reading input: {str(e)}")
        return None

def main():
    print("Service Analysis Tool")
    print("====================")
    print("Enter either a service name (e.g., 'Spotify', 'Notion') or paste a service description text.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = get_user_input()
        
        if user_input is None:
            break
            
        if not user_input:
            print("Please enter some text to analyze.")
            continue
            
        print("\nAnalyzing... Please wait...\n")
        analysis = analyze_service(user_input)
        
        # Print to console first
        print("\nAnalysis Results:")
        print("=" * 50)
        print(analysis)
        print("=" * 50)
        
        # Then save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.md"
        if save_to_file(analysis, filename):
            print(f"\nAnalysis has been saved to {filename}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        sys.exit(1)
    main() 