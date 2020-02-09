import abjad
import random
import copy
from simplified_time_signature_ratio import simplified_time_signature_ratio


class LoopWindowByElements():
    r"""Takes a container as input as well as an integer representing the
    number of elements per looping window, then outputs a container with
    the elements processed in the looping process. For instance, if the initial
    container had the leaves [A, B, C, D, E] and the looping window was size 3,
    the output would be: A B C B C D C D E D E E, which can be better
    visualised in:

    A B C
      B C D
        C D E
          D E
            E

    ..  container:: example

        Usage is similar to other factory classes. It takes a container (or
        child class equivalent) and the size of the window. Each call of the
        object, in thi case looper(), will output the result and move the
        window forwards. Notice that the time signatures in the example below
        are commented out with %%% because abjad only adds them to the score
        once the leaves are part of a staff:

        >>> input_music = abjad.Container(r"c'4 d'2 e'4 f'4 g'1")
        >>> looper = LoopWindowByElements(input_music, 3)
        >>> container = looper()
        >>> abjad.f(container)
        {
            %%% \time 4/4 %%%
            c'4
            d'2
            e'4
        }
        >>> container = looper()
        >>> abjad.f(container)
        {
            %%% \time 4/4 %%%
            d'2
            e'4
            f'4
        }
    """

    def __init__(self,
                 container: abjad.Container,
                 elements_per_window: int,
                 *,
                 step_size: int = 1,
                 repetition_chance: float = 0.0,
                 max_steps: int = 1,
                 initial_head_position: int = 0,
                 ):
        if not isinstance(container, abjad.Container):
            raise TypeError("'container' must be 'abjad.Container' or "
                            "child class")
        if not isinstance(elements_per_window, int):
            raise TypeError("'elements_per_window' must be a int")
        if not isinstance(step_size, int):
            raise TypeError("'step_size' must be a int")
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be float")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if not isinstance(initial_head_position,
                  (int, float, tuple, str, abjad.Duration),
                  ):
              raise TypeError("'initial_head_position' must be a duration")

        self._container = abjad.select(container).logical_ties()
        self.current_head_position = initial_head_position
        self.elements_per_window = elements_per_window
        self.step_size = step_size
        self.repetition_chance = repetition_chance
        self.max_steps = max_steps
        self.counter = 0
        self._current_window = self._slice_container()


    def __call__(self) -> abjad.Selection:
        self._move_head()
        self._slice_container()
        return self._current_window

    def reset_counter(self):
        self.counter = 0

    def get_current_window(self):
        return self._current_window

    def __len__(self):
        return len(self._container)

    def done(self):
        return self.current_head_position > (len(self._container) - 2)

    def _slice_container(self) -> abjad.Selection:
        start = self.current_head_position
        end = self.current_head_position + self.elements_per_window
        logical_ties = self._container[start:end]
        self._current_window = abjad.Container()
        time_signature_duration = 0
        for logical_tie in logical_ties:
            effective_duration = abjad.inspect(logical_tie).duration()
            logical_tie_ = copy.deepcopy(logical_tie)
            self._current_window.append(logical_tie_)
            multiplier = effective_duration / logical_tie_.written_duration
            logical_tie_ = abjad.mutate(logical_tie_).scale(multiplier)
            time_signature_duration += effective_duration
        if len(logical_ties) > 0:
            time_signature = abjad.TimeSignature(time_signature_duration)
            time_signature = simplified_time_signature_ratio(time_signature)
            abjad.attach(time_signature,
                         abjad.select(self._current_window).leaves()[0])

    def _move_head(self):
        if self.counter > 0:  # first time always leave head at 0
            if self.repetition_chance == 0.0 \
                    or random.random() > self.repetition_chance:
                self.current_head_position += \
                    self.step_size * random.randint(1, self.max_steps)
        self.counter += 1

    def output_all(self):
        result = abjad.Container()
        while not self.done():
            result.append(self.__call__())
        return result


# input_music = abjad.Container(r"c'4 d'8 e'2 f'16 g'1 a'4 b'32 \times 4/5 {a4 g2 a2} c'2.. d'4. e'8. f'1")
# looper = LoopWindowByElements(input_music, 5)
# while not looper.done():
#     staff.append(looper())
# input_music = abjad.Container(r"c'4 d'2 e'4 f'4 g'1")
# looper = LoopWindowByElements(input_music, 3)
# container = looper.output_all()
# staff = abjad.Staff([container])
# abjad.f(staff)
