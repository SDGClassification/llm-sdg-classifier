import sys
from pathlib import Path

# Make the modules of the parent folder accessible to the scripts
# See: https://stackoverflow.com/a/27876800/6451879
sys.path.append(str(Path(__file__).absolute().parent.parent))

import argparse
from datetime import datetime
from babel.dates import format_date
from classifiers import BaseClassifier, Run
from sdgclassification.benchmark import Benchmark
from scripts.update_files import update_files


# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Evaluate LLM classifier against benchmark"
)
parser.add_argument("classifier", type=str)
parser.add_argument("--config", type=int)
args = parser.parse_args()

Classifier = BaseClassifier.load(args.classifier)
configurations = Classifier.CONFIGURATIONS

# If only a single config exists, always use it
if len(configurations) == 1:
    args.config = 1

# If config was not provided, prompt user for it
if args.config is None:
    print(f"{args.classifier} has several configurations available.")
    [print(f"{i+1}) {c}") for i, c in enumerate(configurations)]
    args.config = int(input("Enter configuration number: "))

# Instantiate classifier
classifier = Classifier(args.config)

# Run benchmark
benchmark = Benchmark(predict_sdgs=classifier.classify)
benchmark.run()

# Store params, results and stats
run = Run(
    config=classifier.configuration,
    date=format_date(datetime.today(), format="long", locale="en"),
    stats=benchmark.stats.to_dataframe(),
    results=benchmark.results.to_dataframe(),
)
run.write_files(classifier.runs_directory)

# Update files
update_files(classifier)
