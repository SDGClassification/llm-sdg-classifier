import sys
from pathlib import Path

# Make the modules of the parent folder accessible to the scripts
# See: https://stackoverflow.com/a/27876800/6451879
sys.path.append(str(Path(__file__).absolute().parent.parent))


import inspect
import pandas as pd
from jinja2 import Template, StrictUndefined
from tabulate import tabulate
from classifiers import BaseClassifier, Run

from typing import Union, Type


def update_readme(classifier: Union[BaseClassifier, Type[BaseClassifier]]) -> None:
    """Re-generates the README.md file for the given classifier.

    Args:
        classifier: Instance or class of classifier"""

    configurations = classifier.CONFIGURATIONS

    # Load data from all runs
    runs = [
        Run.load(config=c, runs_directory=classifier.runs_directory)
        for c in configurations
    ]

    # Evaluate data across all runs
    evaluation = pd.DataFrame(
        index=[c.get_identifier() for c in configurations],
        columns=["Configuration", "All", *[f"SDG {x}" for x in range(1, 18)]],
    )
    evaluation["Configuration"] = range(1, len(configurations) + 1)

    # Fill in data from completed runs
    for run in [r for r in runs if r is not None]:
        id = run.config.get_identifier()
        for stat in run.stats.to_list():
            evaluation.at[id, stat.label] = stat.accuracy

    # Drop empty columns
    evaluation = evaluation.dropna(how="all", axis=1)
    evaluation_data = evaluation.to_dict("records")

    # Update README
    with open(Path("classifiers", "core", "README.md.jinja"), "r") as f:
        template = Template(f.read(), undefined=StrictUndefined)

    with open(classifier.directory.joinpath("README.md"), "w") as f:
        f.write(
            template.render(
                classifier=classifier.name,
                docstring=inspect.cleandoc(
                    classifier.__doc__ or "No documentation provided."
                ),
                parameters=classifier.CONFIGURATIONS.parameters,
                evaluation_table=tabulate(
                    evaluation_data, headers="keys", tablefmt="github"
                ),
                configurations=classifier.CONFIGURATIONS,
                runs=runs,
            )
        )


if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Update README for LLM classifier")
    parser.add_argument("classifier", type=str)
    args = parser.parse_args()

    Classifier = BaseClassifier.load(args.classifier)
    update_readme(Classifier)

    print(f"Readme for {Classifier.name} updated")
