from textwrap import dedent
from typing import Union

import abjad


def piano_pedal(
    argument: Union[abjad.Component, abjad.Selection],
    *,
    half_pedal: bool = False,
    until_the_end: bool = False,
    omit_raise_pedal_glyph: bool = False,
    disable_sustain_off: bool = False,
    selector: abjad.Expression = abjad.select().leaves(),
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
    tag: abjad.Tag = None,
) -> None:
    r"""Attaches piano pedal indicators. This function extends the capabilities
    of Abjad's built-in |abjad.piano_pedal()|.

    Basic usage:
        Basic usage is identical to Abjad's built-ind |abjad.piano_pedal()|:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:])
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-KaleXflNvL.png

    ..  note::

        Auxjad automatically replaces Abjad's built-in |abjad.piano_pedal()|
        with this function. Therefore it can be used either as
        :func:`abjad.piano_pedal()` or |abjad.piano_pedal()|, as shown below:

        >>> staff1 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> staff2 = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff1[:])
        >>> auxjad.piano_pedal(staff2[:])
        >>> selections = [staff1[:], staff2[:]]
        >>> auxjad.get.selections_are_identical(selections)
        True

    ``until_the_end``:
        Call the function with ``until_the_end`` set to ``True`` to add an
        arrow to the initial pedal glyph:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   until_the_end=True,
        ...                   )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-rA7ZHeMrjf.png

    ``omit_raise_pedal_glyph``:
        Call the function with ``omit_raise_pedal_glyph`` set to ``True`` to
        remove the raise pedal glyph:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   omit_raise_pedal_glyph=True,
        ...                   )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \sustainOn
                d'4
                e'4
                \once \override Staff.SustainPedal.stencil = ##f
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-p8S1KwHLIx.png

        Combined with ``until_the_end=True``:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   until_the_end=True,
        ...                   omit_raise_pedal_glyph=True,
        ...                   )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                \once \override Staff.SustainPedal.stencil = ##f
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-Fb5rE6QB1f.png

    ``disable_sustain_off``:

        If ``disable_sustain_off`` is set to ``True``, the final ``\sustainOff`` command will be
        omited.

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:], disable_sustain_off=True)
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                c'4
                \sustainOn
                d'4
                e'4
                f'4
            }

        ..  figure:: ../_images/piano_pedal-lXm7901TC9.png

        ..  note::

            If ``disable_sustain_off`` is set to ``True``, then ``omit_raise_pedal_glyph`` will have
            no effect and the raise pedal glyph will be omitted.

    ``half_pedal``:

        Call the function with ``half_pedal`` set to ``True`` to use the half
        pedalling glyph:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   half_pedal=True,
        ...                   )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-EYs495mi9K.png

        Combined with ``until_the_end=True``:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   half_pedal=True,
        ...                   until_the_end=True,
        ...                   )
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \larger "½"
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-viOZdVeRs9.png

    Pedal style:
        The style of the sustain pedal can be tweaked using |abjad.setting()|
        as shown below:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:])
        >>> abjad.setting(staff).pedal_sustain_style = "#'mixed"
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            \with
            {
                pedalSustainStyle = #'mixed
            }
            {
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-6q9Swb2elq.png

        This tweak also works with ``until_the_end=True`` if desired:

        >>> staff = abjad.Staff(r"c'4 d'4 e'4 f'4")
        >>> abjad.piano_pedal(staff[:],
        ...                   until_the_end=True,
        ...                   )
        >>> abjad.setting(staff).pedal_sustain_style = "#'mixed"
        >>> abjad.show(staff)

        ..  docs::

            \new Staff
            \with
            {
                pedalSustainStyle = #'mixed
            }
            {
                \once \override Staff.SustainPedal.stencil =
                    #(lambda (grob) (grob-interpret-markup grob
                        #{
                            \markup {
                                \concat {
                                    \musicglyph "pedal.Ped"
                                    \musicglyph "pedal.."
                                }
                                \raise #-0.3 "→"
                            }
                        #}))
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

        ..  figure:: ../_images/piano_pedal-cYyRwFvnFH.png
    """
    assert callable(selector)
    argument = selector(argument)
    leaves = abjad.Selection(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    if not half_pedal and until_the_end:
        string = r"""
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            """
    elif half_pedal and not until_the_end:
        string = r"""
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                        }
                    #}))
            """
    elif half_pedal and until_the_end:
        string = r"""
            \once \override Staff.SustainPedal.stencil =
                #(lambda (grob) (grob-interpret-markup grob
                    #{
                        \markup {
                            \larger "½"
                            \concat {
                                \musicglyph "pedal.Ped"
                                \musicglyph "pedal.."
                            }
                            \raise #-0.3 "→"
                        }
                    #}))
            """
    if half_pedal or until_the_end:
        string = dedent(string).strip()
        pedal_tweak = abjad.LilyPondLiteral(string)
        abjad.attach(pedal_tweak, start_leaf)

    start_piano_pedal = start_piano_pedal or abjad.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or abjad.StopPianoPedal()

    abjad.attach(start_piano_pedal, start_leaf, tag=tag)
    if not disable_sustain_off:
        abjad.attach(stop_piano_pedal, stop_leaf, tag=tag)
        if omit_raise_pedal_glyph:
            omit_raise_pedal_glyph_tweak = abjad.LilyPondLiteral(
                r"\once \override Staff.SustainPedal.stencil = ##f"
            )
            abjad.attach(omit_raise_pedal_glyph_tweak, stop_leaf)


# ---------- MONKEY PATCHING ----------

abjad.spanners.piano_pedal = piano_pedal
abjad.piano_pedal = piano_pedal
