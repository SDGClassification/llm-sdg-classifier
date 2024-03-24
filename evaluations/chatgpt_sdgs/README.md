# chatgpt_sdgs

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. It relies on ChatGPT's
existing knowledge of the SDGs.

Response is in JSON format.

## Parameters

No parameters used.




## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   All |   SDG 7 |   SDG 10 |
|-----------------|-------|---------|----------|
|               1 |  91.3 |      90 |    93.44 |


## Configuration 1 (`99914b9`)

**Parameters**:
 None




| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|-------|-----|----------------|-----------------|--------------|------------|------|------|------|------|
| All   | 161 |          91.3  |           87.36 |        96.2  |       0.92 |   76 |   11 |   71 |    3 |
| 7     | 100 |          90    |           83.33 |       100    |       0.91 |   50 |   10 |   40 |    0 |
| 10    |  61 |          93.44 |           96.3  |        89.66 |       0.93 |   26 |    1 |   31 |    3 |

**Evaluated on**: March 24, 2024

