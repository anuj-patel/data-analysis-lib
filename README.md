# Stack Overflow Survey Analysis Toolkit

[![PyPI version](https://img.shields.io/pypi/v/so_survey.svg)](https://pypi.org/project/so_survey/)
[![Build Status](https://img.shields.io/travis/so-survey/so-survey)](https://travis-ci.org/so-survey/so-survey)
[![Coverage](https://img.shields.io/codecov/c/github/so-survey/so-survey)](https://codecov.io/gh/so-survey/so-survey)
[![License](https://img.shields.io/github/license/so-survey/so-survey)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/so-survey/so-survey)](https://github.com/so-survey/so-survey)

A Python toolkit for loading, analyzing, and extracting insights from Stack  
Overflow's annual developer survey datasets. This package provides both a  
command-line interface and a programmatic API for working with survey data.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Contributing](#contributing)
- [License](#license)

## Installation

This package requires Python 3.7 or higher.

```bash
pip install so_survey
```

## Usage

The `so_survey` package provides a command-line interface for common operations:

### List available datasets

```bash
so_survey catalog
```

### Load and preview a dataset

```bash
so_survey load survey_2022 --head 10
```

### Filter a dataset by column values

```bash
so_survey subset survey_2022 --column Language --values "Python" \
  --output filtered_data.csv
```

### Calculate statistics on a dataset

```bash
so_survey stats survey_2022 --columns YearsCodePro Salary
```

## Modules

The package is organized into several modules:

- **loader.py**: Handles loading survey data from CSV files into pandas  
  DataFrames with appropriate data type inference.
- **catalog.py**: Manages dataset discovery and provides utilities for listing  
  and accessing available datasets.
- **subset.py**: Offers functionality for filtering and creating subsets of  
  survey data based on column values or ranges.
- **stats.py**: Implements statistical functions for analyzing survey data  
  including descriptive statistics.
- **cli.py**: Provides a command-line interface with commands for interacting  
  with the survey data.

## Contributing

Contributions to the Stack Overflow Survey Analysis Toolkit are welcome!

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/so-survey/so-survey.git
cd so-survey
```

1. Install development dependencies:

```bash
pip install -e ".[dev]"
```

### Development Workflow

- **Run tests**:

  ```bash
  pytest
  ```

- **Lint code**:

  ```bash
  flake8 .
  ```

- **Type checking**:

  ```bash
  mypy .
  ```

### Pull Requests

Before submitting a pull request, please ensure that:

- Your code passes all tests
- Your code passes flake8 linting
- Your code passes mypy type checking
- You've added tests for any new functionality
- You've updated documentation as needed

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details.

