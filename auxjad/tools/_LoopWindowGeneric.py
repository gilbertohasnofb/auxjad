import copy
import random
import abjad
from .are_leaves_tieable import are_leaves_tieable


class _LoopWindowGeneric():
    r"""This is the parent class of all LoopWindowXxx classes. It implements
    all common methods and attributes, and initialises those using its set_
    methods.
    """

    def __init__(self,
                 head_position,
                 window_size,
                 step_size,
                 max_steps,
                 repetition_chance,
                 forward_bias,
                 ):
        self._first_window = True
        self.set_head_position(head_position)
        self.set_window_size(window_size)
        self.set_step_size(step_size)
        self.set_max_steps(max_steps)
        self.set_repetition_chance(repetition_chance)
        self.set_forward_bias(forward_bias)

    def __call__(self) -> abjad.Selection:
        self._move_head()
        if self._done():
            raise RuntimeError("'container' has been exhausted")
        self._slice_container()
        return copy.deepcopy(self._current_window)

    def __iter__(self):
        return self

    def __next__(self) -> abjad.Selection:
        self._move_head()
        if self._done():
            raise StopIteration
        self._slice_container()
        return copy.deepcopy(self._current_window)

    def set_window_size(self,
                        window_size: int,
                        ):
        if not isinstance(window_size, int):
            raise TypeError("'window_size' must be 'int'")
        if window_size < 1:
            raise ValueError("'window_size' must be greater than zero")
        if window_size > self._container.__len__():
            raise ValueError("'window_size' must be smaller than or equal to "
                             "the length of 'container'")
        self.window_size = window_size

    def set_step_size(self,
                      step_size: int,
                      ):
        if not isinstance(step_size, int):
            raise TypeError("'step_size' must be 'int'")
        if step_size < 1:
            raise ValueError("'step_size' must be greater than zero")
        if step_size >= self._container.__len__():
            raise ValueError("'step_size' must be smaller than the length of "
                             "'container'")
        self.step_size = step_size

    def set_max_steps(self,
                      max_steps: int,
                      ):
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if max_steps < 1:
            raise ValueError("'max_steps' must be greater than zero")
        self.max_steps = max_steps

    def set_repetition_chance(self,
                              repetition_chance: float,
                              ):
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        self.repetition_chance = repetition_chance

    def set_forward_bias(self,
                         forward_bias: float,
                         ):
        if not isinstance(forward_bias, float):
            raise TypeError("'forward_bias' must be 'float'")
        if forward_bias < 0.0 or forward_bias > 1.0:
            raise ValueError("'forward_bias' must be between 0.0 and 1.0")
        self.forward_bias = forward_bias

    def set_head_position(self,
                          head_position: int,
                          ):
        if not isinstance(head_position, int):
            raise TypeError("'head_position' must be 'int'")
        if head_position < 0:
            raise ValueError("'head_position' must be a positive 'int'")
        if head_position >= self._container.__len__():
            raise ValueError("'head_position' must be smaller than the length "
                             "of 'container'")
        self.head_position = head_position

    def get_current_window(self) -> (list, abjad.Selection):
        return copy.deepcopy(self._current_window)

    def output_all(self,
                   *,
                   tie_identical_pitches: bool = False,
                   ) -> abjad.Selection:
        dummy_container = abjad.Container()
        while True:
            try:
                if not tie_identical_pitches or len(dummy_container) == 0:
                    dummy_container.append(self.__call__())
                else:
                    new_window = self.__call__()
                    leaf1 = abjad.select(new_window).leaves()[0]
                    leaf2 = abjad.select(dummy_container).leaves()[-1]
                    if are_leaves_tieable(leaf1, leaf2):
                        abjad.attach(abjad.Tie(), dummy_container[-1])
                    dummy_container.append(new_window)
            except:
                break
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def output_n(self,
                 n: int,
                 *,
                 tie_identical_pitches: bool = False,
                 ) -> abjad.Selection:
        dummy_container = abjad.Container()
        for _ in range(n):
            if not tie_identical_pitches or len(dummy_container) == 0:
                dummy_container.append(self.__call__())
            else:
                new_window = self.__call__()
                leaf1 = abjad.select(new_window).leaves()[0]
                leaf2 = abjad.select(dummy_container).leaves()[-1]
                if are_leaves_tieable(leaf1, leaf2):
                    abjad.attach(abjad.Tie(), dummy_container[-1])
                dummy_container.append(new_window)
        result = dummy_container[:]
        dummy_container[:] = []
        return result

    def _move_head(self):
        if not self._first_window:  # first window always at initial position
            if self.repetition_chance == 0.0 \
                    or random.random() > self.repetition_chance:
                step = self.step_size * random.randint(1, self.max_steps)
                diretion = self._biased_choice(self.forward_bias)
                self.head_position += step * diretion
        else:
            self._first_window = False

    def _done(self) -> bool:
        return self.head_position >= self._container.__len__() or \
            self.head_position < 0

    def _slice_container(self):
        pass

    @staticmethod
    def _biased_choice(bias):
        return random.choices([1, -1], weights=[bias, 1.0-bias])[0]
