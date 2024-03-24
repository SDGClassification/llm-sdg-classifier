# LLM SDG Classifier<!-- omit from toc -->

This repo contains several experiments for classifying texts by Sustainable
Development Goal using recent Large Language Models, such as ChatGPT and Llama2.

## Table of Contents<!-- omit from toc -->

- [Motivation](#motivation)
- [Evaluations](#evaluations)
- [Setup](#setup)
- [How to use](#how-to-use)
  - [Adding an LLM classifier](#adding-an-llm-classifier)
  - [Running an LLM classifier](#running-an-llm-classifier)

## Motivation

Many organizations around the world are working on text classification for the
Sustainable Development Goals (SDGs). Refer to [this
list](https://globalgoals-directory.notion.site/PUBLIC-List-of-AI-driven-SDG-Classification-Initiatives-fe4770a173194e0b980f95b330a8a83b)
for a (non-exhaustive) overview of different SDG classifiers and initiatives.
Use cases include policy mapping, research analysis, and website classification.

Due to the complexity of the SDGs, with 17 goals and 169 targets, developing an
accurate text classification model is very challenging and resource intensive.
Development requires the compilation of long keyword lists (for pattern
matching) or the manual annotation of very large training datasets (for machine
learning).

With the release of the latest generation of large language models, such as
ChatGPT and Llama2, there is a growing interest in the SDG classification
community to test the suitability of these models for SDG classification.

Can modern LLMs perform accurate SDG classification with no (or little) manually
annotated training data? If so, they could prove to be a major leap forward for
SDG classification initiatives.

## Evaluations

| Approach | Parameters | SDG 7 | SDG 10 |
| -------- | ---------- | ----- | ------ |

Different params:

- temp
- json
- etc...

## Setup

This project uses Python 3.12.

[Poetry](https://python-poetry.org/) is used to manage dependencies. To get
started, run `poetry install`.

All `python` commands should be executed from within `poetry shell`.

Depending on the classifiers you want to run, you may need to configure
environment variables in [.env](.env), such as the `OPENAI_API_KEY`. Please refer to [.env.sample](.env.sample) for details.

## How to use

The [evaluations](evaluations/) directory contains a number of different SDG
classification models that all use LLM under the hood. Each model may be using a
different LLM, different prompts and/or different parameters.

### Adding an LLM classifier

To add your own classifier, create a new file `myclassifier.py` in a
`myclassifier` folder under the [evaluations](evaluations/) directory.

The path for the new classifier should be as follows:
`evalutions/myclassifier/myclassifier.py`

You are free to pick any name, combining characters and underscores.

A basic classifier looks like this:

```python
# evaluations/myclassifier/myclassifier.py

from evaluations import BaseClassifier

class Classifier(BaseClassifier):
    """Description of classifier goes here.

    Description continues here...

    Anything written in this docstring will be used to
    generate the README.md file for this classifier.
    """

    def classify(self, text: str) -> list[int]:
        """Classify the given text and return relevant SDGs in numeric form."""
        # ...Perform classification here...
        # For example, make a request to the OpenAI API

        # Return relevant SDGs in numeric form
        return [1, 7, 12]
```

### Running an LLM classifier

To benchmark an LLM classifier, simply run the `evaluate.py` script (from within
the `poetry shell`):

```bash
python scripts/evaluate.py myclassifier
```

As the benchmark progresses, you will see the following output:

```bash
Running benchmark
Benchmarking |################################| 161/161
Results:
+-------+-----+----------------+-----------------+--------------+------------+------+------+------+------+
| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------+-----+----------------+-----------------+--------------+------------+------+------+------+------|
| All   | 161 |          91.3  |           87.36 |        96.2  |       0.92 |   76 |   11 |   71 |    3 |
| 7     | 100 |          90    |           83.33 |       100    |       0.91 |   50 |   10 |   40 |    0 |
| 10    |  61 |          93.44 |           96.3  |        89.66 |       0.93 |   26 |    1 |   31 |    3 |
+-------+-----+----------------+-----------------+--------------+------------+------+------+------+------+
Benchmark completed
################################################################################
```

After the evaluation is complete, you can review the new/updated README.md file
that has been generated in the folder of the classifier. Example:
[evaluations/chatgpt_sdgs/README.md](evaluations/chatgpt_sdgs/README.md)
