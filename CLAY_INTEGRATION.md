# Using Your Research Agent in Clay

You have **3 options** to use this agent with Clay:

## Option 1: Clay HTTP API Integration (Recommended) ✅

Deploy your agent as an API and call it from Clay on a per-row basis.

### Step 1: Deploy Your API

**Local Testing (Development):**
```bash
# Install Flask
pip install flask --break-system-packages

# Run the API server
python3 flask_api.py
```

**Production Deployment Options:**

1. **Railway.app** (Easiest, Free tier available)
   - Push code to GitHub
   - Connect Railway to your repo
   - Set `ANTHROPIC_API_KEY` environment variable
   - Deploy! You'll get a URL like `https://your-app.railway.app`

2. **Heroku**
   ```bash
   heroku create your-app-name
   heroku config:set ANTHROPIC_API_KEY=your-key
   git push heroku main
   ```

3. **Google Cloud Run / AWS Lambda / DigitalOcean**
   - Containerize with Docker
   - Deploy as serverless function

### Step 2: Add to Clay as HTTP API

In your Clay table:

1. Click **"Add Enrichment"**
2. Search for **"HTTP API"**
3. Configure:
   ```
   Method: POST
   URL: https://your-api-url.com/research
   
   Headers:
   Content-Type: application/json
   
   Body:
   {
     "domain": {{company_domain}},
     "query": "What products does this company offer?",
     "output_format": "structured"
   }
   ```

4. Map outputs:
   - `answer` → New column "Products"
   - `confidence` → New column "Confidence"
   - `evidence` → New column "Evidence"

### Step 3: Use Per-Row in Clay

Now for each row in your Clay table:
- Clay will automatically call your API with that row's domain
- Your agent researches the company
- Results populate back into Clay columns
- You can use multiple HTTP API columns with different queries!

**Example Clay Workflow:**
```
Row 1: Anthropic (anthropic.com)
  → HTTP API Call 1: "What products offered?" 
     Returns: "Claude AI assistant..."
  → HTTP API Call 2: "Does company have API?"
     Returns: "Yes, Claude API..."
  → HTTP API Call 3: "What industries served?"
     Returns: "AI research, software..."

Row 2: Stripe (stripe.com)
  → Same queries...
```

---

## Option 2: Use in Claude Code (Per-Row Processing) ✅

If you have Claude Code or want to process rows programmatically:

### Setup Claude Code Skill

Create a custom skill for Claude Code:

```python
# In your Claude Code environment
from optimized_research_agent import OptimizedCompanyResearchAgent
import pandas as pd

# Load your company list
df = pd.read_csv('companies.csv')

# Initialize agent
agent = OptimizedCompanyResearchAgent()

# Define queries
queries = [
    "What products does this company offer?",
    "Does this company have API access?",
    "What industries does this company serve?"
]

# Process each row
results = []
for idx, row in df.iterrows():
    company_results = {
        'company_name': row['name'],
        'domain': row['domain']
    }
    
    for query in queries:
        result = agent.research_with_optimization(
            domain=row['domain'],
            query=query
        )
        
        # Add to results
        query_short = query[:30]  # Short column name
        company_results[query_short] = result['result'].get('answer', 'N/A')
    
    results.append(company_results)
    print(f"✅ Processed {row['domain']}")

# Export results
results_df = pd.DataFrame(results)
results_df.to_csv('enriched_companies.csv', index=False)
```

---

## Option 3: Native Clay Integration (Most Seamless)

You can also run this **directly in Clay's Python environment** if they support custom Python:

### Using Clay's Python Formula

In Clay, you can use Python formulas. Create a custom formula:

```python
# Clay Python Formula
import requests

def research_company(domain, query):
    """Call your API from Clay formula"""
    response = requests.post(
        'https://your-api-url.com/research',
        json={
            'domain': domain,
            'query': query
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        return data.get('answer', 'N/A')
    else:
        return 'Error'

# Use in Clay:
# {{research_company(company_domain, "What products offered?")}}
```

---

## Comparison: Which Option to Use?

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **HTTP API** | • Works in Clay natively<br>• Per-row automatic<br>• Can reuse across tables | • Need to deploy API<br>• API maintenance | Production use, multiple users |
| **Claude Code** | • Full control<br>• Can modify code easily<br>• Local processing | • Manual execution<br>• Not integrated with Clay | One-time projects, experimentation |
| **Python Formula** | • Seamless in Clay<br>• No deployment needed | • Limited by Clay's Python env<br>• May not support all libraries | If Clay supports custom Python |

---

## Detailed: HTTP API Integration in Clay

### Example Clay HTTP API Setup

**Endpoint:** `POST https://your-api.com/research`

**Request Configuration in Clay:**

```json
{
  "method": "POST",
  "url": "https://your-api-url.com/research",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "domain": "{{company.domain}}",
    "query": "What products does this company offer?"
  }
}
```

**Response Mapping:**
- `response.answer` → Map to column "Products"
- `response.confidence` → Map to column "Confidence"
- `response.evidence` → Map to column "Evidence Source"

### Multiple Queries Per Company

Create multiple HTTP API enrichment columns:

**Column 1: Products**
```json
{"domain": "{{domain}}", "query": "What products offered?"}
```

**Column 2: Has API**
```json
{"domain": "{{domain}}", "query": "Does company have API?"}
```

**Column 3: Industries**
```json
{"domain": "{{domain}}", "query": "What industries served?"}
```

Clay will execute these sequentially for each row!

---

## Cost Considerations

### HTTP API Approach
- **Your costs:** Anthropic API charges (~$0.03-0.08/query)
- **Clay costs:** HTTP API calls are included in Clay credits
- **Total:** Same as running locally, just easier to use

### Claude Code Approach
- **Your costs:** Anthropic API charges only
- **No Clay credits needed** (running outside Clay)

### Recommendation
**For integration with Clay:** Use HTTP API (Option 1)
**For standalone processing:** Use Claude Code or batch script (Option 2)

---

## Example: Full Clay Workflow

```
1. Import companies to Clay table
   ├─ company_name
   ├─ domain
   └─ [empty columns for enrichment]

2. Add HTTP API enrichment columns:
   ├─ "Products" - What products offered?
   ├─ "Has_API" - Does company have API?
   ├─ "Industries" - What industries served?
   ├─ "Employee_Range" - Company size estimate?
   └─ "Funding_Status" - Recent funding info?

3. Run enrichment (automatic per row)
   Clay → Your API → Claude → Results → Back to Clay

4. Export enriched data or push to CRM
   ├─ Export to CSV
   ├─ Send to Salesforce
   └─ Trigger email sequences
```

---

## Deployment Example (Railway)

### Procfile
```
web: python3 flask_api.py
```

### runtime.txt
```
python-3.11
```

### Deploy Steps:
1. Push code to GitHub
2. Connect Railway to repo
3. Add environment variable: `ANTHROPIC_API_KEY`
4. Deploy
5. Copy API URL (e.g., `https://myapp.railway.app`)
6. Use in Clay HTTP API: `https://myapp.railway.app/research`

---

## Testing Your API

### Using curl:
```bash
curl -X POST https://your-api.com/research \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "stripe.com",
    "query": "What products does this company offer?"
  }'
```

### Expected Response:
```json
{
  "success": true,
  "answer": "Stripe offers payment processing, billing, and financial infrastructure products...",
  "confidence": "high",
  "evidence": "Found in products section",
  "found": true,
  "section_searched": "products - based on query type"
}
```

---

## Security Considerations

### API Authentication (Optional Enhancement)
```python
# Add to flask_api.py
API_KEY = os.environ.get('API_KEY', 'your-secret-key')

@app.before_request
def check_auth():
    if request.path == '/health':
        return  # Allow health checks
    
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {API_KEY}':
        return jsonify({'error': 'Unauthorized'}), 401
```

Then in Clay HTTP API config:
```
Headers:
Authorization: Bearer your-secret-key
```

---

## Rate Limiting

To avoid overwhelming your API:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["100 per hour"]
)

@app.route('/research', methods=['POST'])
@limiter.limit("20 per minute")  # 20 requests/min max
def research_company():
    # Your code...
```

---

## Next Steps

1. **For Clay integration:**
   - Deploy `flask_api.py` to Railway/Heroku
   - Add HTTP API enrichment in Clay
   - Test with a few rows
   - Scale to full table

2. **For Claude Code:**
   - Use `csv_batch_processor.py` directly
   - Process CSV locally
   - Import results back to Clay

3. **For advanced users:**
   - Add authentication
   - Implement caching
   - Add retry logic
   - Monitor with logging

---

**Bottom line:** HTTP API integration (Option 1) is the best way to use this in Clay on a per-row basis!
