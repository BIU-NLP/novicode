from typing import List
import pandas as pd
import os
from pathlib import Path
from synthetics.entity import Entity


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def print_sample_to_console(samples: List[Entity]):
    for index, s in enumerate(samples):
        print(f"{index+1}) Sample:")
        print(f"Text:\n{s.get('text')}\n")
        print(f"Code:\n{s.get('code')}\n")
        print("-------------------------------")


def print_sample_to_file(samples: List[Entity], output_file: str, append: bool = False):
    # create dir if does not exist
    base_path = os.path.dirname(output_file)
    Path(base_path).mkdir(parents=True, exist_ok=True)

    # write/append file
    mode = "a" if append else "w"
    compression = "gzip" if Path(output_file).suffix == ".gz" else None
    header = False if mode == "a" else True
    samples_df = pd.DataFrame(samples)
    samples_df.to_csv(
        output_file,
        mode=mode,
        header=header,
        index=False,
        compression=compression,
    )
    print(f"Succesfully saved samples to {output_file}")
