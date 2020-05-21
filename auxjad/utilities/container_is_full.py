import abjad
from .underfull_duration import underfull_duration


def container_is_full(container: abjad.Container) -> bool:
    r"""Returns a ``bool`` representing whether an input container (of type
    ``abjad.Container`` or child class) has its last bar is fully filled in or
    not.

    ..  container:: example

        Returns ``True`` if the last bar of any container (or child class) is
        full, otherwise returns ``False``. If no time signature is encountered,
        it uses LilyPond's convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        False
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        True

    ..  container:: example

        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> container4 = abjad.Container(r"\time 6/8 c'2 ~ c'8")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        True
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        False

    ..  container:: example

        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.container_is_full(container)
        True

    ..  container:: example

        It also handles multi-measure rests.

        >>> container1 = abjad.Container(r"R1")
        >>> container2 = abjad.Container(r"\time 3/4 R1*3/4 \time 2/4 r2")
        >>> container3 = abjad.Container(r"\time 5/4 R1*5/4 \time 4/4 g''4")
        >>> container4 = abjad.Container(r"\time 6/8 R1*1/2")
        >>> auxjad.container_is_full(container1)
        True
        >>> auxjad.container_is_full(container2)
        True
        >>> auxjad.container_is_full(container3)
        False
        >>> auxjad.container_is_full(container4)
        False

    ..  warning::

        If a container is malformed, i.e. it has an underfilled bar before a
        time signature change, the function raises a ``ValueError`` exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'1")
        >>> auxjad.container_is_full(container)
        ValueError: 'container' is malformed, with an underfull bar preceeding
        a time signature change
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    return underfull_duration(container) == abjad.Duration(0)
