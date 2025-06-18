# Product Search Tool

A console-based product search application that uses OpenAI's function calling to interpret natural language queries and filter products from a JSON dataset.

## Features

- **Natural Language Processing**: Accept user queries in plain English (e.g., "I need electronics under $200 with good ratings")
- **OpenAI Function Calling**: Leverages OpenAI's function calling (tools API) to extract structured filtering criteria from natural language
- **Flexible Filtering**: Supports filtering by category, price, rating, stock availability, and keywords
- **Structured Output**: Returns filtered products in a clear, formatted list
- **Modern AI Model**: Uses GPT-4.1-mini for optimal performance and cost-effectiveness

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. **Clone or download the project files** to your local machine

2. **Navigate to the task_10 directory**:
   ```bash
   cd task_10
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**:
   - Create a `.env` file in the task_10 directory
   - Add your OpenAI API key to the file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - You can copy from `env_example.txt` as a template

## Usage

1. **Run the application**:
   ```bash
   python product_search.py
   ```

2. **Enter your search query** in natural language. Examples:
   - "I need electronics under $200"
   - "Show me fitness equipment with ratings above 4.5"
   - "Find kitchen appliances that are in stock"
   - "Books under $30 with good ratings"
   - "Clothing items for men under $50"

3. **View the results** - The application will display matching products with their details

4. **Exit the application** by typing `quit`, `exit`, or `q`

## Supported Filtering Criteria

The application can understand and filter by:

- **Category**: Electronics, Fitness, Kitchen, Books, Clothing
- **Price**: Maximum price limits (e.g., "under $200", "less than $100")
- **Rating**: Minimum rating requirements (e.g., "with good ratings", "above 4.5")
- **Stock Availability**: In-stock or out-of-stock items
- **Keywords**: Specific product features or names mentioned in the query

## Example Queries

Here are some example queries you can try:

- "Show me all electronics"
- "I need a smartphone under $800"
- "Fitness equipment with ratings above 4.5"
- "Kitchen appliances that are in stock and under $100"
- "Books about programming"
- "Men's clothing under $50"
- "Wireless headphones with good ratings"

## File Structure

```
task_10/
├── product_search.py    # Main application file
├── products.json        # Product dataset
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── sample_outputs.md   # Example outputs
├── env_example.txt     # Environment variables template
└── .env                # Environment variables (create this)
```

## How It Works

1. **User Input**: The application accepts natural language queries from the user
2. **OpenAI Processing**: The query is sent to OpenAI's GPT-4.1-mini API with a tools schema
3. **Function Calling**: OpenAI analyzes the query and calls the `filter_products` function with structured parameters
4. **Product Filtering**: The application filters the product dataset based on the extracted criteria
5. **Results Display**: Matching products are displayed in a formatted list

## Technical Implementation

The application uses OpenAI's latest function calling implementation:

- **Model**: GPT-4.1-mini for optimal performance and cost
- **Tools API**: Uses the modern `tools` parameter instead of deprecated `functions`
- **Tool Choice**: Forces the model to call the `filter_products` function
- **Structured Output**: Extracts function arguments from `tool_calls` response

## Error Handling

The application includes comprehensive error handling for:
- Missing OpenAI API key
- Invalid JSON data
- API connection issues
- Invalid user input
- Function calling errors

## Troubleshooting

**"OPENAI_API_KEY not found" error**:
- Make sure you've created the `.env` file
- Ensure your API key is correctly formatted
- Verify the file is in the same directory as `product_search.py`

**"products.json file not found" error**:
- Ensure `products.json` is in the same directory as the script
- Check file permissions

**API connection errors**:
- Verify your internet connection
- Check that your OpenAI API key is valid and has sufficient credits
- Ensure you have access to GPT-4.1-mini model

**Function calling errors**:
- The application uses the latest OpenAI tools API
- Ensure you're using the latest version of the OpenAI Python client

## Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure and private
- The application only sends your search queries to OpenAI, not the product data

## Dependencies

- `openai`: Official OpenAI Python client for API communication
- `python-dotenv`: For loading environment variables from .env file

## License

This project is created for educational purposes as part of the AI Challenge 2025. 