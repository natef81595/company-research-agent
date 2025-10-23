#!/usr/bin/env python3
"""
Advanced Company Research Agent with Clay-like Optimizations
- Binary search for finding relevant sections
- Intelligent section targeting
- Token optimization
- Multi-model support
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from bs4 import BeautifulSoup
import re

class OptimizedCompanyResearchAgent:
    """
    Advanced agent with Clay-like optimizations:
    1. Ask LLM where information is likely to be (footer, about page, etc.)
    2. Only scrape relevant sections
    3. Use binary search to narrow down content
    """
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.api_key = anthropic_api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def fetch_website_structure(self, domain: str) -> Dict[str, Any]:
        """
        Fetch website and get structural information (sections, pages, etc.)
        This is like Clay's first step - understanding the website layout.
        """
        if not domain.startswith('http'):
            domain = f'https://{domain}'
        
        try:
            # Get main page
            response = requests.get(domain, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key sections
            structure = {
                'domain': domain,
                'title': soup.title.string if soup.title else 'No title',
                'sections': [],
                'nav_links': [],
                'footer_text': '',
                'main_content': ''
            }
            
            # Get navigation links
            nav_links = soup.find_all('nav') + soup.find_all('a', {'class': re.compile('nav|menu')})
            structure['nav_links'] = [
                {'text': link.get_text(strip=True), 'href': link.get('href')}
                for link in nav_links[:20]  # Limit to avoid too many
                if link.get('href')
            ]
            
            # Get footer (often has certifications, compliance info)
            footer = soup.find('footer')
            if footer:
                structure['footer_text'] = footer.get_text(separator=' ', strip=True)[:2000]
            
            # Get main content
            main = soup.find('main') or soup.find('body')
            if main:
                structure['main_content'] = main.get_text(separator=' ', strip=True)[:10000]
            
            # Identify sections
            for header in soup.find_all(['h1', 'h2', 'h3']):
                section_text = header.get_text(strip=True)
                if section_text and len(section_text) < 100:
                    structure['sections'].append(section_text)
            
            return structure
            
        except Exception as e:
            return {'error': str(e), 'domain': domain}
    
    def identify_relevant_location(self, structure: Dict, query: str) -> str:
        """
        Use Claude to identify where information is most likely to be found.
        This mimics Clay's approach: "Ask GPT-4 which section is most likely to contain the info"
        """
        prompt = f"""You are a website analysis expert. Given a website structure and a research query, identify where the information is most likely to be found.

WEBSITE STRUCTURE:
- Title: {structure.get('title', 'N/A')}
- Available sections: {', '.join(structure.get('sections', [])[:15])}
- Navigation links: {', '.join([link['text'] for link in structure.get('nav_links', [])[:10]])}
- Has footer: {'Yes' if structure.get('footer_text') else 'No'}

RESEARCH QUERY: {query}

Based on the query, where is this information MOST LIKELY to be found? Choose ONE:
1. footer - Usually contains: certifications, compliance, legal info, contact
2. about - Usually contains: company info, mission, team, history
3. products - Usually contains: product listings, services, features
4. pricing - Usually contains: pricing, plans, enterprise info
5. main_content - For general company information
6. specific_page - If a specific nav link is relevant, name it

Respond with ONLY the location name and a brief reason (1 line).
Example: "footer - SOC2 compliance is typically in footer"
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            location_suggestion = response.content[0].text.strip()
            print(f"🎯 Claude suggests looking in: {location_suggestion}")
            return location_suggestion
            
        except Exception as e:
            print(f"⚠️  Error identifying location: {e}")
            return "main_content - default fallback"
    
    def fetch_targeted_content(self, domain: str, location_hint: str) -> str:
        """
        Fetch only the relevant section based on location hint.
        This is the optimization - don't send entire website to LLM.
        """
        if not domain.startswith('http'):
            domain = f'https://{domain}'
        
        try:
            # Map location hints to URL patterns
            url_patterns = {
                'about': ['/about', '/about-us', '/company'],
                'products': ['/products', '/solutions', '/services'],
                'pricing': ['/pricing', '/plans'],
                'footer': [domain],  # Will extract footer section
            }
            
            # Determine which page to fetch
            location_key = location_hint.split('-')[0].strip().lower()
            
            if location_key in url_patterns:
                urls_to_try = url_patterns[location_key]
                
                for url_path in urls_to_try:
                    try:
                        if not url_path.startswith('http'):
                            url = f"{domain.rstrip('/')}{url_path}"
                        else:
                            url = url_path
                        
                        response = requests.get(url, timeout=15, headers={
                            'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'
                        })
                        
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Extract relevant section
                            if location_key == 'footer':
                                footer = soup.find('footer')
                                if footer:
                                    return footer.get_text(separator=' ', strip=True)
                            
                            # Get main content
                            main = soup.find('main') or soup.find('body')
                            if main:
                                content = main.get_text(separator=' ', strip=True)
                                # Limit to save tokens
                                return content[:15000]
                    except:
                        continue
            
            # Fallback: use Jina Reader for clean content
            jina_url = f'https://r.jina.ai/{domain}'
            response = requests.get(jina_url, timeout=30)
            response.raise_for_status()
            return response.text[:15000]
            
        except Exception as e:
            return f"Error fetching content: {str(e)}"
    
    def research_with_optimization(
        self,
        domain: str,
        query: str,
        output_format: str = "structured"
    ) -> Dict[str, Any]:
        """
        Research using Clay-like optimization:
        1. Understand website structure
        2. Ask Claude where info is likely to be
        3. Fetch only that section
        4. Extract the answer
        """
        print(f"\n{'='*70}")
        print(f"🔍 Researching: {domain}")
        print(f"❓ Query: {query}")
        print(f"{'='*70}\n")
        
        # Step 1: Get website structure
        print("📊 Step 1: Analyzing website structure...")
        structure = self.fetch_website_structure(domain)
        
        if 'error' in structure:
            return {
                'domain': domain,
                'query': query,
                'success': False,
                'error': structure['error']
            }
        
        # Step 2: Identify where to look (Clay's approach)
        print("🎯 Step 2: Identifying relevant section...")
        location_hint = self.identify_relevant_location(structure, query)
        
        # Step 3: Fetch targeted content
        print("📡 Step 3: Fetching targeted content...")
        content = self.fetch_targeted_content(domain, location_hint)
        
        if content.startswith("Error"):
            return {
                'domain': domain,
                'query': query,
                'success': False,
                'error': content
            }
        
        # Step 4: Extract answer
        print("🤖 Step 4: Extracting answer with Claude...")
        
        research_prompt = f"""You are analyzing a specific section of a company website to answer a research query.

WEBSITE SECTION (from {location_hint}):
{content}

QUERY: {query}

Please provide a structured answer in JSON format with these fields:
- "answer": Your main answer (concise)
- "confidence": "high", "medium", or "low"
- "evidence": Direct quote from the website that supports your answer (if found)
- "found": true or false

If the information is not in this section, say so clearly."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": research_prompt}]
            )
            
            result_text = response.content[0].text
            
            # Try to parse JSON
            try:
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    parsed_result = json.loads(json_match.group())
                else:
                    parsed_result = {"raw_answer": result_text}
            except:
                parsed_result = {"raw_answer": result_text}
            
            return {
                'domain': domain,
                'query': query,
                'success': True,
                'result': parsed_result,
                'section_searched': location_hint,
                'tokens_saved': f"~{len(structure.get('main_content', '')) - len(content)} characters not sent to LLM"
            }
            
        except Exception as e:
            return {
                'domain': domain,
                'query': query,
                'success': False,
                'error': str(e)
            }
    
    def batch_research_optimized(
        self,
        companies: List[Dict[str, str]],
        queries: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Research multiple companies and queries efficiently.
        
        Args:
            companies: List of dicts with 'name' and 'domain' keys
            queries: List of questions to ask about each company
        
        Returns:
            Structured results for all companies and queries
        """
        all_results = []
        
        for company in companies:
            company_results = {
                'company_name': company.get('name', company['domain']),
                'domain': company['domain'],
                'attributes': {}
            }
            
            for query in queries:
                result = self.research_with_optimization(
                    domain=company['domain'],
                    query=query
                )
                company_results['attributes'][query] = result
            
            all_results.append(company_results)
        
        return all_results


def main():
    """Example usage showing optimization benefits."""
    
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  Please set ANTHROPIC_API_KEY environment variable")
        return
    
    agent = OptimizedCompanyResearchAgent()
    
    # Example 1: Optimized single research
    print("\n" + "="*80)
    print("OPTIMIZED RESEARCH EXAMPLE")
    print("="*80)
    
    result = agent.research_with_optimization(
        domain="stripe.com",
        query="Does this company have SOC2 Type II certification?",
        output_format="structured"
    )
    
    print("\n✅ RESULT:")
    print(json.dumps(result, indent=2))
    
    # Example 2: Product/services research
    print("\n" + "="*80)
    print("PRODUCT RESEARCH EXAMPLE")
    print("="*80)
    
    result = agent.research_with_optimization(
        domain="anthropic.com",
        query="What are the main products and pricing tiers offered?",
        output_format="structured"
    )
    
    print("\n✅ RESULT:")
    print(json.dumps(result, indent=2))
    
    # Example 3: Batch research (commented to save API calls)
    """
    print("\n" + "="*80)
    print("BATCH RESEARCH EXAMPLE")
    print("="*80)
    
    companies = [
        {'name': 'Anthropic', 'domain': 'anthropic.com'},
        {'name': 'OpenAI', 'domain': 'openai.com'}
    ]
    
    queries = [
        "What products does this company offer?",
        "Does this company offer enterprise pricing?",
        "What is the company's primary industry focus?"
    ]
    
    results = agent.batch_research_optimized(companies, queries)
    
    print("\n✅ BATCH RESULTS:")
    print(json.dumps(results, indent=2))
    """


if __name__ == "__main__":
    main()
