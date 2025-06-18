# Sample Outputs

This document contains example runs of the Product Search Tool for different user requests.

## Sample Run 1: Electronics Under $200

**User Input:**
```
Search query: I need electronics under $200
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: I need electronics under $200

Searching...

Filtered Products:
1. Wireless Headphones - $99.99, Rating: 4.5, In Stock
2. Smart Watch - $199.99, Rating: 4.6, In Stock
3. Bluetooth Speaker - $49.99, Rating: 4.4, In Stock
4. Gaming Mouse - $59.99, Rating: 4.3, In Stock
5. External Hard Drive - $89.99, Rating: 4.4, In Stock
6. Portable Charger - $29.99, Rating: 4.2, In Stock
```

## Sample Run 2: Fitness Equipment with High Ratings

**User Input:**
```
Search query: Show me fitness equipment with ratings above 4.5
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: Show me fitness equipment with ratings above 4.5

Searching...

Filtered Products:
1. Dumbbell Set - $149.99, Rating: 4.7, In Stock
2. Foam Roller - $24.99, Rating: 4.5, In Stock
```

## Sample Run 3: Kitchen Appliances In Stock

**User Input:**
```
Search query: Find kitchen appliances that are in stock and under $100
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: Find kitchen appliances that are in stock and under $100

Searching...

Filtered Products:
1. Blender - $49.99, Rating: 4.2, In Stock
2. Air Fryer - $89.99, Rating: 4.6, In Stock
3. Coffee Maker - $79.99, Rating: 4.3, In Stock
4. Toaster - $29.99, Rating: 4.1, In Stock
5. Electric Kettle - $39.99, Rating: 4.4, In Stock
6. Rice Cooker - $59.99, Rating: 4.3, In Stock
```

## Sample Run 4: Books About Programming

**User Input:**
```
Search query: Books about programming
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: Books about programming

Searching...

Filtered Products:
1. Programming Guide - $49.99, Rating: 4.7, In Stock
```

## Sample Run 5: Men's Clothing Under $50

**User Input:**
```
Search query: Men's clothing under $50
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: Men's clothing under $50

Searching...

Filtered Products:
1. Men's T-Shirt - $14.99, Rating: 4.2, In Stock
2. Men's Jeans - $49.99, Rating: 4.1, In Stock
3. Men's Hoodie - $34.99, Rating: 4.6, In Stock
4. Men's Socks - $9.99, Rating: 4.1, In Stock
```

## Sample Run 6: No Results Found

**User Input:**
```
Search query: Electronics over $2000
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: Electronics over $2000

Searching...

No products found matching your criteria.
```

## Sample Run 7: Complex Query with Multiple Criteria

**User Input:**
```
Search query: I need wireless headphones with good ratings that are in stock
```

**Expected Output:**
```
=== Product Search Tool ===
Enter your search query in natural language (e.g., 'I need electronics under $200')
Type 'quit' to exit

Search query: I need wireless headphones with good ratings that are in stock

Searching...

Filtered Products:
1. Wireless Headphones - $99.99, Rating: 4.5, In Stock
2. Noise-Cancelling Headphones - $299.99, Rating: 4.8, In Stock
```

## Technical Implementation Details

The application uses OpenAI's latest function calling implementation with GPT-4.1-mini:

### Function Schema
```json
{
  "type": "function",
  "function": {
    "name": "filter_products",
    "description": "Filter products based on user preferences and return matching products",
    "parameters": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "description": "Product category to filter by (Electronics, Fitness, Kitchen, Books, Clothing)",
          "enum": ["Electronics", "Fitness", "Kitchen", "Books", "Clothing"]
        },
        "max_price": {
          "type": "number",
          "description": "Maximum price limit for products"
        },
        "min_rating": {
          "type": "number",
          "description": "Minimum rating requirement (1.0 to 5.0)"
        },
        "in_stock_only": {
          "type": "boolean",
          "description": "Whether to only show products that are in stock"
        },
        "keywords": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Keywords to search for in product names"
        }
      }
    }
  }
}
```

### API Call Structure
```python
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ],
    tools=[function_schema],
    tool_choice={"type": "function", "function": {"name": "filter_products"}}
)
```

### Response Processing
The application extracts function arguments from the `tool_calls` response:
```python
if response_message.tool_calls:
    tool_call = response_message.tool_calls[0]
    if tool_call.function.name == "filter_products":
        arguments = json.loads(tool_call.function.arguments)
        filtered_products = filter_products(**arguments)
```

## Notes on Function Calling

The application uses OpenAI's modern tools API to interpret natural language queries and extract structured parameters:

- **Category filtering**: Extracts specific categories like "Electronics", "Fitness", etc.
- **Price filtering**: Understands phrases like "under $200", "less than $100", "over $500"
- **Rating filtering**: Interprets "good ratings", "above 4.5", "highly rated"
- **Stock filtering**: Recognizes "in stock", "available", "out of stock"
- **Keyword filtering**: Identifies specific product types like "wireless headphones", "programming books"

The function calling mechanism allows GPT-4.1-mini to understand context and intent, making the search experience more natural and intuitive for users while maintaining full control over the filtering logic. 