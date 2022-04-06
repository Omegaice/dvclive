import csv
import os
import time
from collections import OrderedDict
from pathlib import Path

from dvclive.utils import nested_set

from .base import Data


class Scalar(Data):
    suffixes = [".csv", ".tsv"]
    subfolder = "scalars"

    def __init__(
        self, name: str, output_folder: str, include_timestamp: bool
    ) -> None:
        self.include_timestamp = include_timestamp
        super().__init__(name, output_folder)

    @staticmethod
    def could_log(val: object) -> bool:
        if isinstance(val, (int, float)):
            return True
        return False

    @property
    def output_path(self) -> Path:
        _path = self.output_folder / self.name
        _path.parent.mkdir(exist_ok=True, parents=True)
        return _path.with_suffix(".tsv")

    @property
    def no_step_output_path(self) -> Path:
        return self.output_path

    def first_step_dump(self) -> None:
        self.step_dump()

    def no_step_dump(self) -> None:
        pass

    def step_dump(self) -> None:
        d = OrderedDict()
        if self.include_timestamp:
            d["timestamp"] = int(time.time() * 1000)
        d["step"] = self.step
        d[self.name] = self.val

        existed = self.output_path.exists()
        with open(self.output_path, "a") as fobj:
            writer = csv.DictWriter(fobj, d.keys(), delimiter="\t")

            if not existed:
                writer.writeheader()

            writer.writerow(d)

    @property
    def summary(self):
        d = {}
        nested_set(d, os.path.normpath(self.name).split(os.path.sep), self.val)
        return d
