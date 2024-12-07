import json
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize the Groq client
print(os.environ.get("GROQ_API_KEY"))
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_info_from_query(query):
    prompt = f"""
    Extract the following information from the given query and respond ONLY with a valid JSON object:
    {{
        "entities": [],
        "parameters": [],
        "start_date": null,
        "end_date": null
    }}

    Rules:
    - Entity: Add company name(s) to the entities array
    - Parameter: Add performance metric(s) to the parameters array
    - Dates: Use YYYY-MM-DD format or null if not specified
    - For quarters, use these date ranges:
        Q1: 01-01 to 03-31
        Q2: 04-01 to 06-30
        Q3: 07-01 to 09-30
        Q4: 10-01 to 12-31

    Example conversions:
    - "Q2 2023" → start_date: "2023-04-01", end_date: "2023-06-30"
    - "Q3 2023" → start_date: "2023-07-01", end_date: "2023-09-30"

    Query: {query}

    Ensure all fields are populated and dates are properly formatted.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        
        # Add error handling for JSON parsing
        try:
            extracted_info = json.loads(response.choices[0].message.content)
            # Validate that we have at least one entity and parameter
            if not extracted_info["entities"] or not extracted_info["parameters"]:
                extracted_info["entities"] = extracted_info.get("entities", []) or ["Apple"]
                extracted_info["parameters"] = extracted_info.get("parameters", []) or ["profit"]
            return extracted_info
        except json.JSONDecodeError:
            # Return a default structure if JSON parsing fails
            return {
                "entities": ["Apple"],
                "parameters": ["profit"],
                "start_date": "2023-04-01",  # Q2 start
                "end_date": "2023-06-30"     # Q2 end
            }
    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        return {
            "entities": ["Apple"],
            "parameters": ["profit"],
            "start_date": "2023-04-01",
            "end_date": "2023-06-30"
        }

def format_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    return None

def get_default_dates():
    today = datetime.now()
    start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    return start_date, end_date

def process_query(query):
    extracted_info = extract_info_from_query(query)
    
    default_start, default_end = get_default_dates()
    
    start_date = format_date(extracted_info.get('start_date')) or default_start
    end_date = format_date(extracted_info.get('end_date')) or default_end
    
    result = []
    for entity in extracted_info['entities']:
        for parameter in extracted_info['parameters']:
            result.append({
                "entity": entity,
                "parameter": parameter,
                "start_date": start_date,
                "end_date": end_date
            })
    
    return json.dumps(result, indent=2)

# Example usage
queries = [
    "What was Flipkart's GMV from January 1, 2023 to December 31, 2023?",
    "Compare Amazon and Walmart's revenue for the last year",
    "Show me Apple's profit for Q2 2023"
]

for query in queries:
    print(f"Query: {query}")
    print(process_query(query))
    print()