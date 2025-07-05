"""
REPL (Read-Eval-Print Loop) interface for the so_survey package.
"""
import cmd
import sys
import pandas as pd
from typing import Optional, List
import shlex

from so_survey.loader import load_survey, list_excel_sheets

class SurveyREPL(cmd.Cmd):
    """Interactive REPL for Stack Overflow survey analysis."""
    
    intro = """
Welcome to the Stack Overflow Survey Analysis REPL!
Type 'help' or '?' to list commands.
Type 'exit' or 'quit' to exit.
    """
    prompt = "so_survey> "
    
    def __init__(self):
        super().__init__()
        self.current_dataset = None
        self.current_df = None
        self.directory = None
    
    def do_catalog(self, args):
        """List available survey datasets.
        Usage: catalog [--directory DIR]
        """
        try:
            args_list = shlex.split(args) if args else []
            directory = None
            
            # Parse arguments
            i = 0
            while i < len(args_list):
                if args_list[i] in ['--directory', '-d'] and i + 1 < len(args_list):
                    directory = args_list[i + 1]
                    i += 2
                else:
                    i += 1
            
            datasets = list_datasets(directory)
            if not datasets:
                print("No datasets found.")
            else:
                print("Available datasets:")
                for dataset in datasets:
                    print(f"  - {dataset}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_load(self, args):
        """Load a survey dataset from Excel file.
        Usage: load DATASET [--directory DIR] [--sheet SHEET] [--head N]
        """
        try:
            args_list = shlex.split(args)
            if not args_list:
                print("Error: Dataset name required")
                return
            
            dataset = args_list[0]
            directory = None
            sheet_name = None
            head = 5
            
            # Parse arguments
            i = 1
            while i < len(args_list):
                if args_list[i] in ['--directory', '-d'] and i + 1 < len(args_list):
                    directory = args_list[i + 1]
                    i += 2
                elif args_list[i] in ['--sheet', '-s'] and i + 1 < len(args_list):
                    sheet_param = args_list[i + 1]
                    try:
                        sheet_name = int(sheet_param)
                    except ValueError:
                        sheet_name = sheet_param
                    i += 2
                elif args_list[i] in ['--head', '-n'] and i + 1 < len(args_list):
                    head = int(args_list[i + 1])
                    i += 2
                else:
                    i += 1
            
            # Get full path to the dataset
            file_path = get_dataset_path(dataset, directory)
            
            # Load the dataset
            df = load_survey(file_path, sheet_name=sheet_name)
            
            # Store current dataset
            self.current_dataset = dataset
            self.current_df = df
            self.directory = directory
            
            # Preview the dataset
            print(f"Loaded dataset '{dataset}' with {df.shape[0]} rows and {df.shape[1]} columns.")
            print("\nPreview:")
            print(df.head(head).to_string())
            
            # Print column info
            print("\nColumns:")
            for col in df.columns:
                print(f"  - {col} ({df[col].dtype})")
                
        except Exception as e:
            print(f"Error loading dataset: {e}")
    
    def do_sheets(self, args):
        """List all sheets in an Excel file.
        Usage: sheets DATASET [--directory DIR]
        """
        try:
            args_list = shlex.split(args)
            if not args_list:
                print("Error: Dataset name required")
                return
            
            dataset = args_list[0]
            directory = None
            
            # Parse arguments
            i = 1
            while i < len(args_list):
                if args_list[i] in ['--directory', '-d'] and i + 1 < len(args_list):
                    directory = args_list[i + 1]
                    i += 2
                else:
                    i += 1
            
            # Get full path to the dataset
            file_path = get_dataset_path(dataset, directory)
            
            # List sheets in the Excel file
            sheets = list_excel_sheets(file_path)
            
            print(f"Sheets in {dataset}:")
            for i, sheet in enumerate(sheets):
                print(f"  {i}: {sheet}")
                
        except Exception as e:
            print(f"Error reading Excel file: {e}")
    
    def do_info(self, args):
        """Show information about the currently loaded dataset."""
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        print(f"Current dataset: {self.current_dataset}")
        print(f"Shape: {self.current_df.shape[0]} rows, {self.current_df.shape[1]} columns")
        print(f"Memory usage: {self.current_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print("\nColumn types:")
        for col in self.current_df.columns:
            print(f"  - {col}: {self.current_df[col].dtype}")
    
    def do_head(self, args):
        """Show first N rows of the current dataset.
        Usage: head [N] (default: 5)
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        try:
            n = int(args) if args.strip() else 5
            print(self.current_df.head(n).to_string())
        except ValueError:
            print("Error: Invalid number")
    
    def do_tail(self, args):
        """Show last N rows of the current dataset.
        Usage: tail [N] (default: 5)
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        try:
            n = int(args) if args.strip() else 5
            print(self.current_df.tail(n).to_string())
        except ValueError:
            print("Error: Invalid number")
    
    def do_columns(self, args):
        """List all columns in the current dataset."""
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        print("Columns:")
        for i, col in enumerate(self.current_df.columns, 1):
            print(f"{i:3d}. {col}")
    
    def do_describe(self, args):
        """Show descriptive statistics for the current dataset.
        Usage: describe [COLUMN1 COLUMN2 ...]
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        try:
            columns = shlex.split(args) if args.strip() else None
            stats_df = describe(self.current_df, columns)
            print("Descriptive Statistics:")
            print(stats_df.to_string())
        except Exception as e:
            print(f"Error calculating statistics: {e}")
    
    def do_filter(self, args):
        """Filter the current dataset by column values.
        Usage: filter COLUMN VALUE1 [VALUE2 ...]
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        try:
            args_list = shlex.split(args)
            if len(args_list) < 2:
                print("Error: Column and at least one value required")
                return
            
            column = args_list[0]
            values = args_list[1:]
            
            if column not in self.current_df.columns:
                print(f"Error: Column '{column}' not found")
                return
            
            filtered_df = filter_by_column(self.current_df, column, values)
            
            print(f"Filtered dataset: {filtered_df.shape[0]} rows (from {self.current_df.shape[0]})")
            print("\nPreview of filtered data:")
            print(filtered_df.head().to_string())
            
            # Ask if user wants to replace current dataset
            response = input("\nReplace current dataset with filtered data? (y/N): ")
            if response.lower() in ['y', 'yes']:
                self.current_df = filtered_df
                print("Current dataset updated with filtered data.")
            
        except Exception as e:
            print(f"Error filtering dataset: {e}")
    
    def do_save(self, args):
        """Save the current dataset to a CSV file.
        Usage: save FILENAME
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        if not args.strip():
            print("Error: Filename required")
            return
        
        try:
            filename = args.strip()
            self.current_df.to_csv(filename, index=False)
            print(f"Dataset saved to {filename}")
        except Exception as e:
            print(f"Error saving dataset: {e}")
    
    def do_query(self, args):
        """Execute a pandas query on the current dataset.
        Usage: query "EXPRESSION"
        Example: query "Age > 25 and Country == 'United States'"
        """
        if self.current_df is None:
            print("No dataset loaded. Use 'load DATASET' first.")
            return
        
        if not args.strip():
            print("Error: Query expression required")
            return
        
        try:
            result = self.current_df.query(args)
            print(f"Query result: {result.shape[0]} rows")
            print("\nPreview:")
            print(result.head().to_string())
            
            # Ask if user wants to replace current dataset
            response = input("\nReplace current dataset with query result? (y/N): ")
            if response.lower() in ['y', 'yes']:
                self.current_df = result
                print("Current dataset updated with query result.")
                
        except Exception as e:
            print(f"Error executing query: {e}")
    
    def do_exit(self, args):
        """Exit the REPL."""
        print("Goodbye!")
        return True
    
    def do_quit(self, args):
        """Exit the REPL."""
        return self.do_exit(args)
    
    def do_EOF(self, args):
        """Handle Ctrl+D to exit."""
        print("\nGoodbye!")
        return True
    
    def emptyline(self):
        """Do nothing on empty line."""
        pass


def start_repl():
    """Start the interactive REPL."""
    try:
        SurveyREPL().cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    start_repl()