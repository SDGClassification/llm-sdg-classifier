# chatgpt_sdgs

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. It relies on ChatGPT's
existing knowledge of the SDGs.

Response is in JSON format.

## Parameters



- `model`: ChatGPT model to use


## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   Average |   SDG 1 |   SDG 2 |   SDG 3 |   SDG 4 |   SDG 5 |   SDG 6 |   SDG 7 |   SDG 10 |
|----------------:|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|---------:|
|               1 |      87.3 |    76.6 |    89.9 |    82.9 |    85.4 |    88.4 |    91.8 |      90 |     93.4 |
|               2 |      83.1 |    61   |    89.9 |    80.3 |    82.9 |    84.1 |    90.6 |      91 |     85.2 |


## Configuration 1 (`1875bee`)

**Parameters**:

- `model`: gpt-4-0125-preview


| SDG     |    n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|-----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average | 77.4 |           87.3 |            80.7 |         97.4 |       0.88 | 37.2 |    9 | 30.2 |  0.9 |
| 1       |   77 |           76.6 |            60.5 |         96.3 |       0.74 |   26 |   17 |   33 |    1 |
| 2       |   69 |           89.9 |            89.6 |         95.6 |       0.92 |   43 |    5 |   19 |    2 |
| 3       |   76 |           82.9 |            68.3 |        100.0 |       0.81 |   28 |   13 |   35 |    0 |
| 4       |   82 |           85.4 |            79.2 |         97.7 |       0.88 |   42 |   11 |   28 |    1 |
| 5       |   69 |           88.4 |            81.4 |        100.0 |       0.90 |   35 |    8 |   26 |    0 |
| 6       |   85 |           91.8 |            87.3 |        100.0 |       0.93 |   48 |    7 |   30 |    0 |
| 7       |  100 |           90.0 |            83.3 |        100.0 |       0.91 |   50 |   10 |   40 |    0 |
| 10      |   61 |           93.4 |            96.3 |         89.7 |       0.93 |   26 |    1 |   31 |    3 |

**Evaluated on**: May 10, 2024


## Configuration 2 (`6326b32`)

**Parameters**:

- `model`: gpt-3.5-turbo-0125


| SDG     |    n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|-----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average | 77.4 |           83.1 |            76.3 |         97.1 |       0.85 |   37 | 11.8 | 27.5 |  1.1 |
| 1       |   77 |           61.0 |            47.4 |        100.0 |       0.64 |   27 |   30 |   20 |    0 |
| 2       |   69 |           89.9 |            95.2 |         88.9 |       0.92 |   40 |    2 |   22 |    5 |
| 3       |   76 |           80.3 |            65.9 |         96.4 |       0.78 |   27 |   14 |   34 |    1 |
| 4       |   82 |           82.9 |            76.4 |         97.7 |       0.86 |   42 |   13 |   26 |    1 |
| 5       |   69 |           84.1 |            77.3 |         97.1 |       0.86 |   34 |   10 |   24 |    1 |
| 6       |   85 |           90.6 |            85.7 |        100.0 |       0.92 |   48 |    8 |   29 |    0 |
| 7       |  100 |           91.0 |            84.7 |        100.0 |       0.92 |   50 |    9 |   41 |    0 |
| 10      |   61 |           85.2 |            77.8 |         96.6 |       0.86 |   28 |    8 |   24 |    1 |

**Evaluated on**: May 10, 2024

