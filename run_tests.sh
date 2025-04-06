find . -type d -name "__pycache__" -exec rm -rf {} +
export TEST_MODE=1
pytest -s --cache-clear
find . -type d -name "__pycache__" -exec rm -rf {} +