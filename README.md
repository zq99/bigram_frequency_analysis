# Bigram Frequency Analysis

This project analyses where letter bigrams occur within a list of common
English words.

A bigram is a sequence of two consecutive letters. For example, `hello`
contains four bigrams:

| Bigram | Position |
|---|---:|
| `he` | 1 |
| `el` | 2 |
| `ll` | 3 |
| `lo` | 4 |

## Approach

The program reads the 9,891 entries in `english_words.csv`. For every bigram,
it records:

- how often the bigram appears at each position within a word;
- how often the bigram appears across all positions;
- the percentage of its total appearances occurring at each position.

For example, if a bigram appears 20 times in total and 5 of those appearances
are at position 1, its position-1 percentage is 25%.

Positions are one-based, so the first pair of letters in a word is at position
1.

## Running the analysis

Install the dependency:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python bigram_report.py
```

The analysis is written to `results.csv`.

## Output

The output contains the following columns:

| Column | Description |
|---|---|
| `text` | The two-letter bigram. |
| `position` | Its one-based position within a word. |
| `frequency` | The number of appearances at that position. |
| `total` | The number of appearances across all positions. |
| `percentage` | The percentage of all appearances occurring at that position. |

## Interpretation

Each word in the supplied list is counted equally. The results therefore
describe the composition of this word list; they are not estimates of bigram
frequency in ordinary English prose, where frequently used words would receive
more weight.

> This was originally written as an early Python learning project. It has since
> received minor maintenance, type annotations, and bug fixes while retaining
> its original design.
