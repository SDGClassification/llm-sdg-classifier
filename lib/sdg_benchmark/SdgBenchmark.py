from pathlib import Path
import pandas as pd
from progress.bar import Bar
from .SdgBenchmarkStats import SdgBenchmarkStats

from typing import Callable, Optional

PredictSdgs = Callable[[str], list[int]]


class SdgBenchmark:
    """Run benchmark on an SDG classifier.

    Tests the performance of the given classifier on the SDG classification
    benchmarking dataset.
    """

    predict_sdgs: PredictSdgs
    df: pd.DataFrame
    bar: Bar
    _results: Optional[pd.DataFrame] = None
    _stats: Optional[SdgBenchmarkStats] = None

    def __init__(self, predict_sdgs: PredictSdgs) -> None:
        """Initialize the benchmark.

        Args:
            predict_sdgs: method that takes in a text and returns list of SDGs

        Typical usage example:

        def classify(text: str) -> list[int]:
            ... Call API and return relevant SDGs in numeric form ...

        benchmark = SdgBenchmark(predict_sdgs=classify)
        """
        self.predict_sdgs = predict_sdgs

        # Load the benchmarking dataset
        self.df = pd.read_csv(Path(__file__).parent.joinpath("benchmark.csv"))

        # Rename label to expected label, so we can more easily distinguish
        # between expectation and prediction
        self.df = self.df.rename(columns={"label": "expected_label"})

        # Prepare the progress bar
        self.bar = Bar("Benchmarking", max=len(self.df))

    def run(self) -> None:
        """Run the benchmark."""

        print("#" * 80)
        print("Running benchmark")
        self.bar.update()

        # Classify each text and get the predicted SDGs in *numeric* format
        self.df["predicted_sdgs"] = self.df["text"].map(
            self._predict_sdgs_with_progress
        )

        # Predictions are done
        self.bar.finish()

        # Determine the predicted label by checking whether the predicted SDGs
        # contain the SDG from the benchmarking dataset. Predicted label is set
        # to `True` if the benchmark's SDG is contained in the predictions.
        self.df["predicted_label"] = self.df.apply(
            lambda row: row.sdg in row.predicted_sdgs, axis=1
        )

        # Determine if texts were classified correctly
        self.df["correct"] = self.df["expected_label"] == self.df["predicted_label"]

        # Set results and calculate stats
        self._results = self.df
        self._stats = SdgBenchmarkStats.calculate_from_df(self.df)

        # Print stats
        print("Results:")
        print(self.stats)

        print("Benchmark completed")
        print("#" * 80)

    def _predict_sdgs_with_progress(self, text: str) -> list[int]:
        """Predict SDGs and advance progress.

        This method is a wrapper around the predict_sdgs method that was
        provided during initialization. This method simply calls the
        predict_sdgs method and then advances the progress bar.

        Args:
            text: The text to classify

        Returns: List of relevant SDGs in numeric format."""
        sdgs: list[int] = self.predict_sdgs(text)
        self.bar.next()
        return sdgs

    @property
    def stats(self) -> SdgBenchmarkStats:
        if self._stats is None:
            raise Exception("Benchmark is not complete")

        return self._stats

    @property
    def results(self) -> pd.DataFrame:
        if self._results is None:
            raise Exception("Benchmark is not complete")

        return self._results
