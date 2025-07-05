# Stack Overflow Survey Data Analysis Library

This library provides tools to analyze Stack Overflow Survey data from an XLSX file. It supports:
- Displaying the survey structure (list of questions)
- Searching for specific questions/options
- Creating respondent subsets based on question+option
- Displaying answer distributions for single and multiple choice questions
- CLI/REPL interface for interactive use

## Setup

1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Place your Stack Overflow survey XLSX file in the project root (e.g., `so_2024_raw.xlsx`).

## Usage

### CLI/REPL
Run the CLI/REPL interface:
```sh
python -m stack_survey.cli so_2024_raw.xlsx
```

### Library
You can also use the library in your own Python scripts:
```python
from stack_survey.survey import Survey
survey = Survey('so_2024_raw.xlsx')
survey.display_structure()
```

## Running Tests
Run all unit tests with:
```sh
python -m unittest discover tests
```

## Project Structure
- `stack_survey/` - Main library code
- `tests/` - Unit tests
- `so_2024_raw.xlsx` - Survey data file
- `requirements.txt` - Python dependencies
- `README.md` - This file
