import copy
import abjad
from .close_container import close_container
from .container_is_full import container_is_full
from .remove_repeated_time_signatures import remove_repeated_time_signatures


def repeat_container(container: abjad.Container,
                     n: int,
                     *,
                     omit_all_time_signatures: bool = False,
                     force_identical_time_signatures: bool = False,
                     ) -> abjad.Container:
    r"""This Returns an ``abjad.Container`` with n repetitions of an input
    container (of type ``abjad.Container`` or child class).

    ..  container:: example

        The required arguments are an ``abjad.Container`` (or child class) and
        and integer n for the number of repetitions.

        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> output_container = auxjad.repeat_container(container, 3)
        >>> abjad.f(output_container)
        {
            %%% \time 3/4 %%%
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

        .. figure:: ../_images/image-repeat_container-1.png

    .. note::

        Notice that the time signatures in the output are commented out with
        ``%%%``. This is because Abjad only applies time signatures to
        containers that belong to a ``abjad.Staff``. The present function works
        with either ``abjad.Container`` and ``abjad.Staff``.
        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> output_container = auxjad.repeat_container(container, 3)
        >>> abjad.f(output_container)
        {
            %%% \time 3/4 %%%
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
        >>> staff = abjad.Staff([output_container])
        >>> abjad.f(output_container)
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

    ..  container:: example

        It handle containers with multiple bars and different time signatures.

        >>> container = abjad.Container(r"\time 3/4 c'2. \time 2/4 r2 g'2")
        >>> output_container = auxjad.repeat_container(container, 3)
        >>> abjad.f(output_container)
        {
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
            %%% \time 3/4 %%%
            c'2.
            %%% \time 2/4 %%%
            r2
            g'2
        }

        .. figure:: ../_images/image-repeat_container-4.png

    ..  container:: example

        It automatically closes a container if necessary.

        >>> container = abjad.Container(r"\time 3/4 c'4 d'4 e'4 f'2")
        >>> output_container = auxjad.repeat_container(container, 2)
        >>> abjad.f(output_container)
        {
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            %%% \time 2/4 %%%
            f'2
            %%% \time 3/4 %%%
            c'4
            d'4
            e'4
            %%% \time 2/4 %%%
            f'2
        }

        .. figure:: ../_images/image-repeat_container-5.png

    ..  container:: example

        To omit all time signatures, set the keyword argument
        ``omit_all_time_signatures`` to ``True``.

        >>> container = abjad.Container(r"c'4 d'4 e'4")
        >>> output_container = auxjad.repeat_container(
        ...     container,
        ...     3,
        ...     omit_all_time_signatures=True,
        ... )
        >>> abjad.f(output_container)
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

        .. figure:: ../_images/image-repeat_container-6.png

    ..  container:: example

        To force identical time signatures to be repeated at every repetition,
        set the keyword argument  ``force_identical_time_signatures`` to
        ``True``.

        >>> container = abjad.Container(r"\time 5/4 c'2. d'4 e'4")
        >>> output_container = auxjad.repeat_container(
        ...     container,
        ...     3,
        ...     force_identical_time_signatures=True,
        ... )
        >>> abjad.f(output_container)
        {
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
            %%% \time 5/4 %%%
            c'2.
            d'4
            e'4
        }

        .. figure:: ../_images/image-repeat_container-7.png

    ..  container:: example

        The input container can be of child classes such as ``abjad.Staff``,
        and the output will be of the same type.

        >>> container = abjad.Staff(r"c'4 d'4 e'4")
        >>> output_staff = auxjad.repeat_container(container, 3)
        >>> abjad.f(output_staff)
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

        .. figure:: ../_images/image-repeat_container-8.png

    ..  warning::

        If a container is malformed, i.e. it has an underfilled bar before a
        time signature change, the function raises a ``ValueError`` exception.

        >>> container = abjad.Container(r"\time 5/4 g''1 \time 4/4 f'4")
        >>> output_container = auxjad.repeat_container(container)
        ValueError: 'container' is malformed, with an underfull bar preceeding
        a time signature change
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if not isinstance(n, int):
        raise TypeError("second positional argument must be 'int'")
    if not isinstance(omit_all_time_signatures, bool):
        raise TypeError("'omit_all_time_signatures' must be 'bool'")
    if not isinstance(force_identical_time_signatures, bool):
        raise TypeError("'force_identical_time_signatures' must be 'bool'")

    container_ = copy.deepcopy(container)
    if not container_is_full(container_):
        close_container(container_)
    output_container = type(container_)()
    for _ in range(n):
        output_container.extend(copy.deepcopy(container_))
    if not force_identical_time_signatures:
        remove_repeated_time_signatures(output_container)
    if omit_all_time_signatures:
        for leaf in abjad.select(output_container).leaves():
            if abjad.inspect(leaf).indicator(abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)
    return output_container
