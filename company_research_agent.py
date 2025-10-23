#!/usr/bin/env python3
"""
Company Research Agent
Searches company domains for specific attributes using Claude + web scraping
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from anthropic import Anthropic

class CompanyResearchAgent:
    """
    An agent that researches company domains to find specific attributes.
    Similar to Clay's Claygent but focused on company attribute extraction.
    """
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        """
        Initialize the research agent.
        
        Args:
            anthropic_api_key: Your Anthropic API key. If None, will use ANTHROPIC_API_KEY env var
        """
        self.api_key = anthropic_api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY env var or pass it directly.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude model
        
    def fetch_website_content(self, domain: str) -> str:
        """
        Fetch and convert website content to LLM-friendly format.
        Uses Jina AI Reader (free) to convert HTML to clean markdown.
        
        Args:
            domain: Company domain (e.g., "anthropic.com" or "https://anthropic.com")
            
        Returns:
            Clean text content from the website
        """
        # Ensure domain has protocol
        if not domain.startswith('http'):
            domain = f'https://{domain}'
        
        # Use Jina AI Reader to get clean content
        jina_url = f'https://r.jina.ai/{domain}'
        
        try:
            response = requests.get(jina_url, timeout=30)
            response.raise_for_status()
            content = response.text
            
            # Truncate if too long (to save tokens)
            # Keep first 100k characters - adjust based on your needs
            if len(content) > 100000:
                content = content[:100000] + "\n\n[Content truncated due to length...]"
            
            return content
        except Exception as e:
            return f"Error fetching content: {str(e)}"
    
    def research_attribute(
        self, 
        domain: str, 
        query: str,
        output_format: str = "text"
    ) -> Dict[str, Any]:
        """
        Research a specific attribute about a company.
        
        Args:
            domain: Company domain to research
            query: What you want to know (e.g., "Does this company have SOC2 compliance?")
            output_format: "text", "boolean", "list", or "structured"
            
        Returns:
            Dictionary with research results
        """
        # Fetch website content
        print(f"📡 Fetching content from {domain}...")
        website_content = self.fetch_website_content(domain)
        
        if website_content.startswith("Error"):
            return {
                "domain": domain,
                "query": query,
                "success": False,
                "error": website_content
            }
        
        # Construct prompt for Claude
        prompt = self._build_research_prompt(query, output_format)
        
        print(f"🤖 Analyzing content with Claude...")
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"""{prompt}

WEBSITE CONTENT:
{website_content}

RESEARCH QUERY: {query}

Please analyze the website content and answer the query."""
                    }
                ]
            )
            
            result = response.content[0].text
            
            # Parse result based on output format
            parsed_result = self._parse_result(result, output_format)
            
            return {
                "domain": domain,
                "query": query,
                "success": True,
                "result": parsed_result,
                "raw_response": result
            }
            
        except Exception as e:
            return {
                "domain": domain,
                "query": query,
                "success": False,
                "error": str(e)
            }
    
    def batch_research(
        self,
        domains: List[str],
        queries: List[str],
        output_format: str = "structured"
    ) -> List[Dict[str, Any]]:
        """
        Research multiple attributes across multiple domains.
        
        Args:
            domains: List of company domains
            queries: List of queries to ask about each domain
            output_format: Format for results
            
        Returns:
            List of research results
        """
        results = []
        
        for domain in domains:
            domain_results = {
                "domain": domain,
                "attributes": {}
            }
            
            for query in queries:
                print(f"\n{'='*60}")
                print(f"Researching: {domain}")
                print(f"Query: {query}")
                print(f"{'='*60}\n")
                
                result = self.research_attribute(domain, query, output_format)
                domain_results["attributes"][query] = result
            
            results.append(domain_results)
        
        return results
    
    def _build_research_prompt(self, query: str, output_format: str) -> str:
        """Build the research prompt for Claude based on output format."""
        
        base_prompt = """You are a company research analyst. Your job is to carefully read website content and extract specific information.

IMPORTANT INSTRUCTIONS:
1. Only use information explicitly stated on the website
2. If the information is not found, say "Not found on website"
3. Be precise and cite specific sections when possible
4. If uncertain, indicate your confidence level"""

        format_instructions = {
            "boolean": "\n\nOUTPUT FORMAT: Answer with 'Yes', 'No', or 'Unclear' followed by a brief explanation.",
            "list": "\n\nOUTPUT FORMAT: Provide a bulleted list of items. If nothing found, say 'None found'.",
            "text": "\n\nOUTPUT FORMAT: Provide a concise text answer (2-3 sentences max).",
            "structured": "\n\nOUTPUT FORMAT: Return a JSON object with keys: 'answer', 'confidence' (high/medium/low), 'evidence' (quote from website)"
        }
        
        return base_prompt + format_instructions.get(output_format, format_instructions["text"])
    
    def _parse_result(self, result: str, output_format: str) -> Any:
        """Parse Claude's response based on expected format."""
        
        if output_format == "structured":
            try:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
        
        # For other formats, return as-is
        return result


def main():
    """Example usage of the Company Research Agent."""
    
    # Check if API key is set
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  Please set your ANTHROPIC_API_KEY environment variable")
        print("   Example: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Initialize agent
    agent = CompanyResearchAgent()
    
    # Example 1: Single attribute research
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Attribute Research")
    print("="*80)
    
    result = agent.research_attribute(
        domain="anthropic.com",
        query="What products and services does this company offer?",
        output_format="list"
    )
    
    print(f"\n✅ Result:")
    print(json.dumps(result, indent=2))
    
    # Example 2: Boolean check
    print("\n" + "="*80)
    print("EXAMPLE 2: Boolean Attribute Check")
    print("="*80)
    
    result = agent.research_attribute(
        domain="stripe.com",
        query="Does this company offer API documentation?",
        output_format="boolean"
    )
    
    print(f"\n✅ Result:")
    print(json.dumps(result, indent=2))
    
    # Example 3: Structured output
    print("\n" + "="*80)
    print("EXAMPLE 3: Structured Output")
    print("="*80)
    
    result = agent.research_attribute(
        domain="openai.com",
        query="What is the company's main product?",
        output_format="structured"
    )
    
    print(f"\n✅ Result:")
    print(json.dumps(result, indent=2))
    
    # Example 4: Batch research (commented out to avoid too many API calls)
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Batch Research")
    print("="*80)
    
    results = agent.batch_research(
        domains=["anthropic.com", "openai.com"],
        queries=[
            "What products does this company offer?",
            "Does this company have enterprise pricing?",
            "What industries does this company serve?"
        ],
        output_format="text"
    )
    
    print(f"\n✅ Batch Results:")
    print(json.dumps(results, indent=2))
    """


if __name__ == "__main__":
    main()
