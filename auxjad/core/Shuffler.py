import copy
import random
import abjad
from ..utilities.remove_repeated_time_signatures import (
    remove_repeated_time_signatures
)
from ..utilities.simplified_time_signature_ratio import (
    simplified_time_signature_ratio
)


class Shuffler:
    r"""Shuffler takes an input ``abjad.Container`` and shuffles its logical
    ties. It can also shuffle only pitches, as well as rotate them. When
    shuffling or rotating pitches only, tuplets are allowed. Tuplets are not
    supported when shuffling leaves.

    ..  container:: example

        Calling the object will output a shuffled selection of the input
        container.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }

        .. figure:: ../_images/image-Shuffler-1.png

        To get the result of the last operation, use the property
        ``current_window``.

        >>> music = shuffler.current_window
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            d'4
            c'4
            f'4
            e'4
        }

        .. figure:: ../_images/image-Shuffler-2.png

    ..  container:: example

        Calling the object outputs the same result as using the method
        ``shuffle()``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.shuffle()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            f'4
            c'4
            e'4
            d'4
        }

        .. figure:: ../_images/image-Shuffler-3.png

    ..  container:: example

        This class has many keyword arguments, all of which can be altered
        after instantiation using properties with the same names as shown
        below.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 |"
        ...                             r"\time 2/4 f'4 g'4 |"
        ...                             )
        >>> shuffler = auxjad.Shuffler(container,
        ...                            output_single_measure=False,
        ...                            disable_rewrite_meter=False,
        ...                            force_time_signatures=False,
        ...                            omit_time_signatures=False,
        ...                            )
        >>> shuffler.output_single_measure
        False
        >>> shuffler.disable_rewrite_meter
        False
        >>> shuffler.force_time_signatures
        False
        >>> shuffler.omit_time_signatures
        False
        >>> shuffler.output_single_measure = True
        >>> shuffler.disable_rewrite_meter = True
        >>> shuffler.force_time_signatures = True
        >>> shuffler.omit_time_signatures = True
        >>> shuffler.output_single_measure
        True
        >>> shuffler.disable_rewrite_meter
        True
        >>> shuffler.force_time_signatures
        True
        >>> shuffler.omit_time_signatures
        True


    ..  container:: example

        If ``output_single_measure`` is set to ``True``, then the whole
        container is output as a single measure, having its time signature
        rewritten.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 |"
        ...                             r"\time 2/4 f'4 g'4"
        ...                             )
        >>> shuffler = auxjad.Shuffler(container,
        ...                            output_single_measure=True,
        ...                            )
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            f'4
            d'4
            e'4
            g'4
            c'4
        }

        .. figure:: ../_images/image-Shuffler-4.png

    ..  container:: example

        If ``disable_rewrite_meter`` is set to ``True``, then the automatic
        behaviour of rewriting the leaves according to the meter is disabled.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 |"
        ...                             r"\time 2/4 f'2"
        ...                             )
        >>> shuffler = auxjad.Shuffler(container,
        ...                            output_single_measure=True,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            d'4..
            f'2
            c'16
            e'4
        }

        .. figure:: ../_images/image-Shuffler-5.png

    ..  container:: example

        The first call to the instance will add the correct time signature to
        the first leaf. Subsequent calls will only add it if its necessary,
        such as when there is a time signature change in some bar in the
        container.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }

        .. figure:: ../_images/image-Shuffler-6.png

        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            e'8.
            ~
            e'16
            f'4..
            ~
            f'16
            r8.
            r16
            d'4..
        }

        .. figure:: ../_images/image-Shuffler-7.png

        It is possible to force time signatures on every call using either
        optional keyword argument ``force_time_signatures``.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            force_time_signatures=True,
        ...                            )
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'4..
            r16
            r8.
            c'16
            f'2
            e'4
        }

        .. figure:: ../_images/image-Shuffler-8.png

        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'16
            e'8.
            ~
            e'16
            f'4..
            ~
            f'16
            r8.
            r16
            d'4..
        }

        .. figure:: ../_images/image-Shuffler-9.png

    ..  container:: example

        To disable time signatures altogether, initialise this class with the
        keyword argument ``omit_time_signatures`` set to ``True`` (default is
        ``False``), or change the ``omit_time_signatures`` property after
        initialisation.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. e'4 | r4 f'2")
        >>> shuffler = auxjad.Shuffler(container,
        ...                            omit_time_signatures=True,
        ...                            )
        >>> music = shuffler()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            d'4..
            e'16
            ~
            e'8.
            f'16
            ~
            f'4..
            r16
            r8.
            c'16
        }

        .. figure:: ../_images/image-Shuffler-10.png

        >>> shuffler.omit_time_signatures
        True
        >>> shuffler.omit_time_signatures = False
        >>> shuffler.omit_time_signatures
        False

    ..  container:: example

        To output several shuffled containers at once, use the ``output_n``
        method, inputting the desired number of iterations.

        >>> container = abjad.Container(r"\time 2/4 c'16 d'4.. | r4 e'8. f'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.output_n(3)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            d'4..
            f'16
            c'16
            e'8.
            r4
            d'4..
            e'16
            ~
            e'8
            f'16
            r16
            r8.
            c'16
            r4
            d'4
            ~
            d'8.
            f'16
            c'16
            e'8.
        }

        .. figure:: ../_images/image-Shuffler-11.png

    ..  container:: example

        To shuffle only pitches, keeping the durations of the leaves as they
        are, use the method ``shuffle_pitches()``. It handles both notes and
        chords. Rests will remain at their current location.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.shuffle_pitches()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            e'16
            c'4..
            r4
            d'8.
            f'16
        }

        .. figure:: ../_images/image-Shuffler-12.png

    ..  container:: example

        When dealing with pitches, it is possible to use containers containing
        tuplets. And similarly to the method ``output_n()``, to output several
        containers with shuffled pitches, use ``output_n_shuffled_pitches()``.

        >>> container = abjad.Container(r"\times 2/3 {\time 5/4 c'4 d'2}"
        ...                             r"r4 e'4. f'8"
        ...                             )
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.output_n_shuffled_pitches(3)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                \time 5/4
                f'4
                e'2
            }
            r4
            d'4.
            c'8
            \times 2/3 {
                d'4
                c'2
            }
            r4
            f'4.
            e'8
            \times 2/3 {
                d'4
                f'2
            }
            r4
            c'4.
            e'8
        }

        .. figure:: ../_images/image-Shuffler-13.png

    ..  container:: example

        To rotate pitches, use the ``rotate_pitches()`` method.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.rotate_pitches()
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            d'16
            e'4..
            r4
            f'8.
            c'16
        }

        .. figure:: ../_images/image-Shuffler-14.png

    ..  container:: example

        This method can take two optioanl keyword arguments: ``anticlockwise``,
        set to ``False`` by default, and ``n_rotations``, set to 1 by default.
        The first defines the direction of the rotation, while the later sets
        the number of rotations applied.

        >>> container = abjad.Container(r"\time 3/4 c'16 d'4.. | r4 e'8. f'16")
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.rotate_pitches(anticlockwise=True, n_rotations=2)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            e'16
            f'4..
            r4
            c'8.
            d'16
        }

        .. figure:: ../_images/image-Shuffler-15.png

    ..  container:: example

        Similarly to the method ``output_n()``, to output several containers
        with rotated pitches, use ``output_n_rotated_pitches()``.

        >>> container = abjad.Container(r"\times 2/3 {\time 5/4 c'4 d'2}"
        ...                             r"r4 e'4. f'8"
        ...                             )
        >>> shuffler = auxjad.Shuffler(container)
        >>> music = shuffler.output_n_rotated_pitches(3)
        >>> staff = abjad.Staff(music)
        >>> abjad.f(staff)
        \new Staff
        {
            \times 2/3 {
                \time 5/4
                d'4
                e'2
            }
            r4
            f'4.
            c'8
            \times 2/3 {
                e'4
                f'2
            }
            r4
            c'4.
            d'8
            \times 2/3 {
                f'4
                c'2
            }
            r4
            d'4.
            e'8
        }

        .. figure:: ../_images/image-Shuffler-16.png

    ..  container:: example

        Use the property ``contents`` to get the input container upon which the
        shuffler operates. Notice that ``contents`` remains invariant after
        any shuffling or rotation operations (use ``current_window`` for the
        transformed selection of music). ``contents`` can be used to change the
        ``abjad.Container`` to be shuffled.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> shuffler = auxjad.Shuffler(container)
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Shuffler-17.png

        >>> shuffler()
        >>> abjad.f(shuffler.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Shuffler-18.png

        >>> shuffler.contents = abjad.Container(r"cs2 ds2")
        >>> abjad.f(shuffler.contents)
        {
            cs2
            ds2
        }

        .. figure:: ../_images/image-Shuffler-19.png
    """

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 output_single_measure: bool = False,
                 disable_rewrite_meter: bool = False,
                 force_time_signatures: bool = False,
                 omit_time_signatures: bool = False,
                 ):
        self.contents = contents
        self._update_logical_ties()
        self._find_time_signatures()
        self.output_single_measure = output_single_measure
        self.disable_rewrite_meter = disable_rewrite_meter
        self.force_time_signatures = force_time_signatures
        self.omit_time_signatures = omit_time_signatures
        self._last_time_signature = None

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Outputs the representation of ``contents``.'
        return str(abjad.f(self._current_window))

    def __len__(self) -> int:
        r'Outputs the number of logical ties of ``contents``.'
        return len(self._logical_ties)

    def __call__(self) -> abjad.Selection:
        r'Calls the shuffling process, returning an ``abjad.Container``'
        return self.shuffle()

    ### PUBLIC METHODS ###

    def shuffle(self) -> abjad.Selection:
        r'Shuffles the logical ties of ``contents``.'
        if self._force_time_signatures:
            self._last_time_signature = None
        dummy_container = abjad.Container()
        indeces = list(range(self.__len__()))
        random.shuffle(indeces)
        for index in indeces:
            logical_tie = copy.deepcopy(
                self._logical_ties[index])
            dummy_container.append(logical_tie)
            for leaf in logical_tie:
                if abjad.inspect(leaf).effective(abjad.TimeSignature):
                    abjad.detach(abjad.TimeSignature, leaf)
        if not self._output_single_measure:
            # splitting leaves at bar line points
            abjad.mutate(dummy_container[:]).split(
                self._time_signatures_durations,
                cyclic=True,
            )
            # attaching time signature structure
            time_signature = self._time_signatures[0]
            if (not self._last_time_signature
                    or time_signature != self._last_time_signature):
                abjad.attach(time_signature, dummy_container[0])
                self._last_time_signature = time_signature
            duration = abjad.inspect(dummy_container[0]).duration()
            index = 1
            for leaf in abjad.select(dummy_container).leaves()[1:]:
                if duration % self._time_signatures[index - 1].duration == 0:
                    time_signature = self._time_signatures[index]
                    if time_signature != self._last_time_signature:
                        abjad.attach(time_signature, leaf)
                        self._last_time_signature = time_signature
                    if index + 1 < len(self._time_signatures):
                        index += 1
                        duration = abjad.Duration(0)
                    else:
                        break
                duration += abjad.inspect(leaf).duration()
            remove_repeated_time_signatures(dummy_container)
            self._last_time_signature = self._time_signatures[-1]
        else:
            time_signature = abjad.TimeSignature(
                abjad.inspect(dummy_container).duration())
            time_signature = simplified_time_signature_ratio(time_signature)
            if (not self._last_time_signature
                    or time_signature != self._last_time_signature):
                abjad.attach(time_signature, dummy_container[0])
            self._last_time_signature = time_signature
        # rewrite meter
        if not self._disable_rewrite_meter:
            start = 0
            duration = abjad.Duration(0)
            index = 0
            dummy_container_leaves = abjad.select(dummy_container).leaves()
            for leaf_n in range(len(dummy_container_leaves)):
                duration = abjad.inspect(
                    dummy_container_leaves[start : leaf_n+1]).duration()
                if duration == self._time_signatures_durations[index]:
                    abjad.mutate(
                        dummy_container_leaves[start : leaf_n+1]
                    ).rewrite_meter(self._time_signatures[index])
                    if index + 1 < len(self._time_signatures):
                        index += 1
                        start = leaf_n + 1
                    else:
                        break
        # output
        self._current_window = dummy_container[:]
        dummy_container[:] = []
        return self.current_window

    def shuffle_pitches(self) -> abjad.Selection:
        r'Shuffles only the pitches of ``contents``.'
        if self._force_time_signatures:
            self._last_time_signature = None
        pitches = self._get_pitch_list()
        # shuffling (while preserving rests)
        true_pitches = [pitch for pitch in pitches if pitch is not None]
        random.shuffle(true_pitches)
        index = 0
        for true_pitch in true_pitches:
            while not pitches[index]:
                index += 1
            pitches[index] = true_pitch
            index += 1
        # rewriting leaves
        self._rewrite_pitches(pitches)
        self._last_time_signature = self._time_signatures[-1]
        self._update_logical_ties()
        # updating logical ties
        return self.current_window

    def rotate_pitches(self,
                       *,
                       n_rotations: int = 1,
                       anticlockwise: bool = False,
                       ) -> abjad.Selection:
        r'Rotates the pitches of ``contents``.'
        if not isinstance(n_rotations, int):
            raise TypeError("'n_rotations' must be 'int'")
        if n_rotations < 1:
            raise ValueError("'n_rotations' must be greater than zero")
        if not isinstance(anticlockwise, bool):
            raise TypeError("'anticlockwise' must be 'bool'")
        if self._force_time_signatures:
            self._last_time_signature = None
        pitches = self._get_pitch_list()
        # rotating pitches (while preserving rests)
        true_pitches = [pitch for pitch in pitches if pitch is not None]
        for _ in range(n_rotations):
            if not anticlockwise:
                true_pitches = true_pitches[1:] + [true_pitches[0]]
            else:
                true_pitches = [true_pitches[-1]] + true_pitches[:-1]
        index = 0
        for true_pitch in true_pitches:
            while not pitches[index]:
                index += 1
            pitches[index] = true_pitch
            index += 1
        # rewriting leaves
        self._rewrite_pitches(pitches)
        self._last_time_signature = self._time_signatures[-1]
        # updating logical ties
        return self.current_window

    def output_n(self,
                 n: int,
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the shuffling process and outputs
        a single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.__call__())
        remove_repeated_time_signatures(dummy_container)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def output_n_shuffled_pitches(self,
                                  n: int,
                                  ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the pitch shuffling process and
        outputs a single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("argument must be 'int'")
        if n < 1:
            raise ValueError("argument must be greater than zero")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.shuffle_pitches())
        remove_repeated_time_signatures(dummy_container)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def output_n_rotated_pitches(self,
                                 n: int,
                                 *,
                                 n_rotations: int = 1,
                                 anticlockwise: bool = False,
                                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the pitch rotation process and
        outputs a single ``abjad.Selection``.
        """
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n < 1:
            raise ValueError("first positional argument must be a positive "
                             "'int'")
        if not isinstance(n_rotations, int):
            raise TypeError("'n_rotations' must be 'int'")
        if not isinstance(anticlockwise, bool):
            raise TypeError("'anticlockwise' must be 'bool'")
        dummy_container = abjad.Container()
        for _ in range(n):
            dummy_container.append(self.rotate_pitches(
                n_rotations=n_rotations,
                anticlockwise=anticlockwise,
            ))
        remove_repeated_time_signatures(dummy_container)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    ### PRIVATE METHODS ###

    def _find_time_signatures(self):
        r"""Creates a list of all time signatures for all measures of
        ``contents``.
        """
        self._time_signatures = []
        leaves = abjad.select(self._current_window).leaves()
        duration = abjad.Duration(0)
        time_signature = abjad.inspect(
            leaves[0]).effective(abjad.TimeSignature)
        if not time_signature:
            time_signature = abjad.TimeSignature((4, 4))
        for leaf in leaves:
            if duration % time_signature.duration == 0:
                time_signature = abjad.inspect(
                    leaf).effective(abjad.TimeSignature)
                if time_signature:
                    duration = abjad.Duration(0)
                elif leaf is leaves[0]:
                    time_signature = abjad.TimeSignature((4, 4))
                else:
                    time_signature = self._time_signatures[-1]
                self._time_signatures.append(time_signature)
            duration += abjad.inspect(leaf).duration()
        self._time_signatures_durations = [timesig.duration for timesig
                                           in self._time_signatures]

    def _update_logical_ties(self):
        r'Updates the selection of logical ties of ``contents``.'
        self._logical_ties = abjad.select(self._current_window).logical_ties()

    def _get_pitch_list(self) -> list:
        r'Creates a list of all pitches in ``contents``.'
        pitches = []
        for logical_tie in abjad.select(self._current_window).logical_ties():
            leaf = logical_tie[0]
            if isinstance(leaf, abjad.Rest):
                pitches.append(None)
            elif isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.append(leaf.written_pitches)
        return pitches

    def _rewrite_pitches(self,
                         pitches: list,
                         ):
        r'Rewrites the pitches of all logical ties given a list of pitches.'
        index = 0
        dummy_container = abjad.Container(
            abjad.mutate(self._current_window[:]).copy()
        )
        logical_ties = abjad.select(dummy_container).logical_ties()
        for pitch, logical_tie in zip(pitches, logical_ties):
            for leaf in logical_tie:
                if not pitch:
                    new_leaf = abjad.Rest(leaf.written_duration)
                elif isinstance(pitch, abjad.PitchSegment):
                    new_leaf = abjad.Chord(pitch, leaf.written_duration)
                else:
                    new_leaf = abjad.Note(pitch, leaf.written_duration)
                for indicator in abjad.inspect(leaf).indicators():
                    if not pitch and isinstance(indicator, (abjad.Tie,
                                                            abjad.Articulation
                                                            )):
                        continue
                    if isinstance(indicator, abjad.TimeSignature):
                        if (not self._last_time_signature
                                or indicator != self._last_time_signature):
                            abjad.attach(indicator, new_leaf)
                            self._last_time_signature = indicator
                    else:
                        abjad.attach(indicator, new_leaf)
                selection = abjad.select(dummy_container).leaf(index)
                abjad.mutate(selection).replace(new_leaf)
                index += 1
        # output
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The ``abjad.Container`` to be shuffled.'
        return self._contents

    @contents.setter
    def contents(self,
                 contents: abjad.Container
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or child "
                            "class")
        self._contents = copy.deepcopy(contents)
        self._current_window = copy.deepcopy(contents)

    @property
    def output_single_measure(self) -> bool:
        r"""When ``True``, the output will be a single measure even if the
        contents of the shuffler are several measures.
        """
        return self._output_single_measure

    @output_single_measure.setter
    def output_single_measure(self,
                              output_single_measure: bool,
                              ):
        if not isinstance(output_single_measure, bool):
            raise TypeError("'output_single_measure' must be 'bool'")
        self._output_single_measure = output_single_measure

    @property
    def disable_rewrite_meter(self) -> bool:
        r"""When ``True``, the durations of the notes in the output will not be
        rewritten by the ``rewrite_meter`` mutation.
        """
        return self._disable_rewrite_meter

    @disable_rewrite_meter.setter
    def disable_rewrite_meter(self,
                              disable_rewrite_meter: bool,
                              ):
        if not isinstance(disable_rewrite_meter, bool):
            raise TypeError("'disable_rewrite_meter' must be 'bool'")
        self._disable_rewrite_meter = disable_rewrite_meter

    @property
    def force_time_signatures(self) -> bool:
        r"""When ``True``, every call will output a selection with a time
        signature.
        """
        return self._force_time_signatures

    @force_time_signatures.setter
    def force_time_signatures(self,
                              force_time_signatures: bool,
                              ):
        if not isinstance(force_time_signatures, bool):
            raise TypeError("'force_time_signatures' must be 'bool'")
        self._force_time_signatures = force_time_signatures

    @property
    def omit_time_signatures(self) -> bool:
        r'When ``True``, the output will contain no time signatures.'
        return self._omit_time_signatures

    @omit_time_signatures.setter
    def omit_time_signatures(self,
                             omit_time_signatures: bool,
                             ):
        if not isinstance(omit_time_signatures, bool):
            raise TypeError("'omit_time_signatures' must be 'bool'")
        self._omit_time_signatures = omit_time_signatures

    @property
    def current_window(self) -> abjad.Selection:
        r'Read-only property, returns the result of the last operation.'
        if self._omit_time_signatures:
            for leaf in abjad.select(self._current_window).leaves():
                for indicator in abjad.inspect(leaf).indicators():
                    if isinstance(indicator, abjad.TimeSignature):
                        abjad.detach(indicator, leaf)
        return copy.deepcopy(self._current_window)
