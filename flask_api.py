#!/usr/bin/env python3
"""
Flask API Wrapper for Clay Integration
Exposes the research agent as a REST API that Clay can call via HTTP API
"""

from flask import Flask, request, jsonify
from optimized_research_agent import OptimizedCompanyResearchAgent
import os

app = Flask(__name__)

# Initialize agent (will use ANTHROPIC_API_KEY from environment)
agent = OptimizedCompanyResearchAgent()

@app.route('/research', methods=['POST'])
def research_company():
    """
    API endpoint for Clay HTTP API integration
    
    Expected JSON body:
    {
        "domain": "anthropic.com",
        "query": "What products does this company offer?",
        "output_format": "structured"  // optional
    }
    
    Returns:
    {
        "success": true,
        "answer": "Claude AI assistant...",
        "confidence": "high",
        "evidence": "...",
        "section_searched": "products"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'domain' not in data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: domain and query'
            }), 400
        
        domain = data['domain']
        query = data['query']
        output_format = data.get('output_format', 'structured')
        
        # Run research
        result = agent.research_with_optimization(
            domain=domain,
            query=query,
            output_format=output_format
        )
        
        if result.get('success'):
            # Format for Clay - extract key fields
            response = {
                'success': True,
                'answer': result['result'].get('answer', 'N/A'),
                'confidence': result['result'].get('confidence', 'unknown'),
                'evidence': result['result'].get('evidence', ''),
                'found': result['result'].get('found', True),
                'section_searched': result.get('section_searched', 'N/A')
            }
            return jsonify(response), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/batch', methods=['POST'])
def batch_research():
    """
    Batch endpoint for multiple queries at once
    
    Expected JSON body:
    {
        "domain": "anthropic.com",
        "queries": [
            "What products does this company offer?",
            "Does this company have API access?"
        ]
    }
    
    Returns:
    {
        "success": true,
        "results": [
            {"query": "...", "answer": "...", "confidence": "..."},
            {"query": "...", "answer": "...", "confidence": "..."}
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'domain' not in data or 'queries' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: domain and queries'
            }), 400
        
        domain = data['domain']
        queries = data['queries']
        
        results = []
        for query in queries:
            result = agent.research_with_optimization(
                domain=domain,
                query=query,
                output_format='structured'
            )
            
            results.append({
                'query': query,
                'answer': result['result'].get('answer', 'N/A') if result.get('success') else 'Error',
                'confidence': result['result'].get('confidence', 'unknown') if result.get('success') else 'N/A',
                'success': result.get('success', False)
            })
        
        return jsonify({
            'success': True,
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Check for API key
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
    
    # Run server
    print("🚀 Starting API server for Clay integration...")
    print("📡 API will be available at http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /research - Single company research")
    print("  POST /batch - Batch research for one company")
    print("  GET /health - Health check")
    print("\nReady to integrate with Clay! 🎉\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
