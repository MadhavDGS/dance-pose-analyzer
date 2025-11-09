#!/bin/bash

# Simple test runner script for the project

echo "========================================="
echo "Dance Pose Analyzer - Test Suite"
echo "========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running unit tests..."
echo ""

# Run pytest with verbose output
pytest tests/ -v --tb=short

# Check test result
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "All tests passed!"
    echo "========================================="
else
    echo ""
    echo "========================================="
    echo "Some tests failed. Check output above."
    echo "========================================="
    exit 1
fi
