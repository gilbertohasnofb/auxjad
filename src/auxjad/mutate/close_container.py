import abjad

from .. import get


def close_container(container: abjad.Container) -> None:
    r"""Mutates an input container (of type |abjad.Container| or child class)
    in place and has no return value; this function changes the time signature
    of the last measure of an underfull in order to make it full.

    Basic usage:
        Returns the missing duration of the last measure of any container or
        child class. If no time signature is encountered, it uses LilyPond's
        convention and considers the container as in 4/4.

        >>> container1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Staff(r"c'4 d'4 e'4")
        >>> container3 = abjad.Staff(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Staff(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.mutate.close_container(container1)
        >>> auxjad.mutate.close_container(container2)
        >>> auxjad.mutate.close_container(container3)
        >>> auxjad.mutate.close_container(container4)
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/close_container-nfnk06s90x.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/close_container-swyxwiup8pm.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \time 1/4
                c'4
            }

        ..  figure:: ../_images/close_container-mms5hiysbwe.png

        >>> abjad.show(container4)

        ..  docs::

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

        ..  figure:: ../_images/close_container-aky7avbla4w.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.close_containers(staff)
        >>> abjad.mutate.close_containers(staff)

    Time signature changes:
        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Staff(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
        >>> container2 = abjad.Staff(r"\time 3/4 a2. \time 2/4 c'4")
        >>> container3 = abjad.Staff(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> auxjad.mutate.close_container(container1)
        >>> auxjad.mutate.close_container(container2)
        >>> auxjad.mutate.close_container(container3)
        >>> abjad.show(container1)

        ..  docs::

            \new Staff
            {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
                \time 1/4
                g'4
            }

        ..  figure:: ../_images/close_container-3tgyty245cq.png

        >>> abjad.show(container2)

        ..  docs::

            \new Staff
            {
                \time 3/4
                a2.
                \time 1/4
                c'4
            }

        ..  figure:: ../_images/close_container-st5d89zofoh.png

        >>> abjad.show(container3)

        ..  docs::

            \new Staff
            {
                \time 5/4
                g1
                ~
                g4
                \time 2/4
                af'2
            }

        ..  figure:: ../_images/close_container-wd5irlm76l.png

    ..  note::

        When using |abjad.Container|'s, all time signatures in the output will
        be commented out with ``%%%.`` This is because Abjad only applies time
        signatures to containers that belong to a |abjad.Staff|. The present
        function works with either |abjad.Container| and |abjad.Staff|.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4")
        >>> abjad.show(container)

        ..  docs::

            {
                %%% \time 3/4 %%%
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/close_container-xrwkorhtl5.png

        >>> staff = abjad.Staff([container])
        >>> abjad.show(container)

        ..  docs::

            {
                \time 3/4
                c'4
                d'4
                e'4
            }

        ..  figure:: ../_images/close_container-ys6pcdlywy.png

    Partial time signatures:
        Correctly handles partial time signatures.

        >>> container = abjad.Staff(r"c'4 d'4 e'4 f'4 g'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.mutate.close_container(container)
        >>> abjad.show(container)

        ..  docs::

            \new Staff
            {
                \partial 4
                \time 3/4
                c'4
                d'4
                e'4
                f'4
                \time 1/4
                g'4
            }

        ..  figure:: ../_images/close_container-rfskjbbfnu.png

    ..  error::

        If a container is malformed, i.e. it has an underfilled measure before
        a time signature change, the function raises a :exc:`ValueError`
        exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'4")
        >>> auxjad.mutate.close_container(container)
        ValueError: 'container' is malformed, with an underfull measure
        preceding a time signature change

    ..  warning::

        The input container must be a contiguous logical voice. When dealing
        with a container with multiple subcontainers (e.g. a score containing
        multiple staves), the best approach is to cycle through these
        subcontainers, applying this function to them individually.
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not abjad.select(container).leaves().are_contiguous_logical_voice():
        raise ValueError("argument must be contiguous logical voice")
    try:
        if not get.selection_is_full(container[:]):
            missing_duration = get.underfull_duration(container[:])
            leaves = abjad.select(container).leaves()
            for leaf in leaves[::-1]:
                time_signature = abjad.get.effective(leaf, abjad.TimeSignature)
                if time_signature is not None:
                    last_time_signature = time_signature
                    break
            else:
                last_time_signature = abjad.TimeSignature((4, 4))
            last_bar_duration = last_time_signature.duration - missing_duration
            final_bar_time_signature = abjad.TimeSignature(last_bar_duration)
            final_bar_time_signature.simplify_ratio()
            duration = 0
            for leaf in leaves[::-1]:
                duration += abjad.get.duration(leaf)
                if duration == last_bar_duration:
                    if abjad.get.indicator(leaf, abjad.TimeSignature):
                        abjad.detach(abjad.TimeSignature, leaf)
                    abjad.attach(final_bar_time_signature, leaf)
                    break
    except ValueError as err:
        raise ValueError("'container' is malformed, with an underfull measure "
                         "preceding a time signature change") from err
