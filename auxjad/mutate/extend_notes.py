from math import gcd, lcm

import abjad

from .. import get, mutate


def _calculate_gcd_durations(duration_a, duration_b):
    r"""Calculates the greatest common denominator of two durations. Used to
    select the greatest duration possible for splitting the notes on a grid
    """
    n = gcd(duration_a.pair[0], duration_b.pair[0])
    m = lcm(duration_a.pair[1], duration_b.pair[1])
    return abjad.Duration((n, m))


def extend_notes(container: abjad.Container,
                 max_note_duration: abjad.Duration,
                 *,
                 rewrite_meter: bool = True,
                 ) -> None:
    r"""Mutates an input |abjad.Container| (or child class) in place and has no
    return value; this function extends all notes and chords up to a given
    maximum note duration.

    Basic usage:
        This function will extend each note's duration up until a allowed
        maximum duration.

        >>> staff = abjad.Staff(r"c'16 r2... d'8 r2.. e'8. r16 r2. f'4 r2.")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r2...
                d'8
                r2..
                e'8.
                r16
                r2.
                f'4
                r2.
            }

        ..  figure:: ../_images/extend_notes-gJGtjtm3fu.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r2.
                d'4
                r2.
                e'4
                r2.
                f'4
                r2.
            }

        ..  figure:: ../_images/extend_notes-6pjHLREOap.png

    ..  note::

        Auxjad automatically adds this function as an extension function to
        |abjad.mutate|. It can thus be used from either |auxjad.mutate|_ or
        |abjad.mutate| namespaces. Therefore, the two lines below are
        equivalent:

        >>> auxjad.mutate.extend_notes(staff)
        >>> abjad.mutate.extend_notes(staff)

    Chords:
        This function works with chords:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'8 r8 r2 r4 <d' e' f'>4 r4 r8 g'16 r16 r2"
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'8
                r8
                r2
                r4
                <d' e' f'>4
                r4
                r8
                g'16
                r16
                r2
            }

        ..  figure:: ../_images/extend_notes-2151PE127t.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((2, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2
                r4
                r4
                <d' e' f'>2
                r8
                g'8
                ~
                g'4.
                r8
            }

        ..  figure:: ../_images/extend_notes-GVM7SBRQ5z.png

    Second positional argument:
        The second positional argument must be an |abjad.Duration| or objects
        that can instantiate an |abjad.Duration|, such as :obj:`str`,
        :obj:`tuple`, :obj:`int`, and :obj:`float`. The notes will be extended
        up to that duration, or until the next note if the full duration is not
        possible:

        >>> staff = abjad.Staff(
        ...     r"c'16 r4.. d'16 r4.. e'16 r2... f'16 r4.. g'16 r4.."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r4..
                d'16
                r4..
                e'16
                r2...
                f'16
                r4..
                g'16
                r4..
            }

        ..  figure:: ../_images/extend_notes-GfrvgpqH2J.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2
                d'2
                e'2.
                r4
                f'2
                g'2
            }

        ..  figure:: ../_images/extend_notes-1vKtKyK7up.png

    Dynamics:
        Dynamics are preserved:

        >>> staff = abjad.Staff(
        ...     r"c'16\ppp r2... d'16\ff r2... e'16\f r2... f'16\mp r2..."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                \ppp
                r2...
                d'16
                \ff
                r2...
                e'16
                \f
                r2...
                f'16
                \mp
                r2...
            }

        ..  figure:: ../_images/extend_notes-rAHtip59b2.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'2.
                \ppp
                r4
                d'2.
                \ff
                r4
                e'2.
                \f
                r4
                f'2.
                \mp
                r4
            }

        ..  figure:: ../_images/extend_notes-TNbei46PhS.png

    Time signatures changes:
        This function handles time signature changes:

        >>> staff = abjad.Staff(
        ...     r"\time 3/4 c'16 r8. r2 "
        ...     r"\time 2/4 d'8 r8 e'8 r8 "
        ...     r"\time 3/4 r2 f'16 r8."
        ... )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'16
                r8.
                r2
                \time 2/4
                d'8
                r8
                e'8
                r8
                \time 3/4
                r2
                f'16
                r8.
            }

        ..  figure:: ../_images/extend_notes-k8d4mKMaS7.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((3, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \time 3/4
                c'2.
                \time 2/4
                d'4
                e'4
                ~
                \time 3/4
                e'2
                f'4
            }

        ..  figure:: ../_images/extend_notes-5eDO8ehSld.png

    ``rewrite_meter``
        By default, this function applies |auxjad.mutate.auto_rewrite_meter()|
        at the end of its process.

        >>> staff = abjad.Staff(r"c'16 r4.. d'16 r4..")
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                r4..
                d'16
                r4..
            }

        ..  figure:: ../_images/extend_notes-BcAYS4SvUL.png

        >>> auxjad.mutate.extend_notes(staff, abjad.Duration((1, 4)))
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                r4
                d'4
                r4
            }

        ..  figure:: ../_images/extend_notes-QNEks8lUXB.png

        Set ``rewrite_meter`` to ``False`` to disable this. Note that this
        function works by slicing a container into very thin slices, which are
        then tied together according to the maximum duration. The main reason
        for setting ``rewrite_meter`` to ``False`` is thus performance: when
        multiple mutations are being applied, it's faster to rewrite the meter
        just once.

        >>> staff = abjad.Staff(r"c'16 r4.. d'16 r4..")
        >>> auxjad.mutate.extend_notes(staff,
        ...                            abjad.Duration((1, 4)),
        ...                            rewrite_meter=False,
        ...                            )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'16
                ~
                c'16
                ~
                c'16
                ~
                c'16
                r16
                r16
                r16
                r16
                d'16
                ~
                d'16
                ~
                d'16
                ~
                d'16
                r16
                r16
                r16
                r16
            }

        ..  figure:: ../_images/extend_notes-49jhNoSa9T.png
    """
    if not isinstance(container, abjad.Container):
        raise TypeError("first positional argument must be 'abjad.Container' "
                        "or child class")
    if len(abjad.select(container).tuplets()) > 0:
        raise ValueError("first positional argument contains one ore more "
                         "tuplets, which are not currently supported")
    if not isinstance(max_note_duration,
                      (abjad.Duration, str, tuple, int, float),
                      ):
        raise TypeError("second positional argument must be 'abjad.Duration', "
                        "'str', 'tuple', or a number")
    if not isinstance(rewrite_meter, bool):
        raise TypeError("'rewrite_meter' must be 'bool'")
    if not isinstance(max_note_duration, abjad.Duration):
        max_note_duration = abjad.Duration(max_note_duration)

    grid_unit = max_note_duration
    for leaf in abjad.select(container).leaves():
        grid_unit = _calculate_gcd_durations(abjad.get.duration(leaf),
                                             grid_unit,
                                             )
    abjad.mutate.split(container[:],
                       [grid_unit],
                       cyclic=True,
                       )
    leaves = abjad.select(container).leaves()
    for index, leaf in enumerate(leaves):
        if isinstance(leaf, (abjad.Note, abjad.Chord)):
            total_duration = abjad.get.duration(leaf)
            i = index - 1  # index for backwards looping
            while get.leaves_are_tieable((leaf, leaves[i])):
                total_duration += abjad.get.duration(leaves[i])
                i -= 1
            next_index = index + 1
            while total_duration < max_note_duration:
                if (next_index < len(leaves)
                        and (isinstance(leaves[next_index], abjad.Rest))):
                    if isinstance(leaf, abjad.Note):
                        leaf_copy = abjad.Note(leaf.written_pitch,
                                               leaf.written_duration,
                                               )
                    elif isinstance(leaf, abjad.Chord):
                        leaf_copy = abjad.Chord(leaf.written_pitches,
                                                leaf.written_duration,
                                                )
                    time_sig = abjad.get.indicator(leaves[next_index],
                                                   abjad.TimeSignature,
                                                   )
                    if time_sig is not None:
                        abjad.attach(time_sig, leaf_copy)
                    abjad.mutate.replace(leaves[next_index], leaf_copy)
                    total_duration += abjad.get.duration(leaf_copy)
                    next_index += 1
                else:
                    break
    leaves = abjad.select(container).leaves()
    pairs_of_leaves = [abjad.select(_).with_next_leaf() for _ in leaves]
    for pair_of_leaves in pairs_of_leaves[:-1]:
        if get.leaves_are_tieable(pair_of_leaves[:]):
            if abjad.get.indicator(pair_of_leaves[0], abjad.Tie) is None:
                abjad.attach(abjad.Tie(), pair_of_leaves[0])
    if rewrite_meter:
        mutate.auto_rewrite_meter(container)
