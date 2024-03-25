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

|   Configuration |   All |   SDG 7 |   SDG 10 |
|-----------------|-------|---------|----------|
|               1 | 77.64 |      93 |    52.46 |
|               2 | 77.64 |      93 |    52.46 |


## Configuration 1 (`1875bee`)

**Parameters**:

- `model`: gpt-4-0125-preview


| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------|-----|----------------|-----------------|--------------|------------|------|------|------|------|
| All   | 161 |          77.64 |           92.16 |        59.49 |       0.72 |   47 |    4 |   78 |   32 |
| 7     | 100 |          93    |           92.16 |        94    |       0.93 |   47 |    4 |   46 |    3 |
| 10    |  61 |          52.46 |            0    |         0    |       0    |    0 |    0 |   32 |   29 |

**Evaluated on**: March 25, 2024


## Configuration 2 (`6326b32`)

**Parameters**:

- `model`: gpt-3.5-turbo-0125


| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------|-----|----------------|-----------------|--------------|------------|------|------|------|------|
| All   | 161 |          77.64 |           87.72 |        63.29 |       0.74 |   50 |    7 |   75 |   29 |
| 7     | 100 |          93    |           87.72 |       100    |       0.93 |   50 |    7 |   43 |    0 |
| 10    |  61 |          52.46 |            0    |         0    |       0    |    0 |    0 |   32 |   29 |

**Evaluated on**: March 25, 2024
