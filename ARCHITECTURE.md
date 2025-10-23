# Architecture Diagram - Company Research Agent

## How Clay Built Claygents (Simplified Flow)

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLAY'S CLAYGENT SYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

                              INPUT
                                │
                                ▼
                   ┌────────────────────────┐
                   │   User Query + Domain  │
                   │  "Does stripe.com have │
                   │   SOC2 certification?" │
                   └────────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  STEP 1: Strategic Planning   │
                │  GPT-4 Tool Calling           │
                │  "Where is this info likely?" │
                │  → "footer or security page"  │
                └───────────────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  STEP 2: Targeted Scraping    │
                │  Only fetch footer section     │
                │  Binary search if needed       │
                │  Token savings: ~75%           │
                └───────────────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  STEP 3: Data Extraction      │
                │  GPT-4 extracts answer         │
                │  Structured JSON output        │
                │  Confidence scoring            │
                └───────────────────────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │  STEP 4: Verification         │
                │  Cross-check with other        │
                │  data providers (50+ sources)  │
                │  Validate accuracy             │
                └───────────────────────────────┘
                                │
                                ▼
                              OUTPUT
                                │
                                ▼
                   ┌────────────────────────┐
                   │   Structured Result    │
                   │   Answer: "Yes"        │
                   │   Confidence: "high"   │
                   │   Evidence: "..."      │
                   └────────────────────────┘
```

## Your DIY Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│                 YOUR OPTIMIZED AGENT SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘

                              INPUT
                                │
                                ▼
                   ┌────────────────────────┐
                   │  Query + Domain        │
                   └────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │  STEP 1: Website Structure Analysis      │
        │  • Fetch homepage                         │
        │  • Extract navigation links               │
        │  • Identify main sections                 │
        │  • Detect footer, about, products         │
        └──────────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │  STEP 2: Intelligent Location Detection  │
        │  Claude Analyzes:                        │
        │  • Query type                             │
        │  • Available sections                     │
        │  • Returns: "footer - compliance info"    │
        └──────────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │  STEP 3: Targeted Content Fetch          │
        │  Options:                                │
        │  • Scrape specific section                │
        │  • Use Jina AI Reader (clean content)     │
        │  • Fetch sub-page if needed               │
        │  Token savings: 60-80%                    │
        └──────────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │  STEP 4: Claude Extraction               │
        │  • Analyze content                        │
        │  • Extract specific answer                │
        │  • Provide confidence score               │
        │  • Include evidence/quotes                │
        └──────────────────────────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────┐
        │  STEP 5: Format Output                   │
        │  • JSON structure                         │
        │  • CSV export (batch mode)                │
        │  • Error handling                         │
        └──────────────────────────────────────────┘
                                │
                                ▼
                              OUTPUT
```

## Comparison: Simple vs Optimized Approach

### ❌ Naive Approach (Don't do this)
```
Fetch entire website → Send 100KB to LLM → Get answer
Cost: $0.30 per query
Speed: 45 seconds
Accuracy: Medium (too much noise)
```

### ✅ Optimized Approach (Clay's way)
```
Analyze structure → Identify section → Fetch 15KB → Get answer
Cost: $0.05 per query
Speed: 15 seconds  
Accuracy: High (focused search)
```

## Data Flow Diagram

```
┌──────────────┐
│  Input CSV   │
│  companies   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  For each domain │
└──────┬───────────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────┐   ┌──────────┐
│ Query 1  │   │ Query 2  │
│ Research │   │ Research │
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  Combine      │
    │  Results      │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  Export to    │
    │  CSV / JSON   │
    └───────────────┘
```

## System Components

```
┌─────────────────────────────────────────────────────────┐
│                    COMPONENT STACK                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────┐         │
│  │         Application Layer                  │         │
│  │  • company_research_agent.py              │         │
│  │  • optimized_research_agent.py            │         │
│  │  • csv_batch_processor.py                 │         │
│  └────────────────────────────────────────────┘         │
│                        ↕                                 │
│  ┌────────────────────────────────────────────┐         │
│  │           AI/LLM Layer                     │         │
│  │  • Anthropic Claude API                    │         │
│  │  • Prompt engineering                      │         │
│  │  • Structured output parsing               │         │
│  └────────────────────────────────────────────┘         │
│                        ↕                                 │
│  ┌────────────────────────────────────────────┐         │
│  │        Content Extraction Layer            │         │
│  │  • BeautifulSoup (HTML parsing)            │         │
│  │  • Jina AI Reader (content cleaning)       │         │
│  │  • Requests (HTTP client)                  │         │
│  └────────────────────────────────────────────┘         │
│                        ↕                                 │
│  ┌────────────────────────────────────────────┐         │
│  │           Data Layer                       │         │
│  │  • CSV input/output                        │         │
│  │  • JSON export                             │         │
│  │  • Result caching (optional)               │         │
│  └────────────────────────────────────────────┘         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Token Optimization Strategy

### Without Optimization
```
Website: 100,000 characters
        ↓
    Send all to LLM
        ↓
Input tokens: ~25,000
Cost: $0.08 per query
```

### With Optimization (Clay's approach)
```
Website: 100,000 characters
        ↓
Identify relevant section (500 chars)
        ↓
Fetch only that section: 15,000 characters
        ↓
Input tokens: ~4,000
Cost: $0.01 per query

Savings: 87.5%! 💰
```

## Binary Search Illustration

```
For very large websites:

Initial Content: [████████████████████████████] 100%
                              ↓
                    Does answer exist here?
                              ↓
         ┌────────────────────┴────────────────────┐
         NO                                        YES
         ↓                                          ↓
    [████████]                              [████████████]
    Check this half                      Found! Extract answer
         ↓
    Still too large?
         ↓
    [████]  [████]
    Continue splitting...

Result: Find info with 3-4 checks instead of reading entire site
```

## Processing Pipeline

```
Single Company Research:
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Fetch  │→│Analyze │→│Extract │→│ Format │
│ Site   │  │Content │  │ Answer │  │Output  │
└────────┘  └────────┘  └────────┘  └────────┘
   2s          5s          8s          1s
                                    
Total: ~15 seconds per query

Batch Processing (100 companies, 3 queries each):
┌────────────────────────────────────────┐
│  Company 1  │  Query 1, 2, 3  │  45s   │
│  Company 2  │  Query 1, 2, 3  │  45s   │
│     ...     │      ...        │  ...   │
│  Company 100│  Query 1, 2, 3  │  45s   │
└────────────────────────────────────────┘

Total: ~75 minutes for 300 total queries
Cost: ~$15-25
```

## Error Handling Flow

```
                    ┌──────────┐
                    │  Query   │
                    └────┬─────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Try Fetch      │
                │  Website        │
                └────┬─────┬──────┘
                     │     │
                  SUCCESS  FAIL
                     │     │
                     │     └────→ Use Jina AI
                     │                │
                     │                ▼
                     │         ┌──────────────┐
                     │         │ Retry with   │
                     │         │ Clean Content│
                     │         └──────┬───────┘
                     │                │
                     ▼                ▼
              ┌──────────────────────────┐
              │   Extract with Claude    │
              └─────────┬──────────┬─────┘
                        │          │
                     SUCCESS     FAIL
                        │          │
                        │          └─→ Return error with
                        │              partial results
                        ▼
                 ┌────────────┐
                 │   Return   │
                 │   Result   │
                 └────────────┘
```

## Scaling Architecture

```
Basic (< 100 companies/day):
┌─────────────┐
│ Single      │
│ Python      │→ Claude API
│ Process     │
└─────────────┘

Medium (100-1000 companies/day):
┌─────────────┐
│ Parallel    │→ Claude API
│ Workers     │
│ (3-5)       │→ Claude API
└─────────────┘

Large (1000+ companies/day):
┌─────────────┐
│ Queue       │
│ System      │→ Worker Pool → Claude API
│ (Redis/     │   (10-20)
│  RabbitMQ)  │
└─────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────┐
│         Your Company Research            │
│              Agent System                │
└───────────────┬─────────────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐  ┌────────┐  ┌────────┐
│  CRM   │  │ Slack  │  │ Email  │
│(Salesforce, HubSpot, Sheets)  │
└────────┘  └────────┘  └────────┘
```

---

This diagram shows the complete architecture of how Clay built Claygents and how you can build your own optimized version!
