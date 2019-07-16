# nest
data nesting experiments

## Installation

Only Python 3.6 (or higher) is required for usage. 
For tests `pytest` is used.

Install pytest with

```
pip install -r requirements.txt
```

## Usage

Example data is prepared in file `input.txt`. 

Possible usage looks like this 
```
cat input.txt|python nest.py currency city country
```

## Tests

Run tests with 
```
pytest test.py
```