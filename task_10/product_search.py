#!/usr/bin/env python3
"""
Product Search Tool using OpenAI Function Calling

This console application allows users to search for products using natural language
queries. It leverages OpenAI's function calling to interpret user preferences and
filter products from a JSON dataset.
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductSearchTool:
    def __init__(self):
        """Initialize the product search tool with OpenAI client and products data."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Error: OPENAI_API_KEY not found in environment variables.")
            print("Please set your OpenAI API key in the .env file.")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.products = self.load_products()
        
    def load_products(self) -> List[Dict[str, Any]]:
        """Load products from the JSON file."""
        try:
            with open('products.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error: products.json file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in products.json")
            sys.exit(1)
    
    def get_filter_function_schema(self) -> Dict[str, Any]:
        """Define the function schema for OpenAI function calling."""
        return {
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
    
    def filter_products(self, category: Optional[str] = None, 
                       max_price: Optional[float] = None,
                       min_rating: Optional[float] = None,
                       in_stock_only: Optional[bool] = None,
                       keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Filter products based on the provided criteria.
        This function will be called by OpenAI with structured arguments.
        """
        filtered_products = self.products.copy()
        
        # Filter by category
        if category:
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        # Filter by maximum price
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p['price'] <= max_price]
        
        # Filter by minimum rating
        if min_rating is not None:
            filtered_products = [p for p in filtered_products if p['rating'] >= min_rating]
        
        # Filter by stock availability
        if in_stock_only is not None:
            filtered_products = [p for p in filtered_products if p['in_stock'] == in_stock_only]
        
        # Filter by keywords
        if keywords:
            keyword_filtered = []
            for product in filtered_products:
                product_name_lower = product['name'].lower()
                if any(keyword.lower() in product_name_lower for keyword in keywords):
                    keyword_filtered.append(product)
            filtered_products = keyword_filtered
        
        return filtered_products
    
    def search_products(self, user_query: str) -> List[Dict[str, Any]]:
        """
        Use OpenAI function calling to interpret user query and filter products.
        """
        try:
            # Prepare the system message with context about available products
            system_message = f"""
You are a helpful product search assistant. You have access to a dataset of {len(self.products)} products across different categories.
Your task is to understand the user's natural language query and extract relevant filtering criteria to find matching products.

Available categories: Electronics, Fitness, Kitchen, Books, Clothing
Price range: ${min(p['price'] for p in self.products):.2f} - ${max(p['price'] for p in self.products):.2f}
Rating range: {min(p['rating'] for p in self.products):.1f} - {max(p['rating'] for p in self.products):.1f}

Analyze the user's query and call the filter_products function with appropriate parameters.
If the user doesn't specify certain criteria, don't include those parameters in the function call.
"""

            # Make the API call with function calling using the new format
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_query}
                ],
                tools=[self.get_filter_function_schema()],
                tool_choice={"type": "function", "function": {"name": "filter_products"}}
            )
            
            # Extract function call arguments from the response
            response_message = response.choices[0].message
            
            # Check if there's a tool call
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                if tool_call.function.name == "filter_products":
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # Call the filter function with the extracted arguments
                    filtered_products = self.filter_products(**arguments)
                    return filtered_products
                else:
                    print("Error: Unexpected function call received from OpenAI")
                    return []
            else:
                print("Error: No tool call received from OpenAI")
                return []
                
        except Exception as e:
            print(f"Error during API call: {e}")
            return []
    
    def format_products_output(self, products: List[Dict[str, Any]]) -> str:
        """Format the filtered products for display."""
        if not products:
            return "No products found matching your criteria."
        
        output = "Filtered Products:\n"
        for i, product in enumerate(products, 1):
            stock_status = "In Stock" if product['in_stock'] else "Out of Stock"
            output += f"{i}. {product['name']} - ${product['price']:.2f}, Rating: {product['rating']}, {stock_status}\n"
        
        return output
    
    def run(self):
        """Main application loop."""
        print("=== Product Search Tool ===")
        print("Enter your search query in natural language (e.g., 'I need electronics under $200')")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("Search query: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a search query.")
                    continue
                
                print("\nSearching...")
                filtered_products = self.search_products(user_input)
                
                print("\n" + self.format_products_output(filtered_products))
                print()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.\n")

def main():
    """Main entry point of the application."""
    search_tool = ProductSearchTool()
    search_tool.run()

if __name__ == "__main__":
    main() 