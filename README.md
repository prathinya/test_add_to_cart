# test_add_to_cart
# Selenium Python Automation Framework

## Tech Stack

- Python
- Selenium
- Pytest
- Page Object Model (POM)

## Features

- Page Object Model implementation
- Parameterized testing
- Logging support
- Pytest framework
- HTML Reports
- WebDriver Manager integration

## Installation

pip install -r requirements.txt

## Run Tests

pytest

## Generate HTML Report

pytest --html=Reports/report.html

## Project Structure

selenium_framework/
│
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
│
├── tests/
│   └── test_add_to_cart.py
│
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── driver_factory.py
│
├── requirements.txt
├── pytest.ini
└── README.md
