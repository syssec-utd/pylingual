from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Iterator, List, Union
from more_itertools import peekable
from xopen import xopen
__all__ = ['ParsingError', 'FASTAItem', 'FASTAReader', 'read_fasta']

class ParsingError(Exception):
    """
    Parsing error.
    """

    def __init__(self, line_number: int):
        """
        Parameters
        ----------
        line_number
            Line number.
        """
        super().__init__(f'Line number {line_number}.')
        self._line_number = line_number

    @property
    def line_number(self) -> int:
        """
        Line number.

        Returns
        -------
        Line number.
        """
        return self._line_number

@dataclass
class FASTAItem:
    """
    FASTA item.

    Attributes
    ----------
    defline
        Description line.
    sequence
        Sequence.
    """
    defline: str
    sequence: str

    @property
    def id(self) -> str:
        """
        Identification.

        Returns
        -------
        Identification.
        """
        return self.defline.split()[0]

    @id.setter
    def id(self, val: str):
        if self.has_desc:
            self.defline = val + ' ' + self.desc
        else:
            self.defline = val

    @property
    def has_desc(self) -> bool:
        """
        Does it has description?

        Returns
        -------
        ``True`` if it does contain description; ``False`` otherwise.
        """
        return len(self.defline.split()) > 1

    @property
    def desc(self) -> str:
        """
        Description (if any).

        It will raise `RuntimeError` if it has no description.

        Returns
        -------
        Description.

        Raises
        ------
        RuntimeError
            If it has no description.
        """
        if not self.has_desc:
            raise RuntimeError('It does not have a description.')
        tgt_id = self.id
        return self.defline[len(tgt_id) + 1:]

    def __iter__(self):
        yield self.defline
        yield self.sequence

    def copy(self) -> FASTAItem:
        """
        Copy of itself.

        Returns
        -------
        FASTA item.
        """
        from copy import copy
        return copy(self)

class FASTAReader:
    """
    FASTA reader.
    """

    def __init__(self, file: Union[str, Path, IO[str]]):
        """
        Parameters
        ----------
        file
            File path or IO stream.
        """
        if isinstance(file, str):
            file = Path(file)
        if hasattr(file, 'strpath'):
            file = Path(str(file))
        if isinstance(file, Path):
            file = xopen(file, 'r')
        self._file = file
        self._lines = peekable((line for line in file))
        self._line_number = 0

    def read_item(self) -> FASTAItem:
        """
        Get the next item.

        Returns
        -------
        Next item.
        """
        defline = self._next_defline()
        sequence = self._next_sequence()
        return FASTAItem(defline, sequence)

    def read_items(self) -> List[FASTAItem]:
        """
        Get the list of all items.

        Returns
        -------
        List of all items.
        """
        return list(self)

    def close(self):
        """
        Close the associated stream.
        """
        self._file.close()

    def _next_defline(self) -> str:
        while True:
            line = next(self._lines)
            self._line_number += 1
            if line == '':
                raise StopIteration
            line = line.strip()
            if line.startswith('>'):
                return line[1:]
            if line != '':
                raise ParsingError(self._line_number)

    def _next_sequence(self) -> str:
        lines = []
        while True:
            line = next(self._lines)
            self._line_number += 1
            if line == '':
                raise ParsingError(self._line_number)
            line = line.strip()
            if not line.startswith('>'):
                lines.append(line)
                if self._sequence_continues():
                    continue
                return ''.join(lines)
            if line != '':
                raise ParsingError(self._line_number)

    def _sequence_continues(self):
        try:
            next_line = self._lines.peek()
        except StopIteration:
            return False
        if next_line == '':
            return False
        next_line = next_line.strip()
        return len(next_line) > 0 and (not next_line.startswith('>'))

    def __iter__(self) -> Iterator[FASTAItem]:
        while True:
            try:
                yield self.read_item()
            except StopIteration:
                return

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()

def read_fasta(file: Union[str, Path, IO[str]]) -> FASTAReader:
    """
    Open a FASTA file for reading.

    Parameters
    ----------
    file
        File path or IO stream.

    Returns
    -------
    FASTA reader.
    """
    return FASTAReader(file)