import abjad
import copy
from ._LoopWindowGeneric import _LoopWindowGeneric
from .simplified_time_signature_ratio import simplified_time_signature_ratio


class LoopWindowByElements(_LoopWindowGeneric):
    r"""Takes an abjad.Container as input as well as an integer representing
    the number of elements per looping window, then outputs a container with
    the elements processed in the looping process. For instance, if the initial
    container had the leaves [A, B, C, D, E, F] and the looping window was size
    three, the output would be: A B C B C D C D E D E F E F F, which can be
    better visualised as:

    .. code-block:: none

        A B C
          B C D
            C D E
              D E F
                E F
                  F

    ..  container:: example

        Usage is similar to other factory classes. It takes a container (or
        child class equivalent) and the number of elements of the window as
        arguments. Each call of the object, in this case looper(), will move
        the window forwards and output the result.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=3,
        ...                                      )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

        The method get_current_window() will output the current window without
        moving the head forwards.

        >>> notes = looper.get_current_window()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 11/8
            d'2
            e'4
            f'2
            ~
            f'8
        }

    ..  container:: example

        The instances of LoopWindowByElements can also be used as an iterator,
        which can then be used in a for loop to exhaust all windows.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=2,
        ...                                      )
        >>> for window in looper:
        ...     staff = abjad.Staff(window)
        ...     abjad.f(staff)
        \new Staff
        {
            \time 3/4
            c'4
            d'2
        }
        \new Staff
        {
            \time 3/4
            d'2
            e'4
        }
        \new Staff
        {
            \time 1/4
            e'4
        }

    ..  container:: example

        This class can take many optional keyword arguments during its
        creation. step_size dictates the size of each individual step in
        number of elements (default value is 1). max_steps sets the maximum
        number of steps that the window can advance when the object is called,
        ranging between 1 and the input value (default is also 1).
        repetition_chance sets the chance of a window result repeating itself
        (that is, the window not moving forwards when called). It should range
        from 0.0 to 1.0 (default 0.0, i.e. no repetition). Finally,
        head_position can be used to offset the starting position of the
        looping window. It must be an integer and its default value is 0.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=3,
        ...                                      step_size=1,
        ...                                      max_steps=2,
        ...                                      repetition_chance=0.25,
        ...                                      head_position=0,
        ...                                      )
        >>> looper.window_size
        3
        >>> looper.step_size
        1
        >>> looper.repetition_chance
        0.25
        >>> looper.max_steps
        2
        >>> looper.head_position
        0

        Use the set methods below to change these values after initialisation.

        >>> looper.set_window_size(2)
        >>> looper.set_step_size(2)
        >>> looper.set_max_steps(3)
        >>> looper.set_repetition_chance(0.1)
        >>> looper.set_head_position(2)
        >>> looper.window_size
        2
        >>> looper.step_size
        2
        >>> looper.max_steps
        3
        >>> looper.repetition_chance
        1
        >>> looper.head_position
        2

    ..  container:: example

        To disable time signatures altogether, initialise LoopWindowByElements
        with the keyword omit_time_signature set to True (default is False), or
        use the set_omit_time_signature() method after initialisation.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=3,
        ...                                      omit_time_signature=True,
        ...                                      )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            c'4
            d'2
            e'4
        }

    ..  container:: example

        The function len() can be used to get the total number of elements in
        the container.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=3,
        ...                                      )
        >>> len(looper)
        5

    ..  container:: example

        To run through the whole process and output it as a single container,
        from  the initial head position until the process outputs the single
        last element, use the method output_all().

        >>> input_music = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=2,
        ...                                      )
        >>> window = looper.output_all()
        >>> staff = abjad.Staff(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 2/4
            c'4
            d'4
            \time 2/4
            d'4
            e'4
            \time 2/4
            e'4
            f'4
            \time 1/4
            f'4
        }

    .. container:: example

        To change the size of the window after instantiation, use the method
        set_window_size(). In the example below, the initial window is of size
        3, and so the first call of the looper object outputs the first,
        second, and third leaves. The window size is then set to 4, and the
        looper is called again, moving to the leaf in the next position, thus
        outputting the second, third, fourth, and fifth leaves.

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'2 ~ f'8 g'1")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=3,
        ...                                      )
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 4/4
            c'4
            d'2
            e'4
        }
        >>> looper.set_window_size(4)
        >>> notes = looper()
        >>> staff = abjad.Staff(notes)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 19/8
            d'2
            e'4
            f'2
            ~
            f'8
            g'1
        }

    ..  container:: example

        This class can handle tuplets, but the output is not ideal and so this
        functionality should be considered experimental. Time signatures will
        be correct when dealing with partial tuplets (thus having non-standard
        values in their denominators), but each individual note of a tuplet
        will have the ratio printed above it.

        >>> input_music = abjad.Container(r"c'4 d'8 \times 2/3 {a4 g2}")
        >>> looper = auxjad.LoopWindowByElements(input_music,
        ...                                      window_size=2,
        ...                                      )
        >>> window = looper.output_all()
        >>> staff = abjad.Staff(window)
        >>> abjad.f(staff)
        \new Staff
        {
            \time 3/8
            c'4
            d'8
            #(ly:expect-warning "strange time signature found")
            \time 7/24
            d'8
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                a4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                \time 2/4
                a4
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                g2
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                #(ly:expect-warning "strange time signature found")
                \time 2/6
                g2
            }
        }
    """

    def __init__(self,
                 container: abjad.Container,
                 *,
                 window_size: int,
                 step_size: int = 1,
                 max_steps: int = 1,
                 repetition_chance: float = 0.0,
                 head_position: int = 0,
                 omit_time_signature: bool = False,
                 ):
        if not isinstance(container, abjad.Container):
            raise TypeError("'container' must be 'abjad.Container' or child "
                            "class")
        self._container = abjad.select(container).logical_ties()
        super().__init__(head_position,
                         window_size,
                         step_size,
                         max_steps,
                         repetition_chance,
                         )
        self.set_omit_time_signature(omit_time_signature)


    def __len__(self) -> int:
        return len(self._container)

    def set_omit_time_signature(self,
                                omit_time_signature: bool,
                                ):
        if not isinstance(omit_time_signature, bool):
            raise TypeError("'omit_time_signature' must be 'bool'")
        self.omit_time_signature = omit_time_signature

    def _slice_container(self) -> abjad.Selection:
        start = self.head_position
        end = self.head_position + self.window_size
        logical_ties = self._container[start:end]
        dummy_container = abjad.Container()
        time_signature_duration = 0
        for logical_tie in logical_ties:
            effective_duration = abjad.inspect(logical_tie).duration()
            logical_tie_ = copy.deepcopy(logical_tie)
            dummy_container.append(logical_tie_)
            multiplier = effective_duration / logical_tie_.written_duration
            logical_tie_ = abjad.mutate(logical_tie_).scale(multiplier)
            time_signature_duration += effective_duration
        if len(logical_ties) > 0 and not self.omit_time_signature:
            time_signature = abjad.TimeSignature(time_signature_duration)
            time_signature = simplified_time_signature_ratio(time_signature)
            abjad.attach(time_signature,
                         abjad.select(dummy_container).leaves()[0],
                         )
        self._current_window = dummy_container[:]
        dummy_container[:] = []
