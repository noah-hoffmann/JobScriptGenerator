from .alias_handler import AliasHandler
from .options import (
    ALIASES,
    PBS_OPTIONS,
    SLURM_OPTIONS,
    PBS_L_SELECT_OPTIONS,
    PBS_L_JOB_WIDE_OPTIONS,
)

from typing import Any


class Job(AliasHandler):
    def __init__(self, **kwargs):
        super().__init__()
        for name, aliases in ALIASES.items():
            for alias in aliases:
                self.add_alias(name, alias)
        for item, value in kwargs.items():
            setattr(self, item, value)

    def hasattr(self, item) -> bool:
        return hasattr(self, item)

    def get_arguments(self, item) -> list[Any]:
        arg = getattr(self, item)
        if isinstance(arg, str):
            return [arg]
        try:
            return [arg for arg in getattr(self, item)]
        except TypeError:
            return [getattr(self, item)]

    def to_slurm(self) -> str:
        lines = ["#!/bin/bash"]

        for item in filter(self.hasattr, SLURM_OPTIONS):
            pre = "-" * min(2, len(item))
            delimiter = " " if len(item) == 1 else "="
            prefix = f"#SBATCH {pre}{item}".replace("_", "-")
            for value in self.get_arguments(item):
                lines.append(f"{prefix}{delimiter}{value}")

        return "\n".join(lines)

    def to_pbs(self) -> str:
        lines = ["#!/bin/bash"]
        for item in filter(self.hasattr, PBS_OPTIONS):
            for value in self.get_arguments(item):
                lines.append(f"#PBS -{item} {value}")
        for item in filter(self.hasattr, PBS_L_JOB_WIDE_OPTIONS):
            for value in self.get_arguments(item):
                lines.append(f"#PBS -l {item}={value}")
        select_options = list(filter(self.hasattr, PBS_L_SELECT_OPTIONS))
        if len(select_options) == 0:
            return "\n".join(lines)
        # the first found arguments has to be select containing the number of nodes
        assert select_options[0] == "select"
        n_select = len(self.get_arguments(select_options[0]))
        for i in range(n_select):
            options = []
            for option in select_options:
                try:
                    options.append(f"{option}={self.get_arguments(option)[i]}")
                except IndexError:
                    pass
            lines.append(f"#PBS -l {':'.join(options)}")

        return "\n".join(lines)
