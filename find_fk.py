from dataclasses import dataclass
from pathlib import Path
from typing import List

import click
import polars as pl
from rich.console import Console
from rich.table import Table


@dataclass
class FKCandidate:
    """Represents a potential foreign key relationship between columns"""
    child_table: str
    child_column: str
    parent_table: str
    parent_column: str
    match_percent: float
    sample_matches: List[tuple]
    child_nulls_percent: float

def find_fk_relationships(child_path, parent_path, min_match_percent=0.1, max_samples=5):
    """lower threshold based on entity case"""
    df_child = pl.read_csv(child_path)
    df_parent = pl.read_csv(parent_path)
    candidates = []
    for child_col in df_child.columns:
        child_series = df_child[child_col]
        # handle empty strings as nulls
        child_values = set(
            str(v) for v in child_series.drop_nulls()
            if str(v).strip() != ""
        )
        if not child_values:
            continue
        child_null_percent = (
            (child_series.is_null() | (child_series.cast(pl.Utf8) == ""))
            .mean() * 100
        )
        for parent_col in df_parent.columns:
            parent_series = df_parent[parent_col]
            # Convert both to strings for comparison
            parent_values = set(
                str(v) for v in parent_series.drop_nulls()
                if str(v).strip() != ""
            )
            if not parent_values:
                continue
            # Find matches
            matches = child_values.intersection(parent_values)
            match_percent = len(matches) / len(child_values) * 100
            if match_percent >= min_match_percent:
                # get some sample matching values
                sample_pairs = []
                for val in list(matches)[:max_samples]:
                    child_row = df_child.filter(
                        pl.col(child_col).cast(pl.Utf8) == str(val)
                    ).head(1)
                    parent_row = df_parent.filter(
                        pl.col(parent_col).cast(pl.Utf8) == str(val)
                    ).head(1)
                    if not child_row.is_empty() and not parent_row.is_empty():
                        sample_pairs.append((val, val))
                candidates.append(FKCandidate(
                    child_table=child_path.name,
                    child_column=child_col,
                    parent_table=parent_path.name,
                    parent_column=parent_col,
                    match_percent=match_percent,
                    sample_matches=sample_pairs,
                    child_nulls_percent=child_null_percent
                ))
    return sorted(candidates, key=lambda x: x.match_percent, reverse=True)

@click.command()
@click.argument('tbl1', type=click.Path(exists=True))
@click.argument('tbl2', type=click.Path(exists=True))
@click.option('--min-match', default=10.0, help='Minimum match percentage')
def main(tbl1: str, tbl2: str, min_match: float):
    """find potential foreign key relationships between two CSV files"""
    console = Console()
    candidates = find_fk_relationships(
        Path(tbl1),
        Path(tbl2),
        min_match_percent=min_match
    )
    if not candidates:
        console.print("[yellow]No FK relationships found[/yellow]")
        return
    table = Table(title="potential FKs")
    table.add_column("table #1")
    table.add_column("table #2")
    table.add_column("match %")
    table.add_column("sample matches")
    for c in candidates:
        table.add_row(
            f"{c.child_table.removesuffix('.csv')}.{c.child_column}",
            f"{c.parent_table.removesuffix('.csv')}.{c.parent_column}",
            f"{c.match_percent:.1f}%",
            "\n".join(f"{m[0]} → {m[1]}" for m in c.sample_matches)
        )
    console.print(table)

if __name__ == "__main__":
    main()
