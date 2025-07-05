import sys
from stack_survey.survey import Survey

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m stack_survey.cli <survey_xlsx>")
        sys.exit(1)
    survey = Survey(sys.argv[1])
    print("Stack Overflow Survey CLI. Type 'help' for commands.")
    while True:
        cmd = input("survey> ").strip()
        if cmd in ("exit", "quit"): break
        elif cmd == "help":
            print("""
Commands:
  structure                - Display survey structure (questions)
  searchq <keyword>        - Search for question by keyword
  searcho <q> <option>     - Search for respondents by question+option
  subset <q> <option>      - Display subset of respondents
  dist <q> [MC]            - Show answer distribution (add MC for multi-choice)
  exit/quit                - Exit
""")
        elif cmd == "structure":
            survey.display_structure()
        elif cmd.startswith("searchq "):
            _, keyword = cmd.split(" ", 1)
            results = survey.search_question(keyword)
            for q in results:
                print(q)
        elif cmd.startswith("searcho "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: searcho <question> <option>")
                continue
            _, q, opt = parts
            idxs = survey.search_option(q, opt)
            print(f"Respondent indices: {idxs}")
        elif cmd.startswith("subset "):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Usage: subset <question> <option>")
                continue
            _, q, opt = parts
            df = survey.subset_respondents(q, opt)
            print(df)
        elif cmd.startswith("dist "):
            parts = cmd.split()
            if len(parts) < 2:
                print("Usage: dist <question> [MC]")
                continue
            q = parts[1]
            mc = len(parts) > 2 and parts[2].upper() == "MC"
            dist = survey.answer_distribution(q, multiple_choice=mc)
            for opt, share in dist.items():
                print(f"{opt}: {share:.2%}")
        else:
            print("Unknown command. Type 'help' for commands.")

if __name__ == "__main__":
    main()
