# chatgpt_meike

Classify texts by SDG using ChatGPT.

The prompt does not include examples for each SDG. Instead of relying on GPT's knowledge of SDGs,
it provides the descriptions of all SDGs.

Response is in JSON format.

## Parameters

No parameters used.




## Evaluation

The table below shows the accuracy (in %) for all configurations.

|   Configuration |   All |   SDG 7 |   SDG 10 |
|----------------:|------:|--------:|---------:|
|               1 | 92.55 |      93 |     91.8 |


## Configuration 1 (`99914b9`)

**Parameters**:
 None




| SDG   |   n |   Accuracy (%) |   Precision (%) |   Recall (%) |   F1 Score |   TP |   FP |   TN |   FN |
|:------|----:|---------------:|----------------:|-------------:|-----------:|-----:|-----:|-----:|-----:|
| All   | 161 |          92.55 |           92.41 |        92.41 |       0.92 |   73 |    6 |   76 |    6 |
| 7     | 100 |          93    |           89.09 |        98    |       0.93 |   49 |    6 |   44 |    1 |
| 10    |  61 |          91.8  |          100    |        82.76 |       0.91 |   24 |    0 |   32 |    5 |

**Evaluated on**: April 25, 2024

