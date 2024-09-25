 lint:
     pylint your_module.py
     mypy your_module.py
     flake8 your_module.py
     isort your_module.py --check-only

 .PHONY: lint