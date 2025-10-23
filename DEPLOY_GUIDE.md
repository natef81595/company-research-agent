# 🚀 Quick Deploy Guide - Use Your Agent in Clay

## TL;DR - 3 Ways to Use This

1. **✅ HTTP API in Clay** (Recommended) - Deploy as API, use in Clay per-row
2. **✅ Claude Code** - Process CSV batches programmatically  
3. **⚡ Python Script** - Run locally, import results to Clay

---

## Option 1: Deploy API for Clay Integration (5 minutes)

### Deploy to Railway (Easiest, Free Tier)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Company research agent"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub"
   - Select your repo
   - Add environment variable:
     - Key: `ANTHROPIC_API_KEY`
     - Value: `your-api-key-here`
   - Deploy!
   - Copy your URL: `https://yourapp.railway.app`

3. **Test Your API**
   ```bash
   curl -X POST https://yourapp.railway.app/research \
     -H "Content-Type: application/json" \
     -d '{"domain": "stripe.com", "query": "What products offered?"}'
   ```

4. **Add to Clay**
   - In Clay table, click "Add Enrichment"
   - Select "HTTP API"
   - Configure:
     ```
     Method: POST
     URL: https://yourapp.railway.app/research
     Body: {
       "domain": {{company_domain}},
       "query": "What products does this company offer?"
     }
     ```
   - Map outputs to columns
   - Run on all rows! 🎉

### Deploy to Other Platforms

**Heroku:**
```bash
heroku create myapp
heroku config:set ANTHROPIC_API_KEY=your-key
git push heroku main
```

**Google Cloud Run:**
```bash
gcloud run deploy --source . --set-env-vars ANTHROPIC_API_KEY=your-key
```

**Docker (Any Platform):**
```bash
docker build -t research-agent .
docker run -p 5000:5000 -e ANTHROPIC_API_KEY=your-key research-agent
```

---

## Option 2: Use in Claude Code

If you have Claude for Code or want to process locally:

```python
from csv_batch_processor import CSVBatchProcessor

# Process your Clay export
processor = CSVBatchProcessor()

results = processor.process_csv(
    input_csv="clay_export.csv",  # Export from Clay
    queries=[
        "What products does this company offer?",
        "Does this company have API access?",
        "What industries does this company serve?"
    ],
    output_csv="enriched_results.csv"
)

# Import enriched_results.csv back to Clay
```

---

## Option 3: Local Processing + Import

**Step 1: Export from Clay**
- Export your companies table as CSV

**Step 2: Process Locally**
```bash
python3 csv_batch_processor.py
```

**Step 3: Import Back to Clay**
- Import the results CSV
- Merge with original table

---

## Clay HTTP API Configuration Examples

### Single Query per Company

**URL:** `https://your-api.railway.app/research`

**Body:**
```json
{
  "domain": "{{company.domain}}",
  "query": "What products does this company offer?",
  "output_format": "structured"
}
```

**Response Mapping:**
- `answer` → Column "Products"
- `confidence` → Column "Confidence"
- `evidence` → Column "Source"

### Multiple Queries (Add Multiple Columns)

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

**Column 4: Pricing**
```json
{"domain": "{{domain}}", "query": "What is pricing model?"}
```

### Batch Endpoint (Multiple Queries at Once)

**URL:** `https://your-api.railway.app/batch`

**Body:**
```json
{
  "domain": "{{company.domain}}",
  "queries": [
    "What products offered?",
    "Does company have API?",
    "What industries served?"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {"query": "...", "answer": "...", "confidence": "high"},
    {"query": "...", "answer": "...", "confidence": "high"},
    {"query": "...", "answer": "...", "confidence": "medium"}
  ]
}
```

---

## Cost Comparison

### Running 1000 Companies × 3 Queries = 3000 Total Queries

**Your DIY API:**
- API hosting: $0-5/month (Railway free tier or $5)
- Claude API: ~$90-240 (3000 × $0.03-0.08)
- **Total: $90-245**

**Clay Claygents:**
- Platform fee: $149-800/month
- Credits for 3000 queries: ~$50-150
- **Total: $199-950**

**Break-even point:** ~2000 queries/month

---

## Monitoring Your API

### Check Health
```bash
curl https://yourapp.railway.app/health
```

### View Logs (Railway)
- Go to Railway dashboard
- Click on your deployment
- View logs in real-time

### Add Monitoring (Optional)
```python
# In flask_api.py
import logging

logging.basicConfig(
    filename='api.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/research', methods=['POST'])
def research_company():
    logging.info(f"Request: {request.get_json()}")
    # ... your code
    logging.info(f"Response: {response}")
```

---

## Troubleshooting

### API Returns 500 Error
- Check Railway logs for error details
- Verify ANTHROPIC_API_KEY is set
- Test locally first: `python3 flask_api.py`

### Clay Can't Connect to API
- Verify API URL is correct
- Check API is running: `curl https://yourapp.railway.app/health`
- Ensure request body format is correct

### Slow Responses
- Normal: 10-30 seconds per query
- If slower, check your internet/API connectivity
- Consider adding timeout in Clay HTTP API settings

### Rate Limits
- Anthropic API: 50 requests/minute by default
- Add rate limiting to your API if needed (see CLAY_INTEGRATION.md)

---

## Production Best Practices

### 1. Add Authentication
```python
# Protect your API with a secret key
API_KEY = os.environ.get('API_SECRET_KEY')

@app.before_request
def check_auth():
    if request.headers.get('Authorization') != f'Bearer {API_KEY}':
        return jsonify({'error': 'Unauthorized'}), 401
```

In Clay:
```
Headers:
Authorization: Bearer your-secret-key
```

### 2. Add Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def fetch_and_cache(domain):
    return fetch_website_content(domain)
```

### 3. Add Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def research_with_retry(domain, query):
    return agent.research_with_optimization(domain, query)
```

### 4. Monitor Costs
```python
# Track API usage
import json

@app.route('/research', methods=['POST'])
def research_company():
    # ... your code
    
    # Log usage
    with open('usage.log', 'a') as f:
        f.write(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'estimated_cost': 0.05  # Update based on actual
        }) + '\n')
```

---

## Example: Complete Clay Workflow

```
┌─────────────────────────────────────────┐
│  1. Build List of Companies in Clay    │
│     - Import from CSV                   │
│     - Or use Clay's Find Companies      │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  2. Add HTTP API Enrichment Columns     │
│     - Column A: Products offered        │
│     - Column B: Has API?                │
│     - Column C: Industries served       │
│     - Column D: Company size            │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  3. Run Enrichment                      │
│     - Clay calls your API per row       │
│     - Your API calls Claude             │
│     - Results populate columns          │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  4. Use Enriched Data                   │
│     - Filter/score leads               │
│     - Export to CRM                     │
│     - Trigger email sequences           │
│     - Build reports                     │
└─────────────────────────────────────────┘
```

---

## Files You Need

**For API Deployment:**
- ✅ `flask_api.py` - API server
- ✅ `optimized_research_agent.py` - Agent logic
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Railway/Heroku config
- ✅ `Dockerfile` - Docker deployment (optional)

**For Local Processing:**
- ✅ `csv_batch_processor.py` - Batch processor
- ✅ `optimized_research_agent.py` - Agent logic
- ✅ `requirements.txt` - Dependencies

---

## Quick Commands

**Test Locally:**
```bash
python3 flask_api.py
# In another terminal:
curl -X POST http://localhost:5000/research \
  -H "Content-Type: application/json" \
  -d '{"domain": "stripe.com", "query": "What products?"}'
```

**Deploy to Railway:**
```bash
railway link
railway up
railway open
```

**Check Status:**
```bash
curl https://yourapp.railway.app/health
```

---

## Next Steps

1. ✅ Deploy your API (5 minutes)
2. ✅ Test with curl (1 minute)
3. ✅ Add to Clay as HTTP API (3 minutes)
4. ✅ Test on 5-10 rows first
5. ✅ Scale to full table
6. 🎉 Enjoy automated company research!

---

**Questions? Check:**
- `CLAY_INTEGRATION.md` - Detailed integration guide
- `README.md` - Complete documentation
- `EXAMPLES.md` - Real output examples

You're ready to use your agent in Clay! 🚀
