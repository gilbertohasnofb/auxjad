import abjad

from ..inspections.selection_is_full import selection_is_full
from ..inspections.underfull_duration import underfull_duration
from .time_signature_extractor import time_signature_extractor


def fill_with_rests(container: abjad.Container,
                    *,
                    disable_rewrite_meter: bool = False,
                    ):
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function fills a container with
    rests in order to make it full.

    Basic usage:
        Returns the missing duration of the last measure of any container or
        child class. If no time signature is encountered, it uses LilyPond's
        convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.fill_with_rests(container1)
        >>> auxjad.fill_with_rests(container2)
        >>> auxjad.fill_with_rests(container3)
        >>> auxjad.fill_with_rests(container4)
        >>> abjad.f(container1)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-fill_with_rests-1.png

        >>> abjad.f(container2)
        {
            c'4
            d'4
            e'4
            r4
        }

        .. figure:: ../_images/image-fill_with_rests-2.png

        >>> abjad.f(container3)
        {
            c'4
            d'4
            e'4
            f'4
            c'4
            r2.
        }

        .. figure:: ../_images/image-fill_with_rests-3.png

        >>> abjad.f(container4)
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

        .. figure:: ../_images/image-fill_with_rests-4.png

    Time signature changes:
        Handles any time signatures as well as changes of time signature.

        >>> staff1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
        >>> staff2 = abjad.Staff(r"\time 3/4 a2. \time 2/4 c'4")
        >>> staff3 = abjad.Staff(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> auxjad.fill_with_rests(staff1)
        >>> auxjad.fill_with_rests(staff2)
        >>> auxjad.fill_with_rests(staff3)
        >>> abjad.f(staff1)
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }

        .. figure:: ../_images/image-fill_with_rests-5.png

        >>> abjad.f(staff2)
        {
            \time 3/4
            a2.
            \time 2/4
            c'4
            r4
        }

        .. figure:: ../_images/image-fill_with_rests-6.png

        >>> abjad.f(staff3)
        {
            \time 5/4
            g1
            ~
            g4
            \time 4/4
            af'2
            r2
        }

        .. figure:: ../_images/image-fill_with_rests-7.png

    ..  note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'4")
        >>> auxjad.fill_with_rests(container)
        >>> abjad.f(container)
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }

        .. figure:: ../_images/image-close_container-8.png

        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2.
        }

        .. figure:: ../_images/image-close_container-9.png

    Partial time signatures:
        Correctly handles partial time signatures.

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4 g'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, staff[0])
        >>> auxjad.fill_with_rests(staff)
        >>> abjad.f(staff)
        {
            \partial 4
            \time 3/4
            c'4
            d'4
            e'4
            f'4
            g'4
            r2
        }

        .. figure:: ../_images/image-fill_with_rests-10.png

    ``disable_rewrite_meter``:
        By default, this class uses the |abjad.mutate().rewrite_meter()|
        mutation.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'8")
        >>> auxjad.fill_with_rests(staff)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'8
            ~
            d'8
            e'8
            r2
        }

        .. figure:: ../_images/image-fill_with_rests-11.png

        Call this function with the optional keyword argument
        ``disable_rewrite_meter`` set to ``True`` in order to disable this
        behaviour.

        >>> staff = abjad.Staff(r"\time 4/4 c'8 d'4 e'8")
        >>> auxjad.fill_with_rests(staff, disable_rewrite_meter=True)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'8
            d'4
            e'8
            r2
        }

        .. figure:: ../_images/image-fill_with_rests-12.png

    disable_rewrite_meter

    ..  error::

        If a container is malformed, i.e. it has an underfilled measure before
        a time signature change, the function raises a :exc:`ValueError`
        exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'4")
        >>> auxjad.fill_with_rests(container)
        ValueError: 'container' is malformed, with an underfull measure
        preceding a time signature change

    ..  warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containings
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    if not selection_is_full(container[:]):
        underfull_rests = abjad.LeafMaker()(None,
                                            underfull_duration(container[:]),
                                            )
        container.extend(underfull_rests)
    if not disable_rewrite_meter:
        time_signatures = time_signature_extractor(container,
                                                   do_not_use_none=True,
                                                   )
        measures = abjad.select(container[:]).group_by_measure()
        abjad.mutate(measures[-1]).rewrite_meter(time_signatures[-1])
