import abjad


def underfull_duration(container: abjad.Container) -> abjad.Duration:
    r"""Returns the missing ``abjad.Duration`` of an underfull container (of
    type ``abjad.Container`` or child class).

    ..  container:: example

        Returns the missing duration of the last bar of any container or child
        class. If no time signature is encountered, it uses LilyPond's
        convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.underfull_duration(container1)
        0
        >>> auxjad.underfull_duration(container2)
        1/4
        >>> auxjad.underfull_duration(container3)
        3/4
        >>> auxjad.underfull_duration(container4)
        0

    ..  container:: example

        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
        >>> auxjad.underfull_duration(container1)
        0
        >>> auxjad.underfull_duration(container2)
        0
        >>> auxjad.underfull_duration(container3)
        1/2
        >>> auxjad.underfull_duration(container4)
        1/8

    ..  container:: example

        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.underfull_duration(container)
        0

    ..  container:: example

        It also handles multi-measure rests.

        >>> container1 = abjad.Container(r"R1")
        >>> container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
        >>> container4 = abjad.Container(r"\time 6/8 R1*1/2")
        >>> auxjad.underfull_duration(container1)
        0
        >>> auxjad.underfull_duration(container2)
        0
        >>> auxjad.underfull_duration(container3)
        3/4
        >>> auxjad.underfull_duration(container4)
        1/4

    ..  warning::

        If a container is malformed, i.e. it has an underfilled bar before a
        time signature change, the function raises a ``ValueError`` exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> auxjad.underfull_duration(container)
        ValueError: 'container' is malformed, with an underfull bar preceeding
        a time signature change
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    leaves = abjad.select(container).leaves()
    # handling first leaf
    leaf = leaves[0]
    time_signature = abjad.inspect(leaf).effective(abjad.TimeSignature)
    if time_signature:
        effective_time_signature = time_signature
    else:
        effective_time_signature = abjad.TimeSignature((4, 4))
    duration = abjad.inspect(leaf).duration()
    # handling partial time signatures
    if effective_time_signature.partial:
        duration += effective_time_signature.duration
        duration -= effective_time_signature.partial
    # all other leaves
    for leaf in leaves[1:]:
        time_signature = abjad.inspect(leaf).effective(abjad.TimeSignature)
        if time_signature and time_signature != effective_time_signature:
            if duration % effective_time_signature.duration != 0:
                raise ValueError("'container' is malformed, with an underfull "
                                 "bar preceeding a time signature change")
            effective_time_signature = time_signature
            duration = abjad.Duration(0)
        duration += abjad.inspect(leaf).duration()
    duration_last_bar = duration % effective_time_signature.duration
    duration_left = duration_last_bar
    if duration_last_bar > abjad.Duration(0):
        duration_left = effective_time_signature.duration - duration_last_bar
    return duration_left
