#!/bin/bash

# Setup script for Company Research Agent

echo "=================================="
echo "Company Research Agent - Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

# Check for API key
echo ""
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Or add it to your shell config:"
    echo "  echo 'export ANTHROPIC_API_KEY=\"your-key\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
else
    echo "✅ ANTHROPIC_API_KEY is set"
    
    # Run a simple test
    echo ""
    echo "Running quick test..."
    python3 -c "
from company_research_agent import CompanyResearchAgent
import os

if os.environ.get('ANTHROPIC_API_KEY'):
    print('✅ Import successful')
    print('✅ API key configured')
    print('')
    print('You are ready to go! Try:')
    print('  python3 company_research_agent.py')
else:
    print('❌ API key not found')
"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Quick Start Commands:"
echo "  1. Basic agent:      python3 company_research_agent.py"
echo "  2. Optimized agent:  python3 optimized_research_agent.py"
echo "  3. Batch CSV:        python3 csv_batch_processor.py"
echo ""
echo "See README.md for detailed usage"
echo ""
