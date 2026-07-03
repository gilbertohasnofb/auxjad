import copy
from typing import Any, Iterator


class DeBruijnGenerator:
    r"""
    An implementation of the De Bruijn Sequence and Universal Cycle Constructions generators,
    based on research by Joseph Sawada, Dennis Wong, Aaron Williams, Daniel Gabric. Original C
    implementation of algorithms PCR1 (GrandDaddy) and PCR2 (GrandMama) by Joseph Sawada, 2015-2018.
    This class can be used to generate sequences of elements from an input :obj:`list` in which
    every combination of :math:`n` elements from an alphabet of size :math:`k` are present.

    E.g. for :math:`n=2` and :math:`k=3`, a possible construction of this sequence is:

    .. math::

        0010211220

    The sequence above contains every combination of 2 elements of the alphabet exactly once:

    .. math::

        00 \rightarrow 01 \rightarrow 10 \rightarrow 02 \rightarrow 21 \rightarrow 11 \rightarrow 12
        \rightarrow 22 \rightarrow 20

    This implementation is based on the code by Joseph Sawada, who generously shares it in his
    website https://debruijnsequence.org as well as granted permission for it to be used  as the
    basis for this Python implementation.

    Basic usage:
        The generator should be initialised with a :obj:`list` of objects and the attribute
        :attr:`order`. The elements of this :obj:`list` can be of any type.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.contents
        [0, 1, 2]
        >>> db_generator.order
        2
        >>> db_generator.algorithm
        "pcr1"
        >>> db_generator.cyclic
        False
        >>> db_generator.sequence_length
        10
        >>> db_generator.previous_element
        None

        Calling the generator will output the next element of the de Bruijn sequence.

        >>> db_generator()
        0
        >>> db_generator()
        0
        >>> db_generator()
        1
        >>> db_generator.previous_element
        1
        >>> db_generator.last_selected_index_of_sequence
        2

    :func:`len()` function:
        Applying the :func:`len()` function to the generator returns the length of :attr:`contents`.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> len(db_generator)
        3

    :meth:`output_all`:
        Use :meth:`output_all` to output the full de Bruijn sequence as a :obj:`list` in a single
        call. By default, the sequence is linear (i.e. :attr:`cyclic` is ``False``).

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

    ..  note::

        If :attr:`cyclic`: is set to ``False``, the generator must be reset using :meth:`reset` if
        the sequence is finished.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]
        >>> db_generator.output_all()
        StopIteration: sequence has been exhausted
        >>> db_generator.reset()
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

        However, if :attr:`cyclic`: is set to ``True``, multiple calls will cycle through the
        sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

    :meth:`output_n`:
        Use :meth:`output_n` to output the next ``n`` elements of the de Bruijn sequence as a
        :obj:`list`.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.output_n(3)
        [0, 0, 1]
        >>> db_generator.output_n(3)
        [0, 2, 1]

    ..  note::

        If the generator has output some subgroups before via direct call or the :meth:`output_n`
        method, then :meth:`output_all` will output all *remaining* elements, not from the
        beginning.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.output_n(3)
        [0, 0, 1]
        >>> db_generator.output_all()
        [0, 2, 1, 1, 2, 2, 0]

        If you want to output the full sequence after previous calls have been made, simply reset
        the object.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.output_n(3)
        [0, 0, 1]
        >>> db_generator.reset()
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

    ..  note::

        If :attr:`cyclic` is set to ``True``, :meth:`output_n` is allowed to wrap around outputting
        more elements than there are in the sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        >>> db_generator.output_n(20)
        StopIteration: sequence has been exhausted
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.output_n(20)
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0, 0, 1, 0, 2, 1, 1, 2, 2, 0, 0]

    :meth:`reset`:
        Use the :meth:`reset` method to reset the generator to its initial state. This can be used
        to restart the process at any time.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        >>> db_generator.output_n(4)
        [0, 0, 1, 0]
        >>> db_generator.output_n(4)
        [2, 1, 1, 2]
        >>> db_generator.reset()
        >>> db_generator.output_n(4)
        [0, 0, 1, 0]

    :attr:`cyclic`:
        By default, :attr:`cyclic` is ``False``, meaning the output sequence is linear and contains
        all :math:`k^n` subgroups as explicit consecutive substrings. Setting :attr:`cyclic` to
        ``True`` produces a shorter cyclic sequence where the final subgroups are implicit via
        wraparound.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

    Using as iterator:
        The instances of this class can also be used as an iterator, which can then be used in a for
        loop to exhaust the sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        >>> for element in db_generator:
        ...     element
        0
        0
        1
        0
        2
        1
        1
        2
        2
        0

    ..  warning::

        Please note that using an iterator in a loop with :attr:`cyclic`: set to ``True`` will
        result in an infinite generation of elements. It will then be necessary to manually exit the
        loop.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        >>> for element in db_generator:
        ...     element
        0
        0
        1
        1
        0
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        >>> for i, element in enumerate(db_generator):
        ...     if i == 10:
        ...         break
        ...     element
        0
        0
        1
        1
        0
        0
        1
        1
        0
        0

    :attr:`offset`:
        Rotates the output de Bruijn sequence by a number of indeces.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.sequence
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, offset=3)
        >>> db_generator.sequence
        [0, 2, 1, 1, 2, 2, 0, 0, 1, 0]

        Offset also works with cyclic sequences:

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.sequence
        [0, 0, 1, 0, 2, 1, 1, 2, 2]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True, offset=3)
        >>> db_generator.sequence
        [0, 2, 1, 1, 2, 2, 0, 0, 1]

        If offset is larger than the sequence length or below zero, it wraps around.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        >>> db_generator.sequence
        [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, offset=3)
        >>> db_generator.sequence
        [0, 2, 1, 1, 2, 2, 0, 0, 1, 0]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, offset=15)
        >>> db_generator.sequence
        [1, 2, 2, 0, 0, 1, 0, 2, 1, 1]
        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, offset=-7)
        >>> db_generator.sequence
        [1, 0, 2, 1, 1, 2, 2, 0, 0, 1]

    :attr:`algorithm`:
        Thee are multiple algorithms which can generate de Bruijn sequences, which can be selected
        using :attr:`algorithm`. Currently, options include ``"pcr1"`` or ``"pcr2"``. Both produce
        valid de Bruijn sequences but differ for most combinations of order and alphabet size.
        :attr:`algorithm` defaults to ``"pcr1"``.

        >>> db_generator = auxjad.DeBruijnGenerator(
        ...     [0, 1, 2],
        ...     order=2,
        ...     algorithm="pcr2",
        ...     cyclic=True,
        ... )
        >>> db_generator.output_all()
        [0, 0, 1, 1, 0, 2, 1, 2, 2]

    :attr:`order`:
        The :attr:`order` can be changed after initialisation. This regenerates the sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.sequence_length
        9
        >>> db_generator.order = 3
        >>> db_generator.sequence_length
        27

    :attr:`contents`:
        The :attr:`contents` can be altered after initialisation.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.output_all()
        [0, 0, 1, 0, 2, 1, 1, 2, 2]
        >>> db_generator.contents = [10, 20, 30]
        >>> db_generator.output_all()
        [10, 10, 20, 10, 30, 20, 20, 30, 30]

    .. tip::

        Changing :attr:`contents` with a list of identical size will not reset the sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        >>> db_generator.output_n(4)
        [0, 0, 1, 0]
        >>> db_generator.contents = ["A", "B", "C"]
        >>> db_generator.output_all()
        ["C", "B", "B", "C", "C"]

    Slicing and indexing:
        Instances of this class can be indexed and sliced, allowing reading, assigning, or deleting
        values from :attr:`contents`. If These changes regenerate the sequence.

        >>> db_generator = auxjad.DeBruijnGenerator([10, 20, 30], order=2)
        >>> db_generator[1]
        20
        >>> db_generator[0:2]
        [10, 20]
        >>> db_generator[1] = 99
        >>> db_generator.contents
        [10, 99, 30]
        >>> del db_generator[2]
        >>> db_generator.contents
        [10, 99]

    Read-only properties:
        This class has a number of ready-only properties. :attr:`previous_element` returns the last
        selected element of :attr:`contents`, and :attr:`previous_element_index` returns its index
        within :attr:`contents`; :attr:`last_selected_index_of_sequence` returns the index of the
        last selected element in the de Bruijn sequence. :attr:`sequence` returns the full de Bruijn
        sequence mapped to :attr:`contents` as a :obj:`list` without any of the call functions (i.e.
        it does not exhaust the generator); finally, :attr:`sequence_length` returns the length of
        the de Bruijn sequence (remembering that :func:`len()` returns the length of
        :attr:`contents`, not the output sequence).

        >>> db_generator = auxjad.DeBruijnGenerator(["A", "B", "C"], order=2)
        >>> db_generator.output_n(3)
        ["A", "A", "B"]
        >>> db_generator.previous_element
        "B"
        >>> db_generator.previous_element_index
        1
        >>> db_generator.last_selected_index_of_sequence
        2
        >>> db_generator.sequence
        ["A", "A", "B", "A", "C", "B", "B", "C", "C", "A"]
        >>> db_generator.sequence_length
        10

    ..  tip::

        This class is agnostic towards the data types of the elements of :attr:`contents`. This also
        includes Abjad's types. Abjad's exclusive membership requirement is respected since
        :func:`copy.deepcopy` is applied to any element being output.

        >>> db_generator = auxjad.DeBruijnGenerator(
        ...     [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8")],
        ...     order=2,
        ...     cyclic=True,
        ... )
        >>> notes = db_generator.output_all()
        >>> notes
        [abjad.Note("c'8"), abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("c'8"),
        abjad.Note("e'8"), abjad.Note("d'8"), abjad.Note("d'8"), abjad.Note("e'8"),
        abjad.Note("e'8")]
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'8
                c'8
                d'8
                c'8
                e'8
                d'8
                d'8
                e'8
                e'8
            }

        ..  figure:: ../_images/DeBruijnGenerator-gPsjYD6RZm.png
    """

    # ---------- CLASS VARIABLES ----------

    __slots__ = (
        "_contents",
        "_order",
        "_algorithm",
        "_cyclic",
        "_offset",
        "_sequence",
        "_sequence_length",
        "_last_selected_index_of_sequence",
        "_previous_element",
        "_previous_element_index",
    )

    _DE_BRUIJN_ALGORITHMS = ["pcr1", "pcr2"]

    # ---------- INITIALISER ----------

    def __init__(
        self,
        contents: list[Any],
        *,
        order: int,
        algorithm: str = "pcr1",
        cyclic: bool = False,
        offset: int = 0,
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
        if not isinstance(cyclic, bool):
            raise TypeError("'cyclic' must be 'bool'")
        if not isinstance(offset, int):
            raise TypeError("'offset' must be 'int'")
        # initialising using attributes, not properties, due to ordering constraints. This is
        # because self._generate_sequence() is called when setting any of the attributes below, and
        # this function requires the other attributes to have valid values.
        self._contents = contents[:]
        self._algorithm = algorithm
        self._cyclic = cyclic
        self._order = order
        self._offset = offset
        self._previous_element = None
        self._previous_element_index = None
        self._last_selected_index_of_sequence = None
        self.reset()

    # ---------- SPECIAL METHODS ----------

    def __repr__(self) -> str:
        r"""Returns interpreter representation of :attr:`contents`."""
        return str(self._contents)

    def __len__(self) -> int:
        r"""
        Returns the length of :attr:`contents`. This is the equivalent of the alphabet size of
        the de Bruijn sequence, often notated as :math:`k`.
        """
        return len(self._contents)

    def __call__(self) -> Any:
        r"""Calls the selection process and outputs one element of :attr:`contents`."""
        if self._last_selected_index_of_sequence is None:
            next_index = 0
        elif self.cyclic and self._done:
            next_index = 0
        else:
            next_index = self._last_selected_index_of_sequence + 1
            if next_index >= len(self._sequence):
                raise StopIteration("sequence has been exhausted")
        self._last_selected_index_of_sequence = next_index

        self._previous_element_index = self._sequence[self._last_selected_index_of_sequence]
        self._previous_element = self._contents[self._previous_element_index]

        return self.previous_element

    def __next__(self) -> Any:
        r"""Calls the selection process and outputs one element of :attr:`contents`."""
        return self.__call__()

    def __iter__(self) -> Iterator:
        r"""Returns an iterator, allowing instances to be used as iterators."""
        return self

    def __getitem__(
        self,
        key: int,
    ) -> Any:
        r"""
        Returns one or more elements of :attr:`contents` through indexing
        or slicing.
        """
        return self._contents[key]

    def __setitem__(
        self,
        key: int,
        value: Any,
    ) -> None:
        r"""
        Assigns values to one or more elements of :attr:`contents` through
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

    # ---------- PUBLIC METHODS ----------

    def output_all(self) -> list[Any]:
        r"""
        Outputs remaining elements of the de Bruijn sequence as a single :obj:`list`.

        If the generator has not been called before, returns the full sequence. If some elements
        have already been output via :meth:`__call__` or :meth:`output_n`, returns only the
        remaining elements from the current position to the end. Call :meth:`reset` first to always
        obtain the full sequence.

        Raises :exc:`StopIteration` if the sequence has been exhausted and :attr:`cyclic` is
        ``False``. If :attr:`cyclic` is ``True``, resets and returns the full sequence instead.
        """
        if self._done and not self._cyclic:
            raise StopIteration("sequence has been exhausted")
        if self._cyclic and self._last_selected_index_of_sequence == self.sequence_length - 1:
            self.reset()
        if self._last_selected_index_of_sequence is None:
            self._last_selected_index_of_sequence = self.sequence_length - 1
            return self.sequence
        output_sequence = self.sequence[self._last_selected_index_of_sequence + 1 :]
        self._last_selected_index_of_sequence = self.sequence_length - 1
        return output_sequence

    def output_n(self, n: int) -> list[Any]:
        r"""Outputs the next ``n`` elements of the de Bruijn sequence as a :obj:`list`."""
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n <= 0:
            raise ValueError("first positional argument must be a positive 'int'")
        output_list = []
        for _ in range(n):
            try:
                output_list.append(self.__call__())
            except StopIteration:
                raise StopIteration(
                    f"sequence has been exhausted after {len(output_list)} of {n} elements"
                )
        return output_list

    def reset(self) -> None:
        r"""
        Resets the generator to its initial state and regenerates the sequence.

        Resets :attr:`last_selected_index_of_sequence` to ``None`` and clears
        :attr:`previous_element` and :attr:`previous_element_index`. Regenerates :attr:`sequence` by
        calling :meth:`_generate_sequence`. This method is called automatically whenever
        :attr:`contents`, :attr:`order`, :attr:`algorithm`, or :attr:`cyclic` are changed.
        """
        self._last_selected_index_of_sequence = None
        self._previous_element = None
        self._previous_element_index = None
        self._generate_sequence()
        self._offset_sequence()
        # If not cyclic, we must get the initial order - 1 elements to append at the end of the
        # sequence for both PCR1 and PCR2 algorithms.
        if not self._cyclic:
            self._sequence.extend(self._sequence[: self._order - 1])

    # ---------- PRIVATE METHODS ----------

    def _generate_sequence(self) -> None:
        r"""
        Generates the full de Bruijn sequence. Uses a specified :attr:`algorithm` for selecting
        the next symbol in the sequence, and maps it to the correct element of :attr:`contents`.

        Both PCR1 and PCR2 algorithms start with a window of length :attr:`order` filled with 0s,
        e.g. for ``order = 4`` the window is ``[0, 0, 0, 0]``. Both algorithms work by dropping the
        first item, shifting all others to the left, and appending the generated next item (where
        the difference between PCR1 and PCR2 lies). E.g. for a window ``[a, b, c, d]``, the next
        window would be ``[b, c, d, e]``. The algorithm works by fetching the first element of the
        current window (initialised with zeroes only), then generating a valid next window. When the
        newly generated window has looped back to its initial value (in the example above,
        ``[0, 0, 0, 0]``), the loop is stops. Because we first fetch the first element of a window
        at every loop before generating it, the final loop will look like this:

        - current window: ``[x, 0, 0, 0]``
        - fetches ``x`` and appends to output sequence
        - window moves ``[x, 0, 0, 0]`` :math:`\rightarrow` ``[0, 0, 0, 0]``
        - loop is terminated since we arrived at a window filled with zeroes

        At this point, if :attr:`cyclic` is set to ``True``,  the algorithm is complete and the
        output sequence thus ends with a series of ``x``'s. However,  :attr:`cyclic` is set to
        ``False``, the algorithm append order - 1 zeroes at the end of the sequence.
        """
        generator_name = "_" + self._algorithm + "_generator"
        successor_generator = getattr(self, generator_name)
        window = [0] * self._order
        self._sequence = []

        while True:
            self._sequence.append(window[0])
            next_symbol = successor_generator(window)
            window = window[1:] + [next_symbol]
            if all(symbol == 0 for symbol in window):
                break

    def _pcr1_generator(self, window: list[int]) -> int:
        r"""
        Generator of the next symbol using PCR1 (GrandDaddy) rule.

        Args:
            window (list[int]): Current sliding window of length ``order``.

        Returns:
            int: The next symbol in the sequence.
        """
        alphabet_size = self.__len__()
        max_symbol = alphabet_size - 1
        next_symbol = self._pcr1_get_next_symbol(window)

        if next_symbol is not None and window[0] == max_symbol:
            return next_symbol
        if next_symbol is not None and window[0] < max_symbol and window[0] >= next_symbol:
            return window[0] + 1
        return window[0]

    def _pcr1_get_next_symbol(self, window: list[int]) -> int | None:
        r"""
        Compute the smallest valid next symbol for the PCR1 rule (aka GrandDaddy).

        Finds the tail of the window (all elements after the leading run of max symbols, starting at
        index 1), then inlines necklace period detection to determine the smallest symbol that keeps
        the sequence lexicographically minimal.

        Args:
            window (list[int]): Current sliding window of length ``order``.

        Returns:
            int | None: The smallest valid next symbol, or None if no valid symbol exists (the
                caller function will then keep the current symbol).
        """
        alphabet_size = self.__len__()
        max_symbol = alphabet_size - 1

        first_non_max_index = 1
        while first_non_max_index < self._order and window[first_non_max_index] == max_symbol:
            first_non_max_index += 1

        if first_non_max_index == self._order:
            return 0

        tail_length = self._order - first_non_max_index
        tail = window[first_non_max_index:] + [0] * (self._order - tail_length)

        period_candidate = 0
        for i in range(1, tail_length):
            if tail[i - period_candidate - 1] > tail[i]:
                return None
            if tail[i - period_candidate - 1] < tail[i]:
                period_candidate = i

        tail[tail_length] = tail[tail_length - period_candidate - 1]
        next_symbol = tail[tail_length]

        for i in range(tail_length + 1, self._order):
            if tail[i - period_candidate - 1] < max_symbol:
                return next_symbol

        if self._order % (period_candidate + 1) == 0:
            return next_symbol
        if next_symbol < max_symbol:
            return next_symbol + 1

        return None

    def _pcr2_generator(self, window: list[int]) -> int:
        r"""
        Generator of the next symbol using PCR2 (GrandMama) rule.

        Args:
            window (list[int]): Current sliding window of length ``order``.

        Returns:
            int: The next symbol in the sequence.
        """
        largest_candidate_symbol = self._get_pcr2_largest_candidate_symbol(window)

        if largest_candidate_symbol != 0 and window[0] == largest_candidate_symbol:
            return 0
        if largest_candidate_symbol != 0 and window[0] < largest_candidate_symbol:
            return window[0] + 1
        return window[0]

    def _get_pcr2_largest_candidate_symbol(self, window: list[int]) -> int:
        r"""
        Compute the largest valid candidate symbol for the PCR2 rule (aka GrandMama).

        Scans backward from the end of the window, skipping trailing min-symbols (zeros), to find
        the index ``last_non_min_index`` (:math:`j - 1` in the original C implementation, as it uses
        base 1 for indexing) of the last non-zero symbol. Builds the rotated candidate string of
        length ``order`` with ``(order - last_non_min_index - 1)`` number of leading zeros followed
        by ``window[:last_non_min_index + 1]``, then returns the largest ``element`` (:math:`x` in
        the original C implementation) in ``{1, ..., alphabet_size - 1}`` such that substituting
        ``element`` at position ``order - last_non_min_index - 1`` produces a necklace.

        Args:
            window (list[int]): Current sliding window of length ``order``.

        Returns:
            int: The largest valid ``element``, or ``0`` if no such value exists.
        """
        alphabet_size = self.__len__()

        last_non_min_index = self._order - 1
        while last_non_min_index > 0 and window[last_non_min_index] == 0:
            last_non_min_index -= 1

        candidate = [0] * (self._order - last_non_min_index - 1) + window[: last_non_min_index + 1]

        for element in range(alphabet_size - 1, 0, -1):
            candidate[self._order - last_non_min_index - 1] = element
            if self._is_necklace(candidate):
                return element
        return 0

    def _is_necklace(self, sequence: list[int]) -> bool:
        r"""
        Return ``True`` if and only if ``sequence`` is a necklace (its own lexicographically
        minimal rotation).

        Args:
            sequence (list[int]): The sequence to test.

        Returns:
            bool: ``True`` if ``sequence`` is a necklace, ``False`` otherwise.
        """
        sequence_length = len(sequence)
        period_candidate = 0
        for i in range(1, sequence_length):
            if sequence[i - period_candidate - 1] > sequence[i]:
                return False
            if sequence[i - period_candidate - 1] < sequence[i]:
                period_candidate = i
        return sequence_length % (period_candidate + 1) == 0

    def _offset_sequence(self) -> None:
        r"""Offsets the output sequence by the value given by ``offset``."""
        normalised_offset = self._offset % self.sequence_length
        self._sequence = self._sequence[normalised_offset:] + self._sequence[:normalised_offset]

    # ---------- PUBLIC PROPERTIES ----------

    @property
    def contents(self) -> list[Any]:
        r"""
        The :obj:`list` used by the generator, mapped to the de Bruijn sequence for the output
        sequence. This is the ordered alphabet used by the de Bruijn generator.
        """
        return self._contents

    @contents.setter
    def contents(
        self,
        contents: list[Any],
    ) -> None:
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list")
        different_length = self.__len__() != len(contents)
        self._contents = contents[:]
        if different_length:
            self.reset()

    @property
    def algorithm(self) -> str:
        r"""
        Thee are multiple algorithms which can generate de Bruijn sequences. Current options
        include ``"pcr1"`` or ``"pcr2"``.
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
    def order(self) -> int:
        r"""
        The order of a de Bruijn sequence is the size of each of its subgroups, often notated
        as :math:`n`.
        """
        return self._order

    @order.setter
    def order(
        self,
        order: int,
    ) -> None:
        if not isinstance(order, int):
            raise TypeError("'order' must be 'int'")
        if order < 1:
            raise ValueError("'order' must be 1 or greater")
        self._order = order
        self.reset()

    @property
    def cyclic(self) -> bool:
        r"""
        :obj:`bool` representing whether a sequence is cycle joined or not, defaulting to
        ``False``. E.g. consider a de Bruijn sequence of order 2 and alphabet size 3, generated by
        PCR1 using a cyclic output:

        .. math::

            001021122

        Notice that the substring :math:`20` is not present in the output, but is implicit in the
        result via the cyclic joining of the end of the sequence with its own beginning. For an
        explicit sequence with all combinations (i.e. not cyclical), the output would become:

        .. math::

            0010211220

        Which truly has all combinations of order 2 (:math:`n`) for an alphabet of size 3
        (:math:`k`):

        .. math::

            00 \rightarrow 01 \rightarrow 10 \rightarrow 02 \rightarrow 21 \rightarrow 11
            \rightarrow 12 \rightarrow 22 \rightarrow 20

        It's worth noticing that for cyclical sequences:

        - The length of the output sequence is :math:`k^n`

        - The total number of subgroups is :math:`k^n - (n - 1)`

        While for non-cyclical sequences:

        - The length of the output sequence is :math:`k^n + (n - 1)`

        - The total number of subgroups is :math:`k^n`
        """
        return self._cyclic

    @cyclic.setter
    def cyclic(
        self,
        cyclic: bool,
    ) -> None:
        if not isinstance(cyclic, bool):
            raise TypeError("'cyclic' must be 'bool'")
        self._cyclic = cyclic
        self.reset()

    @property
    def offset(self) -> int:
        r"""The offset of a de Bruijn sequence rotates the output list by its value."""
        return self._offset

    @offset.setter
    def offset(
        self,
        offset: int,
    ) -> None:
        if not isinstance(offset, int):
            raise TypeError("'offset' must be 'int'")
        self._offset = offset
        self.reset()

    @property
    def previous_element_index(self) -> int | None:
        r"""
        Read-only property, returns the index in :attr:`contents` of the previously output
        element of the sequence.
        """
        return self._previous_element_index

    @property
    def previous_element(self) -> Any | None:
        r"""
        Read-only property, returns the last element output by the object mapped to
        :attr:`contents`.
        """
        if self._previous_element is None:
            return self._previous_element
        return copy.deepcopy(self._previous_element)

    @property
    def last_selected_index_of_sequence(self) -> int | None:
        r"""
        Read-only property, returns the index of the last element output by the object in the de
        Bruijn sequence (not :attr:`contents`)."""
        return self._last_selected_index_of_sequence

    @property
    def sequence(self) -> list[Any]:
        r"""Read-only property, returns the de Bruijn sequence mapped to :attr:`contents`."""
        return [copy.deepcopy(self._contents[index]) for index in self._sequence]

    @property
    def sequence_length(self) -> int:
        r"""Read-only property, returns the length of the de Bruijn sequence."""
        return len(self._sequence)

    @property
    def _done(self) -> bool:
        r"""
        :obj:`bool` indicating whether the process is done (i.e. whether the index position has
        overtaken the :attr:`contents`'s length).
        """
        if self._last_selected_index_of_sequence is None:
            return False
        return self._last_selected_index_of_sequence >= len(self._sequence) - 1
