from dataclasses import dataclass, asdict
import pandas as pd
from tabulate import tabulate
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from typing import Self, Literal, Optional, Any

HUMAN_LABELS = dict(
    sdg="SDG",
    n="n",
    accuracy="Accuracy (%)",
    precision="Precision (%)",
    recall="Recall (%)",
    f1="F1 Score",
    tp="TP",
    fp="FP",
    tn="TN",
    fn="FN",
)


@dataclass(frozen=True, kw_only=True)
class Stats:
    """Benchmark statistics, such as accuracy and F1 score.

    Attributes:
        sdg: SDG Number
        n: Number of values
        accuracy: Accuracy in %
        precision: Precision in %
        recall: Recall in %
        f1: F1 score
        tp: True positives
        fp: False positives
        tn: True negatives
        fn: False negatives
    """

    sdg: int | Literal["All"]
    n: int
    accuracy: float
    precision: float
    recall: float
    f1: float
    tp: int
    fp: int
    tn: int
    fn: int

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def label(self) -> str:
        if self.sdg == "All":
            return self.sdg

        return f"SDG {self.sdg}"

    @classmethod
    def from_dict(cls, dict: dict[Any, Any]) -> Self:
        return cls(
            sdg=dict["sdg"],
            n=dict["n"],
            accuracy=dict["accuracy"],
            precision=dict["precision"],
            recall=dict["recall"],
            f1=dict["f1"],
            tp=dict["tp"],
            fp=dict["fp"],
            tn=dict["tn"],
            fn=dict["fn"],
        )

    @classmethod
    def from_series(
        cls, sdg: int | Literal["All"], expected: pd.Series, predicted: pd.Series
    ) -> Self:
        """Calculate stats from the expected and predicted values.

        Args:
            sdg: SDG number
            expected: The expected values
            predicted: The predicted values

        Returns: Stats instance"""
        # Calculate true and false positives and negatives
        tn, fp, fn, tp = confusion_matrix(expected, predicted).ravel()

        return cls(
            sdg=sdg,
            n=len(expected),
            accuracy=round(accuracy_score(expected, predicted) * 100, 2),
            precision=round(
                precision_score(expected, predicted, zero_division=0) * 100, 2
            ),
            recall=round(recall_score(expected, predicted, zero_division=0) * 100, 2),
            f1=round(f1_score(expected, predicted), 2),
            tp=tp,
            fp=fp,
            tn=tn,
            fn=fn,
        )


class SdgBenchmarkStats:
    """Benchmark statistics"""

    overall: Stats
    sdgs: list[Optional[Stats]]

    def __init__(self, overall: Stats, sdgs: list[Optional[Stats]]):
        self.overall = overall
        self.sdgs = sdgs

    def __str__(self) -> str:
        return self.format("psql")

    def format(self, tablefmt: str) -> str:
        """Format the stats as a table.

        All formats of `tabulate` are supported.

        Args:
            tablefmt: The format to use (github, psql, etc...)"""
        data = [stats.to_dict() for stats in self.to_list()]

        # Replace dict keys with human labels
        data = [{HUMAN_LABELS[k]: item[k] for k in item} for item in data]

        return tabulate(
            data,
            headers="keys",
            tablefmt=tablefmt,
        )

    def to_list(self) -> list[Stats]:
        return [
            self.overall,
            *[sdg for sdg in self.sdgs if sdg],
        ]

    def to_df(self) -> pd.DataFrame:
        """Converts the stats into a Pandas dataframe."""
        return pd.DataFrame(self.to_list())

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Self:
        """Converts Pandas dataframe into SdgBenchmarkStats."""
        # Prepare overall stats
        overall_df = df[df.sdg == "All"]
        overall_stats = Stats.from_dict(overall_df.to_dict("records")[0])

        # Prepare SDG stats
        sdgs_df = df[df.sdg != "All"].copy()

        # Convert SDG numbers to numeric
        sdgs_df.sdg = pd.to_numeric(sdgs_df.sdg)

        sdgs_stats: list[Optional[Stats]] = []
        for sdg in range(1, 18):
            if sdg in sdgs_df.sdg.values:
                sdgs_stats.append(
                    Stats.from_dict(sdgs_df[sdgs_df.sdg == sdg].to_dict("records")[0])
                )
            else:
                sdgs_stats.append(None)

        return cls(overall=overall_stats, sdgs=sdgs_stats)

    @classmethod
    def calculate_from_df(cls, df: pd.DataFrame) -> Self:
        """Calculate SdgBenchmarkStats from dataframe.

        Args:
            df: Dataframe from SdgBenchmark"""
        overall_stats = Stats.from_series(
            "All", df["expected_label"], df["predicted_label"]
        )
        sdg_stats: list[Optional[Stats]] = []
        for sdg in range(1, 18):
            # Get expected and predicted labels
            expected = df[df["sdg"] == sdg]["expected_label"]
            predicted = df[df["sdg"] == sdg]["predicted_label"]

            if len(expected) == 0:
                sdg_stats.append(None)
            else:
                sdg_stats.append(Stats.from_series(sdg, expected, predicted))

        return cls(overall=overall_stats, sdgs=sdg_stats)
