# chatgpt_topics_hmc

Hierarchical Multi-label Classification (HMC) with ChatGPT using topics.

Rather than prompting ChatGPT to directly map texts to SDGs, we prompt
ChatGPT to map texts to a manually defined list of topics (e.g. energy) and
subtopics(e.g. renewable energy). Each subtopic is associated with one SDG.

Thanks to the hierarchical nature of the classification, all texts are first
broadly mapped to topics. If a topic is found in the text, the classifier
then checks the text for the list of very specific subtopics.

Example Prompt:

```
You are an intelligent multi-label classification system designed to perform topic classification.

You take the Text delimited by triple quotes as input and return a comma-separated list of relevant topic IDs.

If none of the topics are relevant, return 0.

Topics:
1) ...
2) ...
3) ...

Text: """ ... text goes here ... """

Topic IDs:
```

## Parameters



- `model`: ChatGPT model to use


## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   Average |   SDG 1 |   SDG 2 |   SDG 3 |   SDG 4 |   SDG 5 |   SDG 6 |   SDG 7 |   SDG 10 |
|----------------:|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|---------:|
|               1 |     nan   |   nan   |   nan   |   nan   |   nan   |   nan   |   nan   |      93 |     52.5 |
|               2 |      56.1 |    64.9 |    34.8 |    63.2 |    47.6 |    49.3 |    43.5 |      93 |     52.5 |


## Configuration 1 (`1875bee`)

**Parameters**:

- `model`: gpt-4-0125-preview


| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:------|----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| All   | 161 |           77.6 |            92.2 |         59.5 |       0.72 |   47 |    4 |   78 |   32 |
| 7     | 100 |           93.0 |            92.2 |         94.0 |       0.93 |   47 |    4 |   46 |    3 |
| 10    |  61 |           52.5 |             0.0 |          0.0 |       0.00 |    0 |    0 |   32 |   29 |

**Evaluated on**: March 25, 2024


## Configuration 2 (`6326b32`)

**Parameters**:

- `model`: gpt-3.5-turbo-0125


| SDG     |    n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|-----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average | 77.4 |           56.1 |            11.0 |         12.5 |       0.12 |  6.2 |  0.9 | 38.4 | 31.9 |
| 1       |   77 |           64.9 |             0.0 |          0.0 |       0.00 |    0 |    0 |   50 |   27 |
| 2       |   69 |           34.8 |             0.0 |          0.0 |       0.00 |    0 |    0 |   24 |   45 |
| 3       |   76 |           63.2 |             0.0 |          0.0 |       0.00 |    0 |    0 |   48 |   28 |
| 4       |   82 |           47.6 |             0.0 |          0.0 |       0.00 |    0 |    0 |   39 |   43 |
| 5       |   69 |           49.3 |             0.0 |          0.0 |       0.00 |    0 |    0 |   34 |   35 |
| 6       |   85 |           43.5 |             0.0 |          0.0 |       0.00 |    0 |    0 |   37 |   48 |
| 7       |  100 |           93.0 |            87.7 |        100.0 |       0.93 |   50 |    7 |   43 |    0 |
| 10      |   61 |           52.5 |             0.0 |          0.0 |       0.00 |    0 |    0 |   32 |   29 |

**Evaluated on**: May 10, 2024

