import json
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from tabulate import tabulate
from sdgclassification.benchmark import Stats
from .Config import Config

from typing import Self


@dataclass(kw_only=True)
class Run:
    config: Config
    date: str
    stats: pd.DataFrame
    results: pd.DataFrame

    def write_files(self, runs_directory: Path) -> None:
        """Write run files to disk.

        Args:
            runs_directory: Directory where runs are stored."""
        dir_path = runs_directory.joinpath(self.config.get_identifier())
        dir_path.mkdir(exist_ok=True, parents=True)

        # Write meta
        with open(dir_path.joinpath("meta.json"), "w") as f:
            json.dump(dict(config=self.config, date=self.date), f, indent=4)

        # Write stats
        self.results.to_csv(dir_path.joinpath("results.csv"), index=False)

        # Write results
        self.stats.to_csv(dir_path.joinpath("stats.csv"), index=False)

    def stats_table(self, tablefmt: str, score_precision=1, f1_precision=2) -> str:
        """Formats the stats as a table.

        All formats of `tabulate` are supported.

        Args:
            tablefmt: The format to use (github, psql, etc...)
            score_precision: Number of decimal digits to display for scores
            f1_precision: Number of decimal digits to display for F1 score

        Returns: String of table format"""

        df = self.stats

        # Only keep metrics with at least one text
        df = df[df.n > 0].copy()

        # Round ints to 1 decimal
        for col in ["n", "tp", "fp", "tn", "fn"]:
            df[col] = df[col].apply(lambda x: f"{x:.1f}".rstrip("0").rstrip("."))

        # Adjust precision level
        for col in ["accuracy", "precision", "recall"]:
            df[col] = df[col].apply(lambda x: f"{x:.{score_precision}f}")

        df.f1 = df.f1.apply(lambda x: f"{x:.{f1_precision}f}")

        # Rename columns
        df = df.rename(columns=Stats.HUMAN_LABELS)

        # Convert to dictionary
        data = df.to_dict("records")

        # Set column alignment
        column_alignment = ["right" for _ in df.columns]
        column_alignment[0] = "left"

        return tabulate(
            data,
            headers="keys",
            tablefmt=tablefmt,
            disable_numparse=True,
            colalign=column_alignment,
        )

    @classmethod
    def load(cls, config: Config, runs_directory: Path) -> Self | None:
        """Load run data for the config.

        Args:
            config: Instance of the config
            runs_directory: Directory where runs are stored.

        Returns: Instance of run or None (if no run exists)

        Raises: FileNotFoundError if no run for the given config exists
        """
        dir_path = runs_directory.joinpath(config.get_identifier())

        if not dir_path.exists():
            return None

        # Load all data
        with open(dir_path.joinpath("meta.json")) as f:
            meta = json.load(f)
        stats = pd.read_csv(dir_path.joinpath("stats.csv"))
        results = pd.read_csv(dir_path.joinpath("results.csv"))

        return cls(
            config=config,
            date=meta["date"],
            stats=stats,
            results=results,
        )
