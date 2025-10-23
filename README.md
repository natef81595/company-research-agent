# Company Research Agent - Clay-Style Implementation

Build your own AI agents for researching company domains and extracting specific attributes, similar to Clay's Claygents.

## 🎯 What This Does

This toolkit allows you to automatically research companies by:
- Searching their domains for specific information
- Extracting products, services, certifications, and other attributes
- Processing batches of companies from CSV files
- Getting structured, reliable results

**Example Queries You Can Run:**
- "Does this company have SOC2 certification?"
- "What products and services does this company offer?"
- "Does this company offer API access?"
- "What industries does this company serve?"
- "Is this a B2B or B2C company?"

## 🏗️ Architecture

Based on how Clay built Claygents, this implementation uses:

1. **Intelligent Section Targeting**: Ask the LLM where information is likely to be found (footer, about page, etc.)
2. **Token Optimization**: Only fetch and process relevant sections of websites
3. **Binary Search Approach**: Progressively narrow down where information is located
4. **Structured Output**: Get consistent, parseable results

## 📦 Installation

### Prerequisites
- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com)

### Setup

```bash
# 1. Install dependencies
pip install anthropic requests beautifulsoup4 --break-system-packages

# 2. Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Or add to your ~/.bashrc or ~/.zshrc:
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## 🚀 Quick Start

### Option 1: Simple Agent (Basic Usage)

```python
from company_research_agent import CompanyResearchAgent

# Initialize agent
agent = CompanyResearchAgent()

# Research a single attribute
result = agent.research_attribute(
    domain="stripe.com",
    query="What products does this company offer?",
    output_format="list"
)

print(result)
```

### Option 2: Optimized Agent (Clay-like Optimizations)

```python
from optimized_research_agent import OptimizedCompanyResearchAgent

# Initialize optimized agent
agent = OptimizedCompanyResearchAgent()

# This agent will:
# 1. Analyze website structure
# 2. Ask Claude where to look
# 3. Only fetch relevant sections
# 4. Extract the answer
result = agent.research_with_optimization(
    domain="anthropic.com",
    query="Does this company have SOC2 Type II certification?",
    output_format="structured"
)

print(result)
```

### Option 3: CSV Batch Processing

```python
from csv_batch_processor import CSVBatchProcessor

# Initialize processor
processor = CSVBatchProcessor()

# Process companies from CSV
results = processor.process_csv(
    input_csv="companies.csv",
    queries=[
        "What products does this company offer?",
        "Does this company have API documentation?",
        "What industries does this company serve?"
    ],
    output_csv="results.csv"
)
```

**Your CSV should look like:**
```csv
company_name,domain
Anthropic,anthropic.com
OpenAI,openai.com
Stripe,stripe.com
```

## 📚 Usage Examples

### Example 1: Boolean Check

```python
agent = OptimizedCompanyResearchAgent()

result = agent.research_with_optimization(
    domain="stripe.com",
    query="Does this company offer enterprise pricing?",
    output_format="structured"
)

# Output structure:
{
    "domain": "stripe.com",
    "query": "Does this company offer enterprise pricing?",
    "success": true,
    "result": {
        "answer": "Yes, Stripe offers enterprise pricing",
        "confidence": "high",
        "evidence": "Quote from website...",
        "found": true
    },
    "section_searched": "pricing - based on query context"
}
```

### Example 2: List Extraction

```python
result = agent.research_with_optimization(
    domain="anthropic.com",
    query="What products and services does this company offer?",
    output_format="list"
)

# Returns a list of products/services
```

### Example 3: Batch Research Multiple Companies

```python
companies = [
    {'name': 'Anthropic', 'domain': 'anthropic.com'},
    {'name': 'OpenAI', 'domain': 'openai.com'},
    {'name': 'Stripe', 'domain': 'stripe.com'}
]

queries = [
    "What is the company's main product?",
    "Does this company have API access?",
    "Is this company B2B or B2C?"
]

results = agent.batch_research_optimized(companies, queries)

# Process all companies and queries
# Returns structured results for each combination
```

## 🎛️ Configuration Options

### Output Formats

```python
# Boolean (Yes/No/Unclear with explanation)
output_format="boolean"

# List (Bulleted list of items)
output_format="list"

# Text (Concise 2-3 sentence answer)
output_format="text"

# Structured (JSON with answer, confidence, evidence)
output_format="structured"  # Recommended
```

### Model Selection

By default uses Claude Sonnet 4 (latest). You can modify in the code:

```python
self.model = "claude-sonnet-4-20250514"  # Best balance
# self.model = "claude-opus-4-20250514"  # More powerful but slower/expensive
```

## 💡 How It Works (Clay's Approach)

### 1. Intelligent Section Targeting
Instead of sending the entire website to the LLM:
- First, analyze the website structure
- Ask Claude: "Where is SOC2 compliance info usually found?"
- Claude responds: "footer - compliance info typically in footer"
- Only fetch and process the footer section

### 2. Token Optimization
- Reduces tokens sent to LLM by 70-90%
- Faster responses
- Lower API costs

### 3. Binary Search (Optional Enhancement)
For very large pages, progressively narrow down:
- Take sections of content
- Check if target info is present
- Move to different sections if not found

## 💰 Cost Optimization

**Typical Costs (using Claude Sonnet 4):**
- Simple query: ~$0.03-0.05 per company
- Complex query: ~$0.05-0.10 per company
- Batch of 100 companies with 3 queries: ~$15-30

**Tips to Reduce Costs:**
1. Use the optimized agent (fetches less content)
2. Cache website content if researching multiple attributes
3. Use batch processing to share website fetches
4. Set content length limits appropriately

## 🔧 Advanced Customization

### Add Custom Section Detection

```python
# In optimized_research_agent.py, modify url_patterns:
url_patterns = {
    'about': ['/about', '/about-us', '/company'],
    'products': ['/products', '/solutions', '/services'],
    'pricing': ['/pricing', '/plans'],
    'security': ['/security', '/trust', '/compliance'],  # Add custom
    'careers': ['/careers', '/jobs'],  # Add custom
}
```

### Add Cross-Verification

```python
def cross_verify_result(self, domain: str, result: Dict) -> Dict:
    """Verify result by checking multiple sources"""
    # Fetch from different page
    # Compare results
    # Return confidence score
    pass
```

### Add Caching

```python
import hashlib
import pickle

def cache_website_content(self, domain: str):
    cache_key = hashlib.md5(domain.encode()).hexdigest()
    cache_file = f"/tmp/cache_{cache_key}.pkl"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # Fetch and cache...
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not found"
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Error fetching content: 403 Forbidden"
Some websites block scrapers. Solutions:
- Add user agent headers (already included)
- Use Jina AI Reader (free, already integrated as fallback)
- For production: Use services like Zenrows or Apify

### "Token limit exceeded"
Reduce content length limits in the code:
```python
return content[:15000]  # Reduce this number
```

## 📊 Comparison: This vs Clay

| Feature | This Implementation | Clay Claygents |
|---------|-------------------|----------------|
| Cost | ~$0.03-0.10 per query | Credit-based, similar |
| Customization | Full control | Limited to platform |
| Speed | Similar | Similar |
| Ease of Use | Requires coding | GUI-based |
| Scale | Unlimited | Based on plan |
| Data Sources | Web scraping + LLM | 50+ providers + LLM |

## 🚦 Next Steps

1. **Test with your companies:**
   ```bash
   python3 company_research_agent.py
   ```

2. **Try the optimized version:**
   ```bash
   python3 optimized_research_agent.py
   ```

3. **Process a CSV batch:**
   ```bash
   python3 csv_batch_processor.py
   ```

4. **Customize for your use case:**
   - Modify queries
   - Add custom section detection
   - Implement caching
   - Add your own data sources

## 🤝 Need Help?

Common use cases:
- Lead qualification
- Competitive intelligence
- Market research
- Compliance checking
- Product research

Want to add more features? Consider:
- Multi-page crawling
- Screenshot analysis
- PDF document extraction
- Integration with your CRM
- Scheduled automated runs

## 📝 License

MIT License - Use freely for commercial or personal projects.

---

**Built with inspiration from Clay's Claygents architecture**
