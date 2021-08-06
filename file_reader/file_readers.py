from pathlib import Path
from typing import Union, Iterable, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class FileReaderError(Exception):
    ...


class AbstractFileReader(ABC):
    @abstractmethod
    def __call__(self, file: Union[str, Path]) -> str:
        ...


@dataclass
class BasicFileReader:
    parser: Callable
    file_readers: Iterable[AbstractFileReader]

    def __call__(self, file: Union[str, Path]):
        for file_reader in self.file_readers:
            try:
                raw_data: str = file_reader(file=file)
                parsed_data = self.parser(raw_data)
                return parsed_data
            except FileReaderError:
                ...
        raise FileReaderError(f"Unable to read file {file!r}")
