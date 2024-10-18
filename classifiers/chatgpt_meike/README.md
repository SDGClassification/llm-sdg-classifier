# chatgpt_meike

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. Instead of relying on GPT's knowledge of SDGs,
it provides the descriptions of all SDGs.

## Parameters



- `model`: ChatGPT model to use


## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   Average |   SDG 1 |   SDG 2 |   SDG 3 |   SDG 4 |   SDG 5 |   SDG 6 |   SDG 7 |   SDG 8 |   SDG 10 |
|----------------:|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|---------:|
|               1 |      92.8 |    94.8 |    92.8 |    93.4 |    95.1 |    88.4 |    96.5 |      96 |    85.1 |     93.4 |
|               2 |      91.8 |   nan   |   nan   |   nan   |   nan   |   nan   |   nan   |     nan |   nan   |     91.8 |


## Configuration 1 (`1e1a9c9`)

**Parameters**:

- `model`: gpt-4o


| SDG     |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average |  77 |           92.8 |            94.0 |         91.1 |       0.92 | 34.9 |  2.1 | 36.8 |  3.2 |
| 1       |  77 |           94.8 |            89.7 |         96.3 |       0.93 |   26 |    3 |   47 |    1 |
| 2       |  69 |           92.8 |            97.6 |         91.1 |       0.94 |   41 |    1 |   23 |    4 |
| 3       |  76 |           93.4 |            92.6 |         89.3 |       0.91 |   25 |    2 |   46 |    3 |
| 4       |  82 |           95.1 |            93.3 |         97.7 |       0.95 |   42 |    3 |   36 |    1 |
| 5       |  69 |           88.4 |            93.5 |         82.9 |       0.88 |   29 |    2 |   32 |    6 |
| 6       |  85 |           96.5 |            97.9 |         95.8 |       0.97 |   46 |    1 |   36 |    2 |
| 7       | 100 |           96.0 |            94.2 |         98.0 |       0.96 |   49 |    3 |   47 |    1 |
| 8       |  74 |           85.1 |            90.9 |         78.9 |       0.85 |   30 |    3 |   33 |    8 |
| 10      |  61 |           93.4 |            96.3 |         89.7 |       0.93 |   26 |    1 |   31 |    3 |

**Evaluated on**: May 23, 2024


## Configuration 2 (`3bb2eb2`)

**Parameters**:

- `model`: gpt-4-turbo


| SDG     |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average |  61 |           91.8 |           100.0 |         82.8 |       0.91 |   24 |    0 |   32 |    5 |
| 10      |  61 |           91.8 |           100.0 |         82.8 |       0.91 |   24 |    0 |   32 |    5 |

**Evaluated on**: May 23, 2024

