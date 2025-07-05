import pandas as pd
from typing import List, Dict, Optional, Any

class Survey:
    def __init__(self, xlsx_path: str):
        self.xlsx_path = xlsx_path
        self.df = pd.read_excel(xlsx_path)
        self.questions = list(self.df.columns)

    def display_structure(self) -> None:
        """Prints the list of questions in the survey."""
        for idx, q in enumerate(self.questions, 1):
            print(f"{idx}. {q}")

    def search_question(self, keyword: str) -> List[str]:
        """Search for questions containing the keyword."""
        return [q for q in self.questions if keyword.lower() in q.lower()]

    def search_option(self, question: str, option: str) -> List[int]:
        """Return indices of respondents who selected a given option for a question."""
        if question not in self.df.columns:
            return []
        return self.df.index[self.df[question].astype(str).str.contains(option, na=False)].tolist()

    def subset_respondents(self, question: str, option: str) -> pd.DataFrame:
        """Return a DataFrame subset of respondents who selected a given option for a question."""
        idxs = self.search_option(question, option)
        return self.df.loc[idxs]

    def answer_distribution(self, question: str, multiple_choice: bool = False) -> Dict[str, float]:
        """Return the distribution (share) of answers for a question."""
        if question not in self.df.columns:
            return {}
        if multiple_choice:
            # Split options by semicolon, flatten, and count
            all_options = self.df[question].dropna().astype(str).str.split(';')
            flat = [opt.strip() for sublist in all_options for opt in sublist]
            total = len(flat)
            counts = pd.Series(flat).value_counts()
        else:
            counts = self.df[question].value_counts(dropna=True)
            total = counts.sum()
        return {opt: cnt / total for opt, cnt in counts.items()}
