###LLM-Powered Company Performance Metrics Query Processor
This application uses the llama-3.1-8b-instant model from Groq to process user queries related to company performance metrics and convert them into a structured JSON format. It extracts key information such as company names, performance metrics, and date ranges from natural language queries.
###Features
- Utilizes the llama-3.1-8b-instant model for natural language understanding
- Extracts company names, performance metrics, and date ranges from user queries
- Handles multiple companies and comparison requests in a single query
- Provides default date ranges when not specified in the query
- Converts extracted information into a structured JSON format
- Supports ISO 8601 date format (YYYY-MM-DD)
###Requirements
- Python 3.7+
- groq library
###Installation
Clone this repository:
```bash
git clone https://github.com/y/llm-company-metrics-processor.git
cd llm-company-metrics-processor
```
Install the required dependencies:
```bash
pip install groq
``` 
Set up your Groq API key:
Sign up for an account at https://console.groq.com/
Generate an API key in the Groq console
Set the API key as an environment variable:
```bash
export GROQ_API_KEY='your_api_key_here'
```

###Usage
Open the Jupyter notebook or Python script in your preferred environment.
Run the cells or execute the script to process example queries or modify the queries list to add your own.
The application will output the structured JSON for each query.
Example usage:
```python
queries = [
    "What was Flipkart's GMV from January 1, 2023 to December 31, 2023?",
    "Compare Amazon and Walmart's revenue for the last year",
    "Show me Apple's profit for Q2 2023"
]

for query in queries:
    print(f"Query: {query}")
    print(process_query(query))
    print()
```

###Output Format
The application outputs JSON in the following format:
```json
[
  {
    "entity": "Company Name",
    "parameter": "Performance Metric",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }
]

### Limitations and Future Improvements
The application currently assumes a simple date format. It could be extended to support more complex date parsing.
Error handling could be improved for edge cases and unexpected inputs.
The application could be extended to support more specific financial metrics and calculations.
### License
This project is licensed under the MIT License - see the LICENSE file for details.