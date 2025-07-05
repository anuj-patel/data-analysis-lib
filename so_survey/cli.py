"""
Command-line interface for the so_survey package.
"""
import sys
import click
import pandas as pd
from typing import List, Optional

from so_survey.loader import load_survey, list_excel_sheets
from so_survey.subset import filter_by_column
from so_survey.stats import describe
from so_survey.catalog import list_datasets, get_dataset_path
from so_survey.repl import start_repl


@click.group()
def cli():
    """Stack Overflow survey data analysis toolkit."""
    pass


@cli.command("repl")
def repl_command():
    """Start interactive REPL mode."""
    start_repl()


@cli.command("catalog")
@click.option("--directory", "-d", help="Directory containing dataset files")
def catalog_command(directory: Optional[str] = None):
    """List available survey datasets."""
    datasets = list_datasets(directory)
    if not datasets:
        click.echo("No datasets found.")
    else:
        click.echo("Available datasets:")
        for dataset in datasets:
            click.echo(f"  - {dataset}")


@cli.command("load")
@click.argument("dataset")
@click.option("--directory", "-d", help="Directory containing dataset files")
@click.option("--sheet", "-s", help="Sheet name or index to load from Excel file")
@click.option("--head", "-n", type=int, default=5, help="Number of rows to preview")
@click.option("--output", "-o", help="Output file path (CSV format)")
def load_command(dataset: str, directory: Optional[str] = None, sheet: Optional[str] = None, head: int = 5, output: Optional[str] = None):
    """Load a survey dataset from Excel file and optionally save or preview it."""
    # Get full path to the dataset
    file_path = get_dataset_path(dataset, directory)

    try:
        # Convert sheet parameter to appropriate type
        sheet_name = None
        if sheet:
            # Try to convert to int if it's a number, otherwise use as string
            try:
                sheet_name = int(sheet)
            except ValueError:
                sheet_name = sheet

        # Load the dataset
        df = load_survey(file_path, sheet_name=sheet_name)

        # Preview the dataset
        click.echo(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
        click.echo("\nPreview:")
        click.echo(df.head(head).to_string())

        # Print column info
        click.echo("\nColumns:")
        for col in df.columns:
            click.echo(f"  - {col} ({df[col].dtype})")

        # Save the dataset if output is specified
        if output:
            df.to_csv(output, index=False)
            click.echo(f"\nDataset saved to {output}")

    except Exception as e:
        click.echo(f"Error loading dataset: {str(e)}", err=True)
        sys.exit(1)


@cli.command("sheets")
@click.argument("dataset")
@click.option("--directory", "-d", help="Directory containing dataset files")
def sheets_command(dataset: str, directory: Optional[str] = None):
    """List all sheets in an Excel file."""
    # Get full path to the dataset
    file_path = get_dataset_path(dataset, directory)

    try:
        # List sheets in the Excel file
        sheets = list_excel_sheets(file_path)

        click.echo(f"Sheets in {dataset}:")
        for i, sheet in enumerate(sheets):
            click.echo(f"  {i}: {sheet}")

    except Exception as e:
        click.echo(f"Error reading Excel file: {str(e)}", err=True)
        sys.exit(1)


@cli.command("subset")
@click.argument("dataset")
@click.option("--directory", "-d", help="Directory containing dataset files")
@click.option("--sheet", "-s", help="Sheet name or index to load from Excel file")
@click.option("--column", "-c", required=True, help="Column to filter on")
@click.option("--values", "-v", required=True, multiple=True, help="Values to filter by (can be used multiple times)")
@click.option("--output", "-o", required=True, help="Output file path (CSV format)")
def subset_command(
    dataset: str,
    column: str,
    values: List[str],
    output: str,
    directory: Optional[str] = None,
    sheet: Optional[str] = None
):
    """Filter a dataset by column values and save the result."""
    # Get full path to the dataset
    file_path = get_dataset_path(dataset, directory)

    try:
        # Convert sheet parameter to appropriate type
        sheet_name = None
        if sheet:
            try:
                sheet_name = int(sheet)
            except ValueError:
                sheet_name = sheet

        # Load the dataset
        df = load_survey(file_path, sheet_name=sheet_name)

        # Filter the dataset
        filtered_df = filter_by_column(df, column, values)

        # Save the filtered dataset
        filtered_df.to_csv(output, index=False)

        click.echo(f"Filtered dataset saved to {output}")
        click.echo(f"Original size: {df.shape[0]} rows")
        click.echo(f"Filtered size: {filtered_df.shape[0]} rows")

    except Exception as e:
        click.echo(f"Error filtering dataset: {str(e)}", err=True)
        sys.exit(1)


@cli.command("stats")
@click.argument("dataset")
@click.option("--directory", "-d", help="Directory containing dataset files")
@click.option("--sheet", "-s", help="Sheet name or index to load from Excel file")
@click.option("--columns", "-c", multiple=True, help="Columns to include in statistics (can be used multiple times)")
def stats_command(dataset: str, directory: Optional[str] = None, sheet: Optional[str] = None, columns: Optional[List[str]] = None):
    """Calculate descriptive statistics for a dataset."""
    # Get full path to the dataset
    file_path = get_dataset_path(dataset, directory)

    try:
        # Convert sheet parameter to appropriate type
        sheet_name = None
        if sheet:
            try:
                sheet_name = int(sheet)
            except ValueError:
                sheet_name = sheet

        # Load the dataset
        df = load_survey(file_path, sheet_name=sheet_name)

        # Calculate statistics
        stats_df = describe(df, columns if columns else None)

        # Print statistics
        click.echo("Descriptive Statistics:")
        click.echo(stats_df.to_string())

    except Exception as e:
        click.echo(f"Error calculating statistics: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()