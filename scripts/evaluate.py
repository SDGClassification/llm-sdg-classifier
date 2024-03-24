import sys
from pathlib import Path

# Make the modules of the parent folder accessible to the scripts
# See: https://stackoverflow.com/a/27876800/6451879
sys.path.append(str(Path(__file__).absolute().parent.parent))

import os
import shutil
import argparse
from datetime import datetime
from babel.dates import format_date
from evaluations import BaseClassifier, Run
from lib.sdg_benchmark import SdgBenchmark
from scripts.update_readme import update_readme


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
benchmark = SdgBenchmark(predict_sdgs=classifier.classify)
benchmark.run()

# Store params, results and stats
run = Run(
    config=classifier.configuration,
    date=format_date(datetime.today(), format="long", locale="en"),
    stats=benchmark.stats,
    results=benchmark.results,
)
run.write_files(classifier.runs_directory)

# Clean up old runs
current_config_ids = [c.get_identifier() for c in configurations]
for dir in os.scandir(Path("evaluations", classifier.name, "runs")):
    if dir.name not in current_config_ids:
        shutil.rmtree(dir)

# Update README
update_readme(classifier)
