import abjad

from .. import get, mutate


class Repeater():
    r"""This class takes an |abjad.Container| (or child class) as input and
    outputs an |abjad.Selection| with ``n`` repetitions of it.

    Basic usage:
        Calling the object will return an |abjad.Selection| generated by the
        repeating process. The argument of :meth:`__call__()` defines the
        number of repetitions.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Repeater-tigd5dwtszh.png

        The property :attr:`current_window` can be used to access the last
        results.

        >>> notes = repeater.current_window()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Repeater-hg86wd75fvp.png

    Time signatures:
        This class handles different time signatures.

        >>> container = abjad.Staff(r"\time 3/4 c'2. \time 2/4 r2 g'2")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
            \time 3/4
            c'2.
            \time 2/4
            r2
            g'2
        }

        .. figure:: ../_images/Repeater-fqkjxhegzmv.png

    Underfull containers:
        Containers that are not fully filled in are automatically closed by
        this class in its output. Containers without a time signature are
        assumed to be in ``4/4`` (which is LilyPond's default).

        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/Repeater-k4hxxghalwh.png

        >>> container = abjad.Staff(r"\time 3/4 c'4 d'4 e'4 f'2")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            \time 2/4
            f'2
            \time 3/4
            c'4
            d'4
            e'4
            \time 2/4
            f'2
        }

        .. figure:: ../_images/Repeater-fee3qe1vdjl.png

    Using as iterator:
        The instances of this class can also be used as an iterator, which can
        then be used in a for loop. Note that unlike the methods
        :meth:`__call__()` and :meth:`output_n`, time signatures are added to
        each window returned by the shuffler. Use the function
        |auxjad.mutate.remove_repeated_time_signatures()| to clean the output
        when using this class in this way. It is also important to note that a
        ``break`` statement is needed when using this class as an iterator. The
        reason is that repeating is a process that can happen indefinitely
        (unlike some of the other classes in this library).

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> repeater = auxjad.Repeater(container)
        >>> staff = abjad.Staff()
        >>> for window in repeater:
        ...     staff.append(window)
        ...     if abjad.get.duration(staff) == abjad.Duration((9, 4)):
        ...         break
        >>> auxjad.mutate.remove_repeated_time_signatures(staff[:])
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/Repeater-8oouugbk5zc.png

    Arguments and properties:
        This class can take many optional keyword arguments during its
        creation. attr:`omit_time_signatures` will remove all time signatures
        from the output while :attr:`force_identical_time_signatures` will
        force all time signatures (including repeated ones) to be added to the
        output (both are ``False`` by default). When set to ``True``, the
        properties  :attr:`reposition_clefs`, :attr:`reposition_dynamics`, and
        :attr:`reposition_slurs` will invoke the mutations
        |auxjad.mutate.reposition_clefs()|,
        |auxjad.mutate.reposition_dynamics()|, and
        |auxjad.mutate.reposition_slurs()| (default values are ``True``).
        Check their documentation for more information on how they operate.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> repeater = auxjad.Repeater(container,
        ...                            omit_time_signatures=False,
        ...                            force_identical_time_signatures=False,
        ...                            reposition_clefs=True,
        ...                            reposition_dynamics=True,
        ...                            reposition_slurs=True,
        ...                            )
        >>> repeater.omit_time_signatures
        False
        >>> repeater.force_identical_time_signatures
        False
        >>> repeater.reposition_clefs
        True
        >>> repeater.reposition_dynamics
        True
        >>> repeater.reposition_slurs
        True

        Use the properties below to change these values after initialisation.

        >>> repeater.omit_time_signatures = True
        >>> repeater.force_identical_time_signatures = True
        >>> repeater.reposition_clefs = False
        >>> repeater.reposition_dynamics = False
        >>> repeater.reposition_slurs = False
        >>> repeater.omit_time_signatures
        True
        >>> repeater.force_identical_time_signatures
        True
        >>> repeater.reposition_clefs
        False
        >>> repeater.reposition_dynamics
        False
        >>> repeater.reposition_slurs
        False

    :attr:`contents`:
        Use the :attr:`contents` property to read as well as overwrite the
        contents of the repeater.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Repeater-f1kqq128afw.png

        >>> repeater.contents = abjad.Container(r"c'16 d'16 e'16 f'16 g'2.")
        >>> notes = repeater(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'16
            d'16
            e'16
            f'16
            g'2.
            c'16
            d'16
            e'16
            f'16
            g'2.
        }

        .. figure:: ../_images/Repeater-jblq28xlso.png

    :meth:`output_n`:
        This is an alias of :meth:`__call__()`. Takes an argument ``n`` for the
        number of repetitions.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater.output_n(2)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/Repeater-w0hd2fp2w9e.png

    :attr:`omit_time_signatures`:
        To disable time signatures altogether, initialise this class with the
        keyword argument :attr:`omit_time_signatures` set to ``True`` (default
        is ``False``), or use the :attr:`omit_time_signatures` property after
        initialisation.

        >>> container = abjad.Staff(r"c'4 d'4 e'4")
        >>> repeater = auxjad.Repeater(container,
        ...                            omit_time_signatures=True,
        ...                            )
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/Repeater-vr4af47iwjg.png

    :attr:`force_identical_time_signatures`:
        To force time signatures in all iterations of the output, initialise
        this class with the keyword argument
        :attr:`force_identical_time_signatures` set to ``True`` (default is
        ``False``), or use the :attr:`force_identical_time_signatures` property
        after initialisation.

        >>> container = abjad.Staff(r"\time 5/4 c'2. d'4 e'4")
        >>> repeater = auxjad.Repeater(container,
        ...                            force_identical_time_signatures=True,
        ...                            )
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 5/4
            c'2.
            d'4
            e'4
            \time 5/4
            c'2.
            d'4
            e'4
            \time 5/4
            c'2.
            d'4
            e'4
        }

        .. figure:: ../_images/Repeater-xgpndbdb0j.png

    Dynamics, slurs, and clefs:
        By default, this class automatically handles dynamics, slurs, and
        clefs, optimising their position and omitting repetitions.

        >>> container = abjad.Staff(r"\clef bass f4\pp( e4) d4(")
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
        }

        .. figure:: ../_images/Repeater-m1ibei9s3am.png

        This is done by invoking |auxjad.mutate.reposition_clefs()|,
        |auxjad.mutate.reposition_dynamics()|, and
        |auxjad.mutate.reposition_slurs()|. Check their documentation for
        more information on how they operate.

        >>> repeater = auxjad.Repeater(container)
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            f4
            e4
            )
            d4
            (
            f4
            e4
            )
            d4
        }

        .. figure:: ../_images/Repeater-scjj2uwz2p.png

        Set theproperties  :attr:`reposition_clefs`,
        :attr:`reposition_dynamics`, and :attr:`reposition_slurs` to ``False``
        to not invoke these mutations.

        >>> repeater = auxjad.Repeater(container,
        ...                            reposition_clefs=False,
        ...                            reposition_dynamics=False,
        ...                            reposition_slurs=False,
        ...                            )
        >>> notes = repeater(3)
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/4
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
            \clef "bass"
            f4
            \pp
            (
            e4
            )
            d4
            (
        }

        .. figure:: ../_images/Repeater-cc39a0h84dc.png

    .. error::

        If a container is malformed, i.e. it has an underfilled measure before
        a time signature change, this class will raise a :exc:`ValueError`
        exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> repeater = auxjad.Repeater(container)
        ValueError: 'contents' is malformed, with an underfull measure
        preceding a time signature change
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_contents',
                 '_current_window',
                 '_omit_time_signatures',
                 '_force_identical_time_signatures',
                 '_reposition_clefs',
                 '_reposition_dynamics',
                 '_reposition_slurs',
                 )

    ### INITIALISER ###

    def __init__(self,
                 contents: abjad.Container,
                 *,
                 omit_time_signatures: bool = False,
                 force_identical_time_signatures: bool = False,
                 reposition_clefs: bool = True,
                 reposition_dynamics: bool = True,
                 reposition_slurs: bool = True,
                 ) -> None:
        r'Initialises self.'
        self.contents = contents
        self.omit_time_signatures = omit_time_signatures
        self.force_identical_time_signatures = force_identical_time_signatures
        self.reposition_clefs = reposition_clefs
        self.reposition_dynamics = reposition_dynamics
        self.reposition_slurs = reposition_slurs

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Returns interpreter representation of  :attr:`contents`.'
        return abjad.lilypond(self._contents)

    def __call__(self,
                 n: int = 1,
                 ) -> abjad.Selection:
        r"""Calls the repeater process for ``n`` iterations, returning an
        |abjad.Selection|. Default ``n`` is ``1``.
        """
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n < 1:
            raise ValueError("first positional argument must be a positive "
                             "'int'")
        self._repeating_process(n)
        return self.current_window

    def __next__(self) -> abjad.Selection:
        r"""Calls the shuffling process for one iteration, returning an
        |abjad.Selection|.
        """
        return self.__call__()

    def __iter__(self) -> None:
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def output_n(self,
                 n: int = 1,
                 ) -> abjad.Selection:
        r"""Calls the repeater process for ``n`` iterations, returning an
        |abjad.Selection|. Default ``n`` is ``1``.
        """
        return self.__call__(n)

    ### PRIVATE METHODS ###

    def _repeating_process(self,
                           n: int,
                           ) -> None:
        r'Repeats a container ``n`` times.'
        dummy_container = abjad.mutate.copy(self._contents)
        for _ in range(n - 1):
            dummy_container.extend(abjad.mutate.copy(self._contents))
        if not self._force_identical_time_signatures:
            mutate.remove_repeated_time_signatures(dummy_container[:])
        if self._reposition_clefs:
            mutate.reposition_clefs(dummy_container[:])
        if self._reposition_clefs:
            mutate.reposition_dynamics(dummy_container[:])
        if self._reposition_clefs:
            mutate.reposition_slurs(dummy_container[:])
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    def _get_lilypond_format(self) -> str:
        r'Returns interpreter representation of  :attr:`contents`.'
        return self.__repr__()

    @staticmethod
    def _remove_all_time_signatures(container) -> None:
        r'Removes all time signatures of an |abjad.Container|.'
        for leaf in abjad.select(container).leaves():
            if abjad.get.effective(leaf, abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> abjad.Container:
        r'The |abjad.Container| to be shuffled.'
        return abjad.mutate.copy(self._contents)

    @contents.setter
    def contents(self,
                 contents: abjad.Container,
                 ) -> None:
        if not isinstance(contents, abjad.Container):
            raise TypeError("'contents' must be 'abjad.Container' or child "
                            "class")
        if not abjad.select(contents).leaves().are_contiguous_logical_voice():
            raise ValueError("'contents' must be contiguous logical voice")
        if isinstance(contents, abjad.Score):
            self._contents = abjad.mutate.copy(contents[0])
        elif isinstance(contents, abjad.Tuplet):
            self._contents = abjad.Container([abjad.mutate.copy(contents)])
        else:
            self._contents = abjad.mutate.copy(contents)
        dummy_container = abjad.mutate.copy(contents)
        try:
            if not get.selection_is_full(dummy_container[:]):
                mutate.close_container(self._contents)
                mutate.close_container(dummy_container)
        except ValueError as err:
            raise ValueError("'contents' is malformed, with an underfull "
                             "measure preceding a time signature change"
                             ) from err
        self._current_window = dummy_container[:]
        dummy_container[:] = []

    @property
    def current_window(self) -> abjad.Selection:
        r'Read-only property, returns the previously output selection.'
        current_window = abjad.mutate.copy(self._current_window)
        if self._omit_time_signatures:
            self._remove_all_time_signatures(current_window)
        return current_window

    @property
    def omit_time_signatures(self) -> bool:
        r'When ``True``, all time signatures will be omitted from the output.'
        return self._omit_time_signatures

    @omit_time_signatures.setter
    def omit_time_signatures(self,
                             omit_time_signatures: bool,
                             ) -> None:
        if not isinstance(omit_time_signatures, bool):
            raise TypeError("'omit_time_signatures' must be 'bool'")
        self._omit_time_signatures = omit_time_signatures

    @property
    def force_identical_time_signatures(self) -> bool:
        r"""When ``True``, all time signatures will be printed in the output,
        including repeated ones .
        """
        return self._force_identical_time_signatures

    @force_identical_time_signatures.setter
    def force_identical_time_signatures(
        self,
        force_identical_time_signatures: bool,
    ) -> None:
        if not isinstance(force_identical_time_signatures, bool):
            raise TypeError("'force_identical_time_signatures' must be 'bool'")
        self._force_identical_time_signatures = force_identical_time_signatures

    @property
    def reposition_clefs(self) -> bool:
        r'When ``True``, |auxjad.mutate.reposition_clefs()| is invoked.'
        return self._reposition_clefs

    @reposition_clefs.setter
    def reposition_clefs(self,
                         reposition_clefs: bool,
                         ) -> None:
        if not isinstance(reposition_clefs, bool):
            raise TypeError("'reposition_clefs' must be 'bool'")
        self._reposition_clefs = reposition_clefs

    @property
    def reposition_dynamics(self) -> bool:
        r'When ``True``, |auxjad.mutate.reposition_dynamics()| is invoked.'
        return self._reposition_dynamics

    @reposition_dynamics.setter
    def reposition_dynamics(self,
                            reposition_dynamics: bool,
                            ) -> None:
        if not isinstance(reposition_dynamics, bool):
            raise TypeError("'reposition_dynamics' must be 'bool'")
        self._reposition_dynamics = reposition_dynamics

    @property
    def reposition_slurs(self) -> bool:
        r'When ``True``, |auxjad.mutate.reposition_slurs()| is invoked.'
        return self._reposition_slurs

    @reposition_slurs.setter
    def reposition_slurs(self,
                         reposition_slurs: bool,
                         ) -> None:
        if not isinstance(reposition_slurs, bool):
            raise TypeError("'reposition_slurs' must be 'bool'")
        self._reposition_slurs = reposition_slurs
