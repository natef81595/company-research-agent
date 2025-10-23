#!/usr/bin/env python3
"""
CSV Batch Company Research Agent
Process multiple companies from CSV and export results
"""

import os
import csv
import json
from typing import List, Dict
from datetime import datetime
from optimized_research_agent import OptimizedCompanyResearchAgent

class CSVBatchProcessor:
    """
    Process company research queries in batch from CSV files.
    Similar to how you'd use Clay with a table of companies.
    """
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        self.agent = OptimizedCompanyResearchAgent(anthropic_api_key)
    
    def process_csv(
        self,
        input_csv: str,
        queries: List[str],
        output_csv: str = None
    ) -> List[Dict]:
        """
        Process companies from CSV file.
        
        CSV format expected:
        company_name,domain
        Anthropic,anthropic.com
        OpenAI,openai.com
        
        Args:
            input_csv: Path to input CSV with companies
            queries: List of research queries to run on each company
            output_csv: Path to output CSV (optional)
        
        Returns:
            List of research results
        """
        # Read companies from CSV
        companies = []
        with open(input_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                companies.append({
                    'name': row.get('company_name', row.get('name', 'Unknown')),
                    'domain': row['domain']
                })
        
        print(f"📋 Loaded {len(companies)} companies from {input_csv}")
        print(f"❓ Running {len(queries)} queries per company")
        print(f"🔄 Total operations: {len(companies) * len(queries)}\n")
        
        # Process each company
        results = self.agent.batch_research_optimized(companies, queries)
        
        # Export to CSV if requested
        if output_csv:
            self.export_to_csv(results, queries, output_csv)
            print(f"\n✅ Results exported to {output_csv}")
        
        return results
    
    def export_to_csv(
        self,
        results: List[Dict],
        queries: List[str],
        output_path: str
    ):
        """Export research results to CSV format."""
        
        # Prepare rows for CSV
        rows = []
        
        for company_result in results:
            row = {
                'company_name': company_result['company_name'],
                'domain': company_result['domain'],
            }
            
            # Add each query result as a column
            for query in queries:
                query_key = query[:50]  # Truncate for column name
                
                if query in company_result['attributes']:
                    result = company_result['attributes'][query]
                    
                    if result.get('success'):
                        answer_data = result.get('result', {})
                        row[f"{query_key}"] = answer_data.get('answer', 'N/A')
                        row[f"{query_key}_confidence"] = answer_data.get('confidence', 'N/A')
                    else:
                        row[f"{query_key}"] = f"ERROR: {result.get('error', 'Unknown')}"
                        row[f"{query_key}_confidence"] = 'N/A'
            
            rows.append(row)
        
        # Write to CSV
        if rows:
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
    
    def export_to_json(self, results: List[Dict], output_path: str):
        """Export full results to JSON (includes more detail than CSV)."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Detailed results exported to {output_path}")


def create_sample_csv(filename: str = "companies_sample.csv"):
    """Create a sample input CSV for testing."""
    sample_data = [
        {"company_name": "Anthropic", "domain": "anthropic.com"},
        {"company_name": "OpenAI", "domain": "openai.com"},
        {"company_name": "Stripe", "domain": "stripe.com"},
    ]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['company_name', 'domain'])
        writer.writeheader()
        writer.writerows(sample_data)
    
    print(f"✅ Created sample CSV: {filename}")
    return filename


def main():
    """Example usage of CSV batch processor."""
    
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  Please set ANTHROPIC_API_KEY environment variable")
        print("   Example: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    print("\n" + "="*80)
    print("CSV BATCH COMPANY RESEARCH")
    print("="*80 + "\n")
    
    # Create sample input CSV
    input_csv = create_sample_csv()
    
    # Define research queries
    queries = [
        "What are the main products or services offered?",
        "Does the company offer API access?",
        "What industries does this company primarily serve?",
    ]
    
    # Initialize processor
    processor = CSVBatchProcessor()
    
    # Process companies
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"research_results_{timestamp}.csv"
    output_json = f"research_results_{timestamp}.json"
    
    print("🚀 Starting batch research...\n")
    
    results = processor.process_csv(
        input_csv=input_csv,
        queries=queries,
        output_csv=output_csv
    )
    
    # Also export detailed JSON
    processor.export_to_json(results, output_json)
    
    print("\n" + "="*80)
    print("✅ BATCH PROCESSING COMPLETE")
    print("="*80)
    print(f"📊 Processed: {len(results)} companies")
    print(f"📁 CSV Output: {output_csv}")
    print(f"📁 JSON Output: {output_json}")
    print("\n")


if __name__ == "__main__":
    # Fix import issue
    import sys
    from typing import Optional
    from optimized_research_agent import OptimizedCompanyResearchAgent
    
    main()
