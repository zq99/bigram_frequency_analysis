"""Analyze the position of letter bigrams in a supplied word list."""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Union

import pandas as pd


log = logging.getLogger("bigram analysis")
logging.basicConfig(level=logging.INFO)

PathLike = Union[str, Path]


class Bigram:
    """Represent a bigram found at a one-based position in a word."""

    def __init__(self, text: str, position: int) -> None:
        self.text = text
        self.position = position

    def __hash__(self) -> int:
        return hash((self.text, self.position))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bigram):
            return NotImplemented
        return (self.text, self.position) == (other.text, other.position)


def calculate_percentage(count: int, total: int) -> float:
    """Return ``count`` as a percentage of ``total``."""
    return round(100 * count / total, 2) if total > 0 else 0.0


def get_bigram_at_position(word: str, position: int) -> str:
    """Return the two characters beginning at a zero-based position."""
    return word[position : position + 2]


def export_to_csv(
    bigram_position_frequency: dict[Bigram, int],
    bigram_total_frequency: dict[str, int],
    output_file: PathLike,
) -> None:
    """Export positional bigram frequencies to a CSV file."""
    if not bigram_position_frequency or not bigram_total_frequency:
        log.warning("Data missing or incomplete; nothing exported")
        return

    output_path = Path(output_file)

    with output_path.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["text", "position", "frequency", "total", "percentage"])

        sorted_bigrams = sorted(
            bigram_position_frequency,
            key=lambda bigram: (bigram.text, bigram.position),
        )

        for bigram in sorted_bigrams:
            frequency = bigram_position_frequency[bigram]
            total = bigram_total_frequency[bigram.text]
            percentage = calculate_percentage(frequency, total)

            writer.writerow(
                [bigram.text, bigram.position, frequency, total, percentage]
            )

    log.info("Exported analysis to %s", output_path)


def generate_bigram_analysis(
    input_file: PathLike,
    output_file: PathLike,
) -> None:
    """Analyse every word in ``input_file`` and export the results."""
    input_path = Path(input_file)

    # keep_default_na=False prevents words such as "null" being interpreted
    # as missing data.
    words_df = pd.read_csv(
        input_path,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )

    bigram_position_frequency: dict[Bigram, int] = {}
    bigram_total_frequency: dict[str, int] = {}

    for value in words_df.iloc[:, 0]:
        word = value.strip()

        for position in range(len(word) - 1):
            text = get_bigram_at_position(word, position)
            bigram = Bigram(text, position + 1)

            bigram_position_frequency[bigram] = (
                bigram_position_frequency.get(bigram, 0) + 1
            )
            bigram_total_frequency[text] = bigram_total_frequency.get(text, 0) + 1

    export_to_csv(
        bigram_position_frequency,
        bigram_total_frequency,
        output_file,
    )


def main() -> None:
    """Run the analysis using the word list included with the project."""
    project_directory = Path(__file__).resolve().parent
    generate_bigram_analysis(
        input_file=project_directory / "english_words.csv",
        output_file=project_directory / "results.csv",
    )


if __name__ == "__main__":
    main()
