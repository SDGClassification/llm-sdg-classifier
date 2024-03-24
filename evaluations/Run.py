import json
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from lib.sdg_benchmark import SdgBenchmarkStats
from .Config import Config

from typing import Self


@dataclass(kw_only=True)
class Run:
    config: Config
    date: str
    stats: SdgBenchmarkStats
    results: pd.DataFrame

    def write_files(self, runs_directory: Path) -> None:
        """Write run files to disk.

        Args:
            runs_directory: Directory where runs are stored."""
        dir_path = runs_directory.joinpath(self.config.get_identifier())
        dir_path.mkdir(exist_ok=True)

        # Write meta
        with open(dir_path.joinpath("meta.json"), "w") as f:
            json.dump(dict(config=self.config, date=self.date), f, indent=4)

        # Write stats
        self.results.to_csv(dir_path.joinpath("results.csv"), index=False)

        # Write results
        self.stats.to_df().to_csv(dir_path.joinpath("stats.csv"), index=False)

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
        stats = SdgBenchmarkStats.from_df(pd.read_csv(dir_path.joinpath("stats.csv")))
        results = pd.read_csv(dir_path.joinpath("results.csv"))

        return cls(
            config=config,
            date=meta["date"],
            stats=stats,
            results=results,
        )
