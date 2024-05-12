# NoviCode

## About

NoviCode is a Natural Language Programming task, that translates natural language descriptions given by non-technical users and express complex goals, to an executable program that contains an intricate flow composed of API access and control structures as loops, conditions, and sequences.
This task aims to unlock the challenge of generating a complete program from a plain non-technical description we present NoviCode, a novel NL Programming task, which takes as input an API and a natural language description by a novice non-programmer, and provides an executable program as output. 

## Dataset

### Get the Data

The NoviCode evaluation dataset is hosted on HuggingFace Datasets. You can download it using the following command:

```python
from datasets import load_dataset

dataset = load_dataset("biu-nlp/NoviCode")
```

This dataset contains 150 examples of natural language descriptions and their corresponding unit tests. 
The dataset is focused on 9 domains and their inherent intents: clock, events, map, messaging, music, reminders, shopping, smart
home, and weather.

The dataset contains the following columns:
| Column    | Description |
| --------- | ----------- |
| `guid`    | A unique identifier for the example. |
| `text`    | A natural language textual instruction made by a novice non-programmers. |
| `test`    | A unit test that evaluates the correctness of the generated code. |
| `imports` | A list of imports that are required for the code to run. |

## API

To provide code frameworks that bridge the translation of NL descriptions to their respective code programs, we created an API that generically aligns spans in the user description to code data type and actions.
The generated code must correctly utilize the API endpoints and be executable, allowing us to assess its functionality by executing corresponding tests.

We provide a mock-up implementation that simulates the proposed actions in the API specifications, allows test input data seeding, and supports evaluating state changes of the underlying data model following the invoked methods.

Link your project code with the mock-up API code by using the following command:

```python
import sys
sys.path.append('path/to/novicode/src/api')
```

## Usage

To use the run the evaluation tests in the dataset, you should follow the following steps:

1. Load the dataset
2. Link with the mock-up API code

### Running the tests

At runtime, one can execute the unit test by combining the test scenario snippet, the generated code, and the assertion tests. The test scenario snippet is a description of the test case, the generated code is the output of the model, and the assertion tests are the expected results of the test case.

```python
code_insert_idx = test.find(code_embed_str)
program_code = imports
program_code += "\n"
program_code += test[:code_insert_idx]
program_code += code
program_code += "\n"
program_code += test[code_insert_idx:]
exec(program_code)
```

## Citing

If you use NoviCode in a scientific publication, we would appreciate references to the following paper:

**NoviCode: NoviCode: Generating Programs from Natural Language Utterances by Novices. Asaf Achi Mordechai, Yoav Goldberg, Reut Tsarfaty. [arXiv:1708.07747](http://arxiv.org/abs/1708.07747)**

Biblatex entry:
```latex
@online{asafam/novicode,
  author       = {Asaf Achi Mordechai and Yoav Goldberg and Reut Tsarfaty},
  title        = {NoviCode: Generating Programs from Natural Language Utterances by Novices},
  date         = {2024-05-28},
  year         = {2024},
}
```