import copy
import random
import abjad
from ..utilities.rests_to_multimeasure_rest import rests_to_multimeasure_rest
from ..utilities.remove_empty_tuplets import remove_empty_tuplets
from ..utilities.time_signature_extractor import time_signature_extractor


class Hocketer():
    r"""Hocketer is a hocket generator. It takes an input ``abjad.Container``
    and randomly distribute its logical ties among different staves, filling
    the empty durations with rests.

    ..  container:: example

        Calling the object will return a list of ``abjad.Staff`` generated by
        the hocket process and ready to be assigned to an ``abjad.Score``. Each
        call will generate a new random hocket from the input container.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> hocketer = auxjad.Hocketer(container)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                r2
                e'4
                r4
            }
            \new Staff
            {
                c'4
                d'4
                r4
                f'4
            }
        >>

        .. figure:: ../_images/image-Hocketer-1.png

        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4
                d'4
                e'4
                r4
            }
            \new Staff
            {
                r2.
                f'4
            }
        >>

        .. figure:: ../_images/image-Hocketer-2.png

    ..  container:: example

        Alternatively, it is possible to retrieve an ``abjad.Selection`` for
        each individual voice generated by the process by indexing or slicing
        the the object itself. In the case below, the hocket process is invoked
        in the third line, and the individual selections are retrieved in the
        loop.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> hocketer = auxjad.Hocketer(container)
        >>> hocketer()
        >>> score = abjad.Score()
        >>> for selection in hocketer[:]:
        ...     staff = abjad.Staff([selection])
        ...     score.append(staff)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4
                r2.
            }
            \new Staff
            {
                r4
                d'4
                e'4
                f'4
            }
        >>

        .. figure:: ../_images/image-Hocketer-3.png

    ..  container:: example

        To get the result of the last operation, use the property
        ``current_window``.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> hocketer = auxjad.Hocketer(container)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4
                r4
                e'4
                r4
            }
            \new Staff
            {
                r4
                d'4
                r4
                f'4
            }
        >>

        .. figure:: ../_images/image-Hocketer-4.png

        >>> music = hocketer.current_window
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4
                r4
                e'4
                r4
            }
            \new Staff
            {
                r4
                d'4
                r4
                f'4
            }
        >>

        .. figure:: ../_images/image-Hocketer-5.png

    ..  container:: example

        This class has many keyword arguments, all of which can be altered
        after instantiation using properties with the same names as shown
        below.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 | f'4 g'4 a'4")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            n_voices=3,
        ...                            weights=[1, 2, 5],
        ...                            k=2,
        ...                            force_k_voices=True,
        ...                            disable_rewrite_meter=True,
        ...                            use_multimeasure_rests=False,
        ...                            )
        >>> hocketer.n_voices
        3
        >>> hocketer.weights
        [1, 2, 5]
        >>> hocketer.k
        2
        >>> hocketer.force_k_voices
        True
        >>> hocketer.disable_rewrite_meter
        True
        >>> not hocketer.use_multimeasure_rests
        False
        >>> hocketer.n_voices = 5
        >>> hocketer.weights = [1, 1, 1, 2, 7]
        >>> hocketer.k = 3
        >>> hocketer.force_k_voices = False
        >>> hocketer.disable_rewrite_meter = False
        >>> hocketer.use_multimeasure_rests = True
        >>> hocketer.n_voices
        5
        >>> hocketer.weights
        [1, 1, 1, 2, 7]
        >>> hocketer.k
        3
        >>> not hocketer.force_k_voices
        False
        >>> not hocketer.disable_rewrite_meter
        False
        >>> hocketer.use_multimeasure_rests
        True

    ..  container:: example

        Use the optional argument ``n_voices`` to set the number of different
        staves in the output (default is 2).

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container, n_voices=3)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'8
                r8
                e'8
                r8
                g'8
                r4.
            }
            \new Staff
            {
                r8
                d'8
                r4.
                a'8
                r4
            }
            \new Staff
            {
                r4.
                f'8
                r4
                b'8
                c''8
            }
        >>

        .. figure:: ../_images/image-Hocketer-6.png

    ..  container:: example

        Applying the ``len()`` function to the hocketer will return the current
        number of voices to be output by the hocketer.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 ~ | f'2 g'2")
        >>> hocketer = auxjad.Hocketer(container, n_voices=7)
        >>> len(hocketer)
        6

    ..  container:: example

        Set ``weights`` to a list of numbers (either floats or integers) to
        give different weights to each voice. By default, all voices have equal
        weight. The list in ``weights`` must have the same length as the number
        of voices. In the example below, ``weights`` is set to a list of length
        2 (matching the default two voices). The second voice has a higher
        weight to it, and receives more notes from the hocket process as
        expected.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            weights=[2.1, 5.7],
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                r8
                d'8
                r4
                g'8
                r4.
            }
            \new Staff
            {
                c'8
                r8
                e'8
                f'8
                r8
                a'8
                b'8
                c''8
            }
        >>

        .. figure:: ../_images/image-Hocketer-7.png

        Use the method ``reset_weights()`` to reset the weights back to their
        default values.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            weights=[2.1, 5.7],
        ...                            )
        >>> hocketer.weights
        [2.1, 5.7]
        >>> hocketer.reset_weights()
        >>> hocketer.weights
        [1.0, 1.0]

    ..  container:: example

        Set ``k`` to an integer representing how many times each logical tie
        is fed into the hocket process. By default, ``k`` is set to ``1``, so
        each logical tie is assigned to a single voice. Changing this to a
        higher value will increase the chance of a logical tie appearing for
        up to ``k`` different voices.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> hocketer = auxjad.Hocketer(container, n_voices=4, k=2)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4
                d'4
                e'4
                r4
            }
            \new Staff
            {
                r2
                e'4
                f'4
            }
            \new Staff
            {
                r2.
                f'4
            }
            \new Staff
            {
                r4
                d'4
                r2
            }
        >>

        .. figure:: ../_images/image-Hocketer-8.png

        It is important to note that changing ``k`` to a higher value does not
        guarantee each logical tie will appear in ``k`` different voices. By
        default, ``k`` only defines how many times each logical tie is
        processed by the hocket process, which may select the same voice more
        than once. To ensure that each logical tie appears in ``k`` unique
        voices, set the optional keyword argument ``force_k_voices`` to
        ``True`` as shown below.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            n_voices=3,
        ...                            k=2,
        ...                            force_k_voices=True,
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r8
                f'8
                g'8
                r8
                b'8
                c''8
            }
            \new Staff
            {
                r4
                e'8
                r8
                g'8
                a'8
                b'8
                c''8
            }
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                r8
                a'8
                r4
            }
        >>

        .. figure:: ../_images/image-Hocketer-9.png

    ..  error::

        Setting ``force_k_voices`` to ``True`` when ``k`` is larger than
        ``n_voices`` will raise an exception:

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container, n_voices=4, k=5)
        >>> hocketer.force_k_voices = True
        ValueError: 'force_k_voices' cannot be set to True if 'k' > 'n_voices',
        change 'k' first

    ..  container:: example

        By default, this class rewrites uses abjad's ``rewrite_meter()``
        mutation, which is necessary for cleaning up the rests.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r4.
                a'8
                r4
            }
            \new Staff
            {
                r4
                e'8
                f'8
                g'8
                r8
                b'8
                c''8
            }
        >>

        .. figure:: ../_images/image-Hocketer-10.png

        Set ``disable_rewrite_meter`` to ``True`` in order to disable this
        behaviour.

        >>> container = abjad.Container(r"c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            disable_rewrite_meter=True,
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'8
                d'8
                r8
                r8
                r8
                a'8
                r8
                r8
            }
            \new Staff
            {
                r8
                r8
                e'8
                f'8
                g'8
                r8
                b'8
                c''8
            }
        >>

        .. figure:: ../_images/image-Hocketer-11.png

    ..  container:: example

        By default, this class rewrites all bars that are filled with rests,
        replacing the rests by a multi-measure rest.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
        >>> hocketer = auxjad.Hocketer(container)
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                R1 * 3/4
                r4
                g'4
                a'4
            }
            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
                f'4
                r2
            }
        >>

        .. figure:: ../_images/image-Hocketer-12.png

        Set ``use_multimeasure_rests`` to ``False`` to disable this behaviour.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'4 g'4 a'4")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            use_multimeasure_rests=False,
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 3/4
                r2.
                r4
                g'4
                a'4
            }
            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
                f'4
                r2
            }
        >>

        .. figure:: ../_images/image-Hocketer-13.png

    ..  container:: example

        Use the property ``contents`` to get the input container upon which the
        hocketer operates. Notice that ``contents`` remains invariant after
        any shuffling or rotation operations (use ``current_window`` for the
        transformed selection of music). ``contents`` can be used to change the
        ``abjad.Container`` to be shuffled.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> hocketer = auxjad.Hocketer(container)
        >>> abjad.f(hocketer.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Hocketer-14.png

        >>> hocketer()
        >>> abjad.f(hocketer.contents)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-Hocketer-15.png

        >>> hocketer.contents = abjad.Container(r"cs2 ds2")
        >>> abjad.f(hocketer.contents)
        {
            cs2
            ds2
        }

        .. figure:: ../_images/image-Hocketer-16.png

    ..  container:: example

        This function uses the default logical tie splitting algorithm from
        abjad's ``rewrite_meter()``.

        >>> container = abjad.Container(r"c'4. d'8 e'2")
        >>> hocketer = auxjad.Hocketer(container,
        ...                            n_voices=1,
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                c'4.
                d'8
                e'2
            }
        >>

        .. figure:: ../_images/image-Hocketer-17.png

        Set ``rewrite_meter_boundary_depth`` to a different number to change
        its behaviour.

        >>> hocketer = auxjad.Hocketer(container,
        ...                            n_voices=1,
        ...                            rewrite_meter_boundary_depth=1,
        ...                            )
        >>> music = hocketer()
        >>> score = abjad.Score(music)
        >>> abjad.f(staff)
        \new Score
        <<
            \new Staff
            {
                c'4
                ~
                c'8
                d'8
                e'2
            }
        >>

        .. figure:: ../_images/image-Hocketer-18.png

    ..  container:: example

        This class can handle time signature changes as well as nested tuplets.

        >>> container = abjad.Container(
        ...     r"\time 5/4 r4 \times 2/3 {c'4 d'2} e'4. f'8 "
        ...     r"\times 4/5 {\time 4/4 g'2. \times 2/3 {a'8 r8 b'2}}"
        >>> )
        >>> hocketer = auxjad.Hocketer(container,
        ...                            n_voices=4,
        ...                            k=2,
        ...                            )
        >>> staves = hocketer()
        >>> score = abjad.Score(staves)
        >>> abjad.f(score)
        \new Score
        <<
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3 {
                    c'4
                    d'2
                }
                r4.
                f'8
                \times 4/5 {
                    \time 4/4
                    r2.
                    \times 2/3 {
                        a'8
                        r8
                        r2
                    }
                }
            }
            \new Staff
            {
                \time 5/4
                R1 * 5/4
                R1
            }
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3 {
                    r4
                    d'2
                }
                e'4.
                f'8
                \times 4/5 {
                    \time 4/4
                    r2.
                    \times 2/3 {
                        a'8
                        r8
                        b'2
                    }
                }
            }
            \new Staff
            {
                \time 5/4
                r4
                \times 2/3 {
                    c'4
                    r2
                }
                r2
                \times 4/5 {
                    \time 4/4
                    g'2.
                    \times 2/3 {
                        r4
                        b'2
                    }
                }
            }
        >>

        .. figure:: ../_images/image-Hocketer-19.png
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_contents',
                 '_n_voices',
                 '_weights',
                 '_k',
                 '_force_k_voices',
                 '_disable_rewrite_meter',
                 '_use_multimeasure_rests',
                 '_voices',
                 '_time_signatures',
                 '_rewrite_meter_boundary_depth',
                 )

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 n_voices: int = 2,
                 weights: list = None,
                 k: int = 1,
                 force_k_voices: bool = False,
                 disable_rewrite_meter: bool = False,
                 use_multimeasure_rests: bool = True,
                 rewrite_meter_boundary_depth: int = None,
                 ):
        r'Initialises self.'
        self.contents = contents
        self._voices = None
        self._n_voices = n_voices
        self._k = k
        if weights is not None:
            self.weights = weights
        else:
            self.reset_weights()
        self.force_k_voices = force_k_voices
        self.disable_rewrite_meter = disable_rewrite_meter
        self.use_multimeasure_rests = use_multimeasure_rests
        self.rewrite_meter_boundary_depth = rewrite_meter_boundary_depth

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpret representation of ``contents``.'
        return format(self._contents)

    def __len__(self) -> int:
        r'Returns the number of voices of the hocketer.'
        return self._n_voices

    def __call__(self) -> list:
        r'Calls the hocket process, returning a list of ``abjad.Staff``'
        self._hocket_process()
        return [abjad.Staff([copy.deepcopy(voice)]) for voice in self._voices]

    def __getitem__(self, key: int) -> abjad.Selection:
        r"""Returns one or more voices of the output of the hocketer through
        indexing or slicing.
        """
        return copy.deepcopy(self._voices[key])

    ### PUBLIC METHODS ###

    def reset_weights(self):
        r'Resets the weight vector of all voices to an uniform distribution.'
        self._weights = [1.0 for _ in range(self.__len__())]

    ### PRIVATE METHODS ###

    def _hocket_process(self):
        r"""Runs the hocket process, returning a tuple of
        ``abjad.Container()``. It distributes the logical ties from the
        ``contents`` into different voices. Voices can have different weights,
        and the process of distributing a same logical tie can be run more than
        once (defined by the attribute ``k``).
        """
        # creating multiple copies of contents. The process actually removes
        # unwanted logical ties instead of writing them to empty containers
        dummy_voices = [copy.deepcopy(self._contents)
                        for _ in range(self._n_voices)]

        # creating a list of selected voices for each logical tie
        selected_voices = []
        if not self._force_k_voices:
            for _ in abjad.select(self._contents).logical_ties():
                item = random.choices(list(range(self._n_voices)),
                                      weights=self._weights,
                                      k=self._k,
                                      )
                selected_voices.append(item)
        else:
            for _ in abjad.select(self._contents).logical_ties():
                item = []
                while len(item) < self._k:
                    voice = random.choices(list(range(self._n_voices)),
                                           weights=self._weights,
                                           k=self._k,
                                           )[0]
                    if voice not in item:
                        item.append(voice)
                selected_voices.append(item)

        # replacing notes and chords for silences if voice not in the selected
        # list for a given logical tie
        for voice_index, voice in enumerate(dummy_voices):
            for logical_tie_index, logical_tie in \
                    enumerate(abjad.select(voice).logical_ties()):
                if voice_index not in selected_voices[logical_tie_index]:
                    for leaf in logical_tie:
                        rest = abjad.Rest(leaf.written_duration)
                        for indicator in abjad.inspect(leaf).indicators():
                            if isinstance(indicator, abjad.TimeSignature):
                                abjad.attach(indicator, rest)
                        abjad.mutate(leaf).replace(rest)

        # removing empty tuplets
        for voice in dummy_voices:
            remove_empty_tuplets(voice)

        # rewriting meter
        if not self._disable_rewrite_meter:
            for voice in dummy_voices:
                measures = abjad.select(voice[:]).group_by_measure()
                for measure, time_signature in zip(measures,
                                                   self._time_signatures):
                    abjad.mutate(measure).rewrite_meter(
                        time_signature,
                        boundary_depth=self._rewrite_meter_boundary_depth,
                    )

        # replacing rests with multi-measure rests
        if self._use_multimeasure_rests:
            for voice in dummy_voices:
                rests_to_multimeasure_rest(voice)

        # output
        self._voices = []
        for voice in dummy_voices:
            self._voices.append(voice[:])
            voice[:] = []

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The ``abjad.Container`` to be hocketed.'
        return copy.deepcopy(self._contents)

    @contents.setter
    def contents(self,
                 contents: abjad.Container
                 ):
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or child "
                            "class")
        self._contents = copy.deepcopy(contents)
        self._time_signatures = time_signature_extractor(contents,
                                                         do_not_use_none=True,
                                                         )

    @property
    def n_voices(self) -> int:
        r'Number of individual voices in the output.'
        return self._n_voices

    @n_voices.setter
    def n_voices(self,
                 n_voices: int,
                 ):
        if not isinstance(n_voices, int):
            raise TypeError("'n_voices' must be 'int'")
        if n_voices < 1:
            raise ValueError("'n_voices' must be greater than zero")
        if self._force_k_voices and self._k > n_voices:
            raise ValueError("'n_voices' cannot be smaller than 'k' when "
                             "'force_k_voices' is set to True")
        self._n_voices = n_voices

    @property
    def weights(self) -> list:
        r'The ``list`` with weights for each voice.'
        return self._weights

    @weights.setter
    def weights(self,
                weights: list,
                ):
        if not isinstance(weights, list):
            raise TypeError("'weights' must be 'list'")
        if not self.__len__() == len(weights):
            raise ValueError("'weights' must have the same length as "
                             "'n_voices'")
        if not all(isinstance(weight, (int, float))
                   for weight in weights):
            raise TypeError("'weights' elements must be 'int' or 'float'")
        self._weights = weights[:]

    @property
    def k(self) -> int:
        r'Number of random choice operations applied to a logical tie.'
        return self._k

    @k.setter
    def k(self,
          k: int,
          ):
        if not isinstance(k, int):
            raise TypeError("'k' must be 'int'")
        if k < 1:
            raise ValueError("'k' must be greater than zero")
        if self._force_k_voices and k > self._n_voices:
            raise ValueError("'k' cannot be greater than 'n_voices' when "
                             "'force_k_voices' is set to True")
        self._k = k

    @property
    def force_k_voices(self) -> bool:
        r"""When ``True``, the hocket process will ensure that each logical tie
        is distributed among ``k`` voices.
        """
        return self._force_k_voices

    @force_k_voices.setter
    def force_k_voices(self,
                       force_k_voices: bool,
                       ):
        if not isinstance(force_k_voices, bool):
            raise TypeError("'force_k_voices' must be 'bool'")
        if force_k_voices and self._k > self._n_voices:
            raise ValueError("'force_k_voices' cannot be set to True if 'k' > "
                             "'n_voices', change 'k' first")
        self._force_k_voices = force_k_voices

    @property
    def disable_rewrite_meter(self) -> bool:
        r"""When ``True``, the durations of the notes in the output will not be
        rewritten by the ``rewrite_meter`` mutation. Rests will have the same
        duration as the logical ties they replaced.
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
    def use_multimeasure_rests(self) -> bool:
        r"""When ``True``, the rests in any bars filled only with rests will be
        replaced by a multi-measure rest.
        """
        return self._use_multimeasure_rests

    @use_multimeasure_rests.setter
    def use_multimeasure_rests(self,
                              use_multimeasure_rests: bool,
                              ):
        if not isinstance(use_multimeasure_rests, bool):
            raise TypeError("'use_multimeasure_rests' must be 'bool'")
        self._use_multimeasure_rests = use_multimeasure_rests

    @property
    def rewrite_meter_boundary_depth(self) -> int:
        r"Sets the argument ``boundary_depth`` of abjad's ``rewrite_meter()``."
        return self._rewrite_meter_boundary_depth

    @rewrite_meter_boundary_depth.setter
    def rewrite_meter_boundary_depth(self,
                                     rewrite_meter_boundary_depth: int,
                                     ):
        if rewrite_meter_boundary_depth is not None:
            if not isinstance(rewrite_meter_boundary_depth, int):
                raise TypeError("'rewrite_meter_boundary_depth' must be 'int'")
        self._rewrite_meter_boundary_depth = rewrite_meter_boundary_depth

    @property
    def current_window(self) -> list:
        r'Read-only property, returns the result of the last operation.'
        if self._voices is not None:
            return [abjad.Staff([copy.deepcopy(voice)]) for voice in
                    self._voices]
        else:
            return self._voices
