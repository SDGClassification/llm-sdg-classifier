# chatgpt_sdgs

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. It relies on ChatGPT's
existing knowledge of the SDGs.

Response is in JSON format.

## Parameters



- `model`: ChatGPT model to use


## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   All |   SDG 7 |   SDG 10 |
|-----------------|-------|---------|----------|
|               1 | 91.3  |      90 |    93.44 |
|               2 | 88.82 |      91 |    85.25 |


## Configuration 1 (`1875bee`)

**Parameters**:

- `model`: gpt-4-0125-preview


| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------|-----|----------------|-----------------|--------------|------------|------|------|------|------|
| All   | 161 |          91.3  |           87.36 |        96.2  |       0.92 |   76 |   11 |   71 |    3 |
| 7     | 100 |          90    |           83.33 |       100    |       0.91 |   50 |   10 |   40 |    0 |
| 10    |  61 |          93.44 |           96.3  |        89.66 |       0.93 |   26 |    1 |   31 |    3 |

**Evaluated on**: March 24, 2024


## Configuration 2 (`6326b32`)

**Parameters**:

- `model`: gpt-3.5-turbo-0125


| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------|-----|----------------|-----------------|--------------|------------|------|------|------|------|
| All   | 161 |          88.82 |           82.11 |        98.73 |       0.9  |   78 |   17 |   65 |    1 |
| 7     | 100 |          91    |           84.75 |       100    |       0.92 |   50 |    9 |   41 |    0 |
| 10    |  61 |          85.25 |           77.78 |        96.55 |       0.86 |   28 |    8 |   24 |    1 |

**Evaluated on**: March 24, 2024

