import abjad
from .container_is_full import container_is_full
from .simplified_time_signature_ratio import simplified_time_signature_ratio
from .underfull_duration import underfull_duration


def close_container(container: abjad.Container):
    r"""Mutates an input container (of type ``abjad.Container`` or child class)
    in place and has no return value. This function changes the time signature
    of the last bar of an underfull in order to make it full.

    ..  container:: example

        Returns the missing duration of the last bar of any container or child
        class. If no time signature is encountered, it uses LilyPond's
        convention and considers the container as in 4/4.

        >>> container1 = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> container2 = abjad.Container(r"c'4 d'4 e'4")
        >>> container3 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4")
        >>> container4 = abjad.Container(r"c'4 d'4 e'4 f'4 | c'4 d'4 e'4 f'4")
        >>> auxjad.close_container(container1)
        >>> auxjad.close_container(container2)
        >>> auxjad.close_container(container3)
        >>> auxjad.close_container(container4)
        >>> abjad.f(container1)
        {
            c'4
            d'4
            e'4
            f'4
        }

        .. figure:: ../_images/image-close_container-1.png

        >>> abjad.f(container2)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
        }

        .. figure:: ../_images/image-close_container-2.png

        >>> abjad.f(container3)
        {
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            c'4
        }

        .. figure:: ../_images/image-close_container-3.png

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

        .. figure:: ../_images/image-close_container-4.png

    ..  container:: example

        Handles any time signatures as well as changes of time signature.

        >>> container1 = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
        >>> container2 = abjad.Container(r"\time 3/4 a2. \time 2/4 c'4")
        >>> container3 = abjad.Container(r"\time 5/4 g1 ~ g4 \time 4/4 af'2")
        >>> auxjad.close_container(container1)
        >>> auxjad.close_container(container2)
        >>> auxjad.close_container(container3)
        >>> abjad.f(container1)
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            g'4
        }

        .. figure:: ../_images/image-close_container-5.png

        >>> abjad.f(container2)
        {
            %%% \time 3/4 %%%
            a2.
            %%% \time 1/4 %%%
            c'4
        }

        .. figure:: ../_images/image-close_container-6.png

        >>> abjad.f(container3)
        {
            %%% \time 5/4 %%%
            g1
            ~
            g4
            %%% \time 2/4 %%%
            af'2
        }

        .. figure:: ../_images/image-close_container-7.png

    .. note::

        Notice that the time signatures in the output are commented out with
        ``%%%``. This is because Abjad only applies time signatures to
        containers that belong to a ``abjad.Staff``. The present function works
        with either ``abjad.Container`` and ``abjad.Staff``.

        >>> container = abjad.Container(r"\time 4/4 c'4 d'4 e'4 f'4 g'")
        >>> auxjad.close_container(container)
        >>> abjad.f(container)
        {
            %%% \time 4/4 %%%
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            g'4
        }
        >>> staff = abjad.Staff([container])
        >>> abjad.f(container)
        {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
            \time 1/4
            g'4
        }

    ..  container:: example

        Correctly handles partial time signatures.

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4 g'4")
        >>> time_signature = abjad.TimeSignature((3, 4), partial=(1, 4))
        >>> abjad.attach(time_signature, container[0])
        >>> auxjad.close_container(container)
        >>> abjad.f(container)
        {
            %%% \partial 4 %%%
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            f'4
            %%% \time 1/4 %%%
            g'4
        }

        .. figure:: ../_images/image-close_container-10.png

    ..  warning::

        If a container is malformed, i.e. it has an underfilled bar before a
        time signature change, the function raises a ``ValueError`` exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'4")
        >>> auxjad.close_container(container)
        ValueError: 'container' is malformed, with an underfull bar preceeding
        a time signature change
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("argument must be 'abjad.Container' or child class")
    if not container_is_full(container):
        missing_duration = underfull_duration(container)
        leaves = abjad.select(container).leaves()
        for leaf in leaves[::-1]:
            time_signature = abjad.inspect(leaf).effective(abjad.TimeSignature)
            if time_signature:
                last_time_signature = time_signature
                break
        else:
            last_time_signature = abjad.TimeSignature((4, 4))
        last_bar_duration = last_time_signature.duration - missing_duration
        final_bar_time_signature = abjad.TimeSignature(last_bar_duration)
        final_bar_time_signature = simplified_time_signature_ratio(
            final_bar_time_signature)
        duration = 0
        for leaf in leaves[::-1]:
            duration += abjad.inspect(leaf).duration()
            if duration == last_bar_duration:
                if abjad.inspect(leaf).indicators(abjad.TimeSignature):
                    abjad.detach(abjad.TimeSignature, leaf)
                abjad.attach(final_bar_time_signature, leaf)
                break
