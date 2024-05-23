import sys
from pathlib import Path

# Make the modules of the parent folder accessible to the scripts
# See: https://stackoverflow.com/a/27876800/6451879
sys.path.append(str(Path(__file__).absolute().parent.parent))

import os
import shutil
import inspect
import re
import pandas as pd
from jinja2 import Template, StrictUndefined
from tabulate import tabulate
from classifiers import BaseClassifier, Run

from typing import Union, Type


def update_files(classifier: Union[BaseClassifier, Type[BaseClassifier]]) -> None:
    """Re-generates the files for the given classifier.

    Re-generates README.md and stats.csv files for the classifier.
    Updates the evaluation table in the main README.md.

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
        columns=["Configuration", "Average", *[f"SDG {x}" for x in range(1, 18)]],
    )
    evaluation["Configuration"] = range(1, len(configurations) + 1)

    # Fill in data from completed runs
    for run in [r for r in runs if r is not None]:
        id = run.config.get_identifier()

        # Only consider SDGs with at least one text
        stats_df = run.stats[run.stats.n > 0]
        for _, row in stats_df.iterrows():
            label = row.sdg if row.sdg == "Average" else f"SDG {row.sdg}"
            evaluation.at[id, label] = row.accuracy

    # Re-order columns
    evaluation = evaluation[
        [
            "Configuration",
            "Average",
            *[f"SDG {x}" for x in range(1, 18)],
        ]
    ]

    # Update stats.csv file
    evaluation.to_csv(classifier.directory.joinpath("stats.csv"), index=False)

    # Cast columns to float types
    evaluation = evaluation.astype(
        dtype={
            "Configuration": int,
            "Average": float,
            **{f"SDG {x}": float for x in range(1, 18)},
        }
    )

    # Round stats to 1 decimal
    evaluation = evaluation.round(1)

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
                    evaluation_data, headers="keys", tablefmt="pipe"
                ),
                configurations=classifier.CONFIGURATIONS,
                runs=runs,
            )
        )

    # Clean up old runs
    current_config_ids = [c.get_identifier() for c in configurations]
    for dir in os.scandir(classifier.runs_directory):
        if dir.name not in current_config_ids:
            shutil.rmtree(dir)

    # Update main README
    stats = []
    for dir in os.scandir("classifiers"):
        # Only consider directories
        if not dir.is_dir():
            continue

        # Skip folders that do not define a <classifier-name.py> file
        if not Path(dir.path, dir.name + ".py").exists():
            continue

        # Skip folders that do not have a stats.csv file
        if not Path(dir.path, "stats.csv").exists():
            continue

        # Load stats
        stats_df = pd.read_csv(Path(dir.path, "stats.csv"))

        # Check if stats are in new format (using averages)
        if "Average" not in stats_df.columns:
            print(
                "Info: Updating README: Skipping",
                dir.name,
                "because stats are not yet in new format",
            )
            continue

        # Add name (as markdown link)
        stats_df["Classifier"] = f"[{dir.name}](classifiers/{dir.name}/)"

        # Keep highest accuracy only
        stats_df = stats_df.sort_values(by=["Average"], ascending=False)
        stats_df = stats_df.drop(columns=["Configuration"])

        # Combine into dataframe
        stats.append(stats_df[:1])

    # Combine into overall stats
    overall_stats_df = pd.concat(stats)

    # Re-order columns
    overall_stats_df = overall_stats_df[
        [
            "Classifier",
            "Average",
            *[f"SDG {x}" for x in range(1, 18)],
        ]
    ]

    # Cast columns to float types
    overall_stats_df = overall_stats_df.astype(
        dtype={
            "Classifier": str,
            "Average": float,
            **{f"SDG {x}": float for x in range(1, 18)},
        }
    )

    # Round stats to 1 decimal
    overall_stats_df = overall_stats_df.round(1)

    # Drop empty columns
    overall_stats_df = overall_stats_df.dropna(how="all", axis=1)
    overall_stats_table = tabulate(
        overall_stats_df.to_dict("records"), headers="keys", tablefmt="pipe"
    )

    # Replace stats in README.md
    with open("README.md", "r") as f:
        readme = f.read()

    readme = re.sub(
        r"(^<!-- evaluation table begin -->\n\n)(.*)(\n\n<!-- evaluation table end -->$)",
        lambda match: match.group(1) + overall_stats_table + match.group(3),
        readme,
        count=1,
        flags=re.MULTILINE + re.DOTALL,
    )

    with open("README.md", "w") as f:
        f.write(readme)


if __name__ == "__main__":
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Update files for LLM classifier")
    parser.add_argument("classifier", type=str)
    args = parser.parse_args()

    Classifier = BaseClassifier.load(args.classifier)
    update_files(Classifier)

    print(f"Files for {Classifier.name} updated")
