# Service Analysis Tool

This console application analyzes digital services and products using OpenAI's GPT-3.5 to generate comprehensive markdown-formatted reports. The tool can analyze both known services (like Spotify or Notion) and custom service descriptions.

## Task Description

In this task, the goal is to create a lightweight console application that can accept service or product information and return a comprehensive, markdown-formatted report from multiple viewpoints—including business, technical, and user-focused perspectives.

This task simulates a real-world scenario where product managers, investors, or prospective users want quick, structured insights about a digital service. The system uses AI to extract and synthesize relevant information from provided text (like an "About Us" section) or from known service names.

The application accepts either:
- A known service name (e.g., "Spotify", "Notion")
- Raw service description text

And returns a markdown-formatted multi-section analysis report.

### Required Report Sections
1. Brief History: Founding year, milestones, etc.
2. Target Audience: Primary user segments
3. Core Features: Top 2–4 key functionalities
4. Unique Selling Points: Key differentiators
5. Business Model: How the service makes money
6. Tech Stack Insights: Any hints about technologies used
7. Perceived Strengths: Mentioned positives or standout features
8. Perceived Weaknesses: Cited drawbacks or limitations

### Requirements
- The app must include a call to OpenAI API using your API key
- The app must accept input from the console (text or known service name)
- Guide (readme.md) should contain clear and detailed instructions on how to run the application
- sample_outputs.md must include at least two sample runs of your application
- Output must be clear, properly formatted and align with all the requirements stated in task description
- OpenAI API key must not be stored in your GitHub repo!

## Features

- Accepts service names or custom service descriptions as input
- Generates comprehensive analysis reports in markdown format
- Saves reports to timestamped files
- Includes analysis of:
  - Brief History
  - Target Audience
  - Core Features
  - Unique Selling Points
  - Business Model
  - Tech Stack Insights
  - Perceived Strengths
  - Perceived Weaknesses

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

! Important note: to test the app by youself, rename .env_example to .env and put there
your valid OpenAI API key.

1. Clone the repository
2. Navigate to the task_9 directory
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the task_9 directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python service_analyzer.py
   ```

2. Enter either:
   - A service name (e.g., "Spotify", "Notion")
   - Or paste a service description text

3. Press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter to submit your input, or just press Enter for MacOS.

4. The analysis will be:
   - Displayed in the console
   - Saved to a markdown file with timestamp (e.g., `analysis_20240321_143022.md`)

5. Type 'exit' to quit the application

## Example Input

```
Spotify
```

or

```
A music streaming service that allows users to access millions of songs, podcasts, and other audio content. The service offers both free and premium subscription options, with features like offline listening, ad-free experience, and high-quality audio streaming.
```

## Output

The tool generates a markdown-formatted report with all required sections. See `sample_outputs.md` for example outputs.
The tool dumps results for each query also to a file.

## Notes

- The application requires an active internet connection to communicate with the OpenAI API
- API calls may incur costs depending on your OpenAI account settings
- Generated reports are saved in the current directory with timestamped filenames 