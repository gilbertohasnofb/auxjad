import copy
from typing import Any, Self


class DeBruijnGenerator:
    r"""An implementation of the De Bruijn Sequence and Universal Cycle Constructions generators,
    based on research by Joseph Sawada, Dennis Wong, Aaron Williams, Daniel Gabric. Original C
    implementation of algorithms PCR1 (GrandDaddy) and PCR2 (GrandMama) by Joseph Sawada, 2015-2018.
    This class can be used to generate sequences of elements from an input :obj:`list` in which
    every combination of :math:`n` elements from an alphabet of size :math:`k` are present.

    E.g. for :math:`n=2` and :math:`k=3`, a possible construction of this sequence is:

    .. code-block::

        001021122

    The sequence above contains every combination of 2 elements of the alphabet exactly once:

    .. code-block::

        00
         01
          10
           02
            21
             11
              12
               22

    This implementation is based on the code by Joseph Sawada, who generously shares it in his
    website https://debruijnsequence.org as well as granted permission for it to be used  as the
    basis for this Python implementation.

    Basic usage:  # TODO
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_contents",
        "_order",
        "_alphabet_size",
        "_algorithm",
        "_sequence",
        "_sequence_length",
        "_sequence_last_selected_index",
        "_previous_element",
    )

    _DE_BRUIJN_ALGORITHMS = ["pcr1", "pcr2"]

    ### INITIALISER ###

    def __init__(
        self,
        contents: list[Any],
        *,
        order: int,
        algorithm: str = "pcr1",
    ) -> None:
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list'")
        if len(contents) < 2:
            raise ValueError("'contents' must be a 'list' of length 2 or greater")
        if not isinstance(order, int):
            raise TypeError("'order' must be 'int'")
        if order <= 0:
            raise ValueError("'order' must be greater than 0")
        if not isinstance(algorithm, str):
            raise TypeError("'algorithm' must be 'str'")
        if algorithm not in self._DE_BRUIJN_ALGORITHMS:
            raise ValueError(
                f"Invalid algorithm '{algorithm}', must be one of {self._DE_BRUIJN_ALGORITHMS}"
            )
        # initialising using attributes, not properties, due to cyclic dependencies, as
        # self._generate_sequence() is called when setting each of the attributes below
        self._contents = contents[:]
        self._algorithm = algorithm
        self._order = order
        self._previous_element = None
        self.reset()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r"""Returns interpreter representation of :attr:`contents`."""
        return str(self._contents)

    def __len__(self) -> int:
        r"""Returns the length of :attr:`contents`."""
        return len(self._contents)

    def __call__(self) -> Any:
        r"""Calls the selection process and outputs one element of :attr:`contents`."""
        if self._sequence_last_selected_index is None:
            self._sequence_last_selected_index = 0
        else:
            self._sequence_last_selected_index += 1
        if self._done:
            raise StopIteration("sequence has been exhausted")
        self._previous_element = self._sequence[self._sequence_last_selected_index]
        return copy.deepcopy(self._previous_element)

    def __next__(self) -> Any:
        r"""Calls the selection process and outputs one element of :attr:`contents`."""
        return self.__call__()

    def __iter__(self) -> Self:
        r"""Returns an iterator, allowing instances to be used as iterators."""
        return self

    def __getitem__(
        self,
        key: int,
    ) -> Any:
        r"""Returns one or more elements of :attr:`contents` through indexing
        or slicing.
        """
        return self._contents[key]

    def __setitem__(
        self,
        key: int,
        value: Any,
    ) -> None:
        r"""Assigns values to one or more elements of :attr:`contents` through
        indexing or slicing.
        """
        length_before_set = self.__len__()
        self._contents[key] = value
        if length_before_set != self.__len__():
            self.reset()

    def __delitem__(
        self,
        key: int,
    ) -> None:
        r"""Deletes one or more elements of :attr:`contents` through indexing or slicing."""
        del self._contents[key]
        self.reset()

    ### PUBLIC METHODS ###

    def output_all(self) -> list[Any]:
        r"""Outputs the full de Bruijn sequence as a single :obj:`list`."""
        output_list = []
        while True:
            try:
                output_list.append(self.__call__())
            except RuntimeError:
                break
        return output_list

    def output_n(self, n: int) -> list[Any]:
        r"""Outputs the next ``n`` elements of the de Bruijn sequence as a :obj:`list`."""
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 0:
            raise ValueError("argument must be a positive 'int'")
        output_list = []
        for _ in range(n):
            output_list.append(self.__call__())
        return output_list

    def reset(self) -> None:
        r"""Resets the process, regenerating the sequence."""
        self._alphabet_size = len(self._contents)
        self._sequence_last_selected_index = None
        self._generate_sequence()
        self._sequence_length = len(self._sequence)

    ### PRIVATE METHODS ###

    def _generate_sequence(self) -> None:
        r"""Generates the full de Bruijn sequence. Uses a specified :attr:`algorithm` for selecting
        the next symbol in the sequence, and maps it to the correct element of :attr:`contents`.

        Both PCR1 and PCR2 algorithms start with a window of length :attr:`order` filled with 0s,
        e.g. for ``order = 4`` the window is ``[0, 0, 0, 0]``. Both algorithms work by dropping the
        first item, shifting all others to the left, and appending the generated next item (where
        the difference between PCR1 and PCR2 lies). E.g. for a window ``[a, b, c, d]``, the next 
        window would be ``[b, c, d, e]``. The algorithm generates one of these next windows at every
        loop, and fetches only the first element for the output list. When the list has looped back
        to its initial value (in the example above, ``[0, 0, 0, 0]``), the loop is stopped. Because
        we only fetch the first element of a window at every loop, the final two loops will have
        values ``[x, 0, 0, 0]`` :math:`\rightarrow` ``[0, 0, 0, 0]``, which is why the sequence will
        end with a series of ``x``'s.
        """
        generator_name = "_" + self._algorithm + "_generator"
        successor_generator = getattr(self, generator_name)
        window = [0] * self._order
        index_sequence = []

        while True:
            index_sequence.append(window[0])
            next_symbol = successor_generator(window, self._order, self._alphabet_size)
            window = window[1:] + [next_symbol]
            if all(symbol == 0 for symbol in window):
                break

        self._sequence = [copy.deepcopy(self._contents[index]) for index in index_sequence]

    @staticmethod
    def _pcr1_generator(window: list[int], order: int, alphabet_size: int) -> int:
        r"""Generator of the next symbol using PCR1 (GrandDaddy) rule.

        Args:
            window (list[int]): Current sliding window of length ``order``.
            order (int): Order of the de Bruijn sequence.
            alphabet_size (int): Number of distinct symbols in alphabet.

        Returns:
            int: The next symbol in the sequence.
        """
        max_symbol = alphabet_size - 1
        next_symbol = DeBruijnGenerator._pcr1_get_next_symbol(window, order, alphabet_size)

        if next_symbol is not None and window[0] == max_symbol:
            return next_symbol
        if next_symbol is not None and window[0] < max_symbol and window[0] >= next_symbol:
            return window[0] + 1
        return window[0]

    @staticmethod
    def _pcr1_get_next_symbol(window: list[int], order: int, alphabet_size: int) -> int | None:
        r"""
        Compute the smallest valid next symbol for the PCR1 rule (aka GrandDaddy).

        Finds the tail of the window (all elements after the leading run of max symbols, starting at
        index 1), then inlines necklace period detection to determine the smallest symbol that keeps
        the sequence lexicographically minimal.

        Args:
            window (list[int]): Current sliding window of length ``order``.
            order (int): Order of the de Bruijn sequence.
            alphabet_size (int): Number of distinct symbols in alphabet.

        Returns:
            int | None: The smallest valid next symbol, or None if no valid symbol exists (the
                caller function will then keep the current symbol).
        """
        max_symbol = alphabet_size - 1

        first_non_max = 1
        while first_non_max < order and window[first_non_max] == max_symbol:
            first_non_max += 1

        if first_non_max == order:
            return 0

        # Pad with a leading zero so that period arithmetic (tail[i - period]) uses 1-based
        # positions, keeping i and period directly comparable with original C implementation.
        tail_length = order - first_non_max
        tail = [0] + window[first_non_max:] + [0]

        period = 1
        for i in range(2, tail_length + 1):
            if tail[i - period] > tail[i]:
                return None
            if tail[i - period] < tail[i]:
                period = i

        tail[tail_length + 1] = tail[(tail_length + 1) - period]
        next_symbol = tail[tail_length + 1]

        for i in range(tail_length + 2, order + 1):
            if tail[i - period] < max_symbol:
                return next_symbol

        if order % period == 0:
            return next_symbol
        if next_symbol < max_symbol:
            return next_symbol + 1

        return None

    @staticmethod
    def _pcr2_generator(window: list[int], order: int, alphabet_size: int) -> int:
        r"""Generator of the next symbol using PCR2 (GrandMama) rule.

        Args:
            window (list[int]): Current sliding window of length ``order``.
            order (int): Order of the de Bruijn sequence.
            alphabet_size (int): Number of distinct symbols in alphabet.

        Returns:
            int: The next symbol in the sequence.
        """
        largest_candidate_symbol = DeBruijnGenerator._get_pcr2_largest_candidate_symbol(
            window, order, alphabet_size,
        )

        if largest_candidate_symbol != 0 and window[0] == largest_candidate_symbol:
            return 0
        if largest_candidate_symbol != 0 and window[0] < largest_candidate_symbol:
            return window[0] + 1
        return window[0]

    @staticmethod
    def _get_pcr2_largest_candidate_symbol(
        window: list[int],
        order: int,
        alphabet_size: int,
    ) -> int:
        r"""
        Compute the largest valid candidate symbol for the PCR2 rule (aka GrandMama).

        Scans backward from the end of the window, skipping trailing min-symbols (zeros), to find
        the length ``last_non_min_index`` (:math:`j` in the original C implementation) of the
        meaningful suffix.  Builds the rotated candidate string of length ``order`` with
        ``(order - last_non_min_index)`` number of leading zeros followed by
        ``window[:last_non_min_index]``, then returns the largest ``element`` (:math:`x` in the
        original C implementation) in ``{1, ..., alphabet_size - 1}`` such that substituting
        ``element`` at position ``order - last_non_min_index`` produces a necklace.

        Args:
            window (list[int]): Current sliding window of length ``order``.
            order (int): Order of the de Bruijn sequence.
            alphabet_size (int): Number of distinct symbols.

        Returns:
            int: The largest valid ``element``, or ``0`` if no such value exists.
        """
        # Scan from the end of the window backward while symbols equal 0 (the min symbol). The
        # variable last_non_min_index is a 1-based count of the meaningful prefix length, and
        # window[last_non_min_index - 1] is the last non-zero symbol (or last_non_min_index stays at
        # 1 if the entire window is zero).
        last_non_min_index = order
        while last_non_min_index > 1 and window[last_non_min_index - 1] == 0:
            last_non_min_index -= 1

        # Build the rotated candidate of length order:
        # (order - last_non_min_index) leading zeros, then window[:last_non_min_index]
        candidate = [0] * (order - last_non_min_index) + window[:last_non_min_index]

        # Try element from the largest possible symbol down to 1; return the first that yields a
        # necklace. candidate[order - last_non_min_index] is the insertion point (the position of
        # element in the rotated candidate.
        for element in range(alphabet_size - 1, 0, -1):
            candidate[order - last_non_min_index] = element
            if DeBruijnGenerator._is_necklace(candidate):
                return element
        return 0

    @staticmethod
    def _is_necklace(sequence: list[int]) -> bool:
        r"""
        Return ``True`` if and only if ``sequence`` is a necklace (its own lexicographically minimal
        rotation).

        Pads with a leading zero so that period arithmetic uses 1-based positions, keeping ``i``
        and ``period_candidate`` (:math:`p` in the original C implementation) directly comparable.

        Args:
            sequence (list[int]): The sequence to test (0-based values).

        Returns:
            bool: ``True`` if ``sequence`` is a necklace, ``False`` otherwise.
        """
        n = len(sequence)
        # Pad with a leading zero so that period arithmetic in the loop below uses 1-based
        # positions, keeping i and period_candidate directly comparable
        padded_sequence = [0] + sequence
        period_candidate = 1
        for i in range(2, n + 1):
            if padded_sequence[i - period_candidate] > padded_sequence[i]:
                return False
            if padded_sequence[i - period_candidate] < padded_sequence[i]:
                period_candidate = i
        return n % period_candidate == 0

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> list[Any]:
        r"""The :obj:`list` used by the generator, mapped to the de Bruijn sequence for the output
        sequence.
        """
        return self._contents

    @contents.setter
    def contents(
        self,
        contents: list[Any],
    ) -> None:
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list")
        self._contents = contents[:]
        self.reset()

    @property
    def algorithm(self) -> str:
        r"""The :obj:`str` with the name of the algorithm. Options include ``"pcr1"`` or ``"pcr2"``.
        """
        return self._algorithm

    @algorithm.setter
    def algorithm(
        self,
        algorithm: str,
    ) -> None:
        if not isinstance(algorithm, str):
            raise TypeError("'algorithm' must be 'str'")
        if algorithm not in self._DE_BRUIJN_ALGORITHMS:
            raise ValueError(
                f"Invalid algorithm '{algorithm}', must be one of {self._DE_BRUIJN_ALGORITHMS}"
            )
        self._algorithm = algorithm
        self.reset()

    @property
    def previous_element(self) -> Any:
        r"""Returns the last element output by the object."""
        return self._previous_element

    @property
    def sequence(self) -> int:
        r"""Returns the de Bruijn sequence using ."""
        return [copy.deepcopy(self._contents[index]) for index in self._sequence]

    @property
    def sequence_length(self) -> int:
        r"""Returns the length of the de Bruijn sequence."""
        return self._sequence_length

    @property
    def sequence_last_selected_index(self) -> int:
        r"""Returns the index of the last element output by the object in the de Bruijn sequence
        (not :attr:`contents`)."""
        return self._sequence_last_selected_index

    @property
    def _done(self) -> bool:
        r""":obj:`bool` indicating whether the process is done (i.e. whether the index position has
        overtaken the :attr:`contents`'s length).
        """
        return self._sequence_last_selected_index == len(self._sequence) - 1
