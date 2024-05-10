# LLM SDG Classifier<!-- omit from toc -->

This repo contains several experiments for classifying texts by Sustainable
Development Goal using recent Large Language Models, such as ChatGPT and Llama2.

## Table of Contents<!-- omit from toc -->

- [Motivation](#motivation)
- [Evaluations](#evaluations)
- [Setup](#setup)
- [How to use](#how-to-use)
  - [Adding an LLM classifier](#adding-an-llm-classifier)
  - [Adding configurations](#adding-configurations)
  - [Caching requests](#caching-requests)
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

The table below shows the accuracy of the LLM classifiers. If a classifier has
several configurations, the table shows the results for the configuration that
achieved the highest overall accuracy.

Clicking on one of the classifiers provides additional details, including
metadata about the classifier, F1 score, precision, recall and results for any
other configurations.

<!-- evaluation table begin -->

| Classifier                                            |   Average |   SDG 1 |   SDG 2 |   SDG 3 |   SDG 4 |   SDG 5 |   SDG 6 |   SDG 7 |   SDG 10 |
|:------------------------------------------------------|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|---------:|
| [chatgpt_sdgs](classifiers/chatgpt_sdgs/)             |      87.3 |    76.6 |    89.9 |    82.9 |    85.4 |    88.4 |    91.8 |      90 |     93.4 |
| [chatgpt_topics_hmc](classifiers/chatgpt_topics_hmc/) |      56.1 |    64.9 |    34.8 |    63.2 |    47.6 |    49.3 |    43.5 |      93 |     52.5 |

<!-- evaluation table end -->

## Setup

This project uses Python 3.12.

[Poetry](https://python-poetry.org/) is used to manage dependencies. To get
started, run `poetry install`.

All `python` commands should be executed from within `poetry shell`.

Depending on the classifiers you want to run, you may need to configure
environment variables in [.env](.env), such as the `OPENAI_API_KEY`. Please refer to [.env.sample](.env.sample) for details.

## How to use

The [classifiers](classifiers/) directory contains a number of different SDG
classification models that all use LLM under the hood. Each model may be using a
different LLM, different prompts and/or different parameters.

### Adding an LLM classifier

To add your own classifier, create a new file `myclassifier.py` in a
`myclassifier` folder under the [classifiers](classifiers/) directory.

The path for the new classifier should be as follows:
`classifiers/myclassifier/myclassifier.py`

You are free to pick any name, combining characters and underscores.

A basic classifier looks like this:

```python
# classifiers/myclassifier/myclassifier.py

from classifiers import BaseClassifier

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

### Adding configurations

Classifiers can define different configurations that they support. This makes it
possible to use one classifier for many similar evaluations. For example,
running the same prompts but with different models (GPT 4 vs GPT 3.5), different
temperature, etc...

To add a configuration to a classifier, overwrite the `CONFIGURATIONS` attribute
in the classifier:

```python
# classifiers/myclassifier/myclassifier.py

from classifiers import BaseClassifier, ConfigSet, Config, Parameters

class Classifier(BaseClassifier):
    """Description of classifier goes here."""

    # Define your configurations below
    CONFIGURATIONS=ConfigSet(
      # Define the set of allowed parameters
      Parameters(model="ChatGPT model"),

      # Note: Each config must define all parameters!
      Config(model="gpt-4-0125-preview"),
      Config(model="gpt-3.5-turbo-0125")
    )

    model: str

    def __post_init__(self, configuration: Config) -> None:
      # You can access the configuration here
      # Note: You can also access the configuration later via self.configuration
      self.model = configuration.model

    def classify(self, text: str) -> list[int]:
        # Access self.model or self.configuration here
        print(self.model)
        return [...]
```

### Caching requests

You may want to cache API requests, so that future requests with the exact same
parameters will skip the request and just rely on the cache.

To do this, wrap the method that calls the API with the `with_cache` method.

For example:

```python
# classifiers/myclassifier/myclassifier.py

from openai import OpenAI
from dotenv import load_dotenv
from classifiers import BaseClassifier

class Classifier(BaseClassifier):
    """Description of classifier goes here."""

    def __post_init__(self, configuration: Config) -> None:
        # Set up OpenAI client
        load_dotenv()
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        # This caches calls to the OpenAI chat completions endpoint
        self.create_chat_completion = self.with_cache(client.chat.completions.create)

    def classify(self, text: str) -> list[int]:
        # These calls are now being cached
        res = self.create_chat_completion(model="gpt-4-turbo-preview", messages=[...])

        # Process response and return SDGs
        return [...]
```

Note that caching is based on the name of the method that is being cached and
the arguments that are passed to the method. Therefore, you should never access
attributes within the method but rather pass them as method arguments:

```python
# Good
def make_api_request(model: str, prompt: str) -> str:
    return requests.get(model=model, prompt=prompt)

# Bad - avoid this!
# Because the cache key is based on the method name plus arguments, any call to
# this method will always hit the cache and return an identical result
def make_api_request() -> str:
    return requests.get(model=self.model, prompt=self.prompt)
```

The cache is stored in the classifier directory under `.cache`. To clear the
cache, simply remove that folder. Example: `classifiers/chatgpt_sdgs/.cache/`

### Running an LLM classifier

To benchmark an LLM classifier, simply run the `evaluate.py` script (from within
the `poetry shell`):

```bash
python scripts/evaluate.py myclassifier
```

If several configs have been defined for the classifier, you will be prompted to
select the config that you want to run.

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
[classifiers/chatgpt_sdgs/README.md](classifiers/chatgpt_sdgs/README.md)
