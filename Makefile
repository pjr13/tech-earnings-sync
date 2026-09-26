.PHONY: test lint clean run

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	python3 -m tech_earnings_sync.cli --help
