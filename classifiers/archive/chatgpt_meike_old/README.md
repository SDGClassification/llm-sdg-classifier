# chatgpt_meike_old

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. Instead of relying on GPT's knowledge of SDGs,
it provides the formal descriptions of all SDGs, e.g. SDG 1: End poverty in all its forms everywhere.

This is an informed zero-shot multilabel classifier.

## Parameters



- `model`: ChatGPT model to use


## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   Average |   SDG 1 |   SDG 2 |   SDG 3 |   SDG 4 |   SDG 5 |   SDG 6 |   SDG 7 |   SDG 8 |   SDG 9 |   SDG 10 |   SDG 11 |   SDG 12 |   SDG 13 |   SDG 14 |   SDG 15 |   SDG 16 |   SDG 17 |
|----------------:|----------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|--------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
|               1 |      89.7 |      87 |    91.3 |    96.1 |    92.7 |    94.2 |    91.8 |      96 |    81.1 |    89.5 |     90.2 |       87 |       90 |     93.8 |     88.1 |     94.4 |     80.9 |     81.2 |
|               2 |     nan   |     nan |   nan   |   nan   |   nan   |   nan   |   nan   |     nan |   nan   |   nan   |    nan   |      nan |      nan |    nan   |    nan   |    nan   |    nan   |    nan   |
|               3 |     nan   |     nan |   nan   |   nan   |   nan   |   nan   |   nan   |     nan |   nan   |   nan   |    nan   |      nan |      nan |    nan   |    nan   |    nan   |    nan   |    nan   |


## Configuration 1 (`7c7fa81`)

**Parameters**:

- `model`: gpt-4o-mini


| SDG     |    n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:--------|-----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| Average | 73.6 |           89.7 |            89.8 |         89.5 |       0.89 | 32.5 |  3.7 | 33.6 |  3.7 |
| 1       |   77 |           87.0 |            74.3 |         96.3 |       0.84 |   26 |    9 |   41 |    1 |
| 2       |   69 |           91.3 |            97.6 |         88.9 |       0.93 |   40 |    1 |   23 |    5 |
| 3       |   76 |           96.1 |            93.1 |         96.4 |       0.95 |   27 |    2 |   46 |    1 |
| 4       |   82 |           92.7 |            87.8 |        100.0 |       0.93 |   43 |    6 |   33 |    0 |
| 5       |   69 |           94.2 |            91.9 |         97.1 |       0.94 |   34 |    3 |   31 |    1 |
| 6       |   85 |           91.8 |            95.6 |         89.6 |       0.92 |   43 |    2 |   35 |    5 |
| 7       |  100 |           96.0 |            96.0 |         96.0 |       0.96 |   48 |    2 |   48 |    2 |
| 8       |   74 |           81.1 |            81.6 |         81.6 |       0.82 |   31 |    7 |   29 |    7 |
| 9       |   57 |           89.5 |            92.3 |         85.7 |       0.89 |   24 |    2 |   27 |    4 |
| 10      |   61 |           90.2 |            92.6 |         86.2 |       0.89 |   25 |    2 |   30 |    4 |
| 11      |   69 |           87.0 |            82.1 |         85.2 |       0.84 |   23 |    5 |   37 |    4 |
| 12      |   80 |           90.0 |            94.9 |         86.0 |       0.90 |   37 |    2 |   35 |    6 |
| 13      |   65 |           93.8 |            91.4 |         97.0 |       0.94 |   32 |    3 |   29 |    1 |
| 14      |   84 |           88.1 |            83.8 |         88.6 |       0.86 |   31 |    6 |   43 |    4 |
| 15      |   71 |           94.4 |           100.0 |         90.2 |       0.95 |   37 |    0 |   30 |    4 |
| 16      |   68 |           80.9 |            76.2 |         91.4 |       0.83 |   32 |   10 |   23 |    3 |
| 17      |   64 |           81.2 |            95.2 |         64.5 |       0.77 |   20 |    1 |   32 |   11 |

**Evaluated on**: May 19, 2025


## Configuration 2 (`1e1a9c9`)

**Parameters**:

- `model`: gpt-4o


Not yet evaluated.


## Configuration 3 (`3bb2eb2`)

**Parameters**:

- `model`: gpt-4-turbo


Not yet evaluated.

