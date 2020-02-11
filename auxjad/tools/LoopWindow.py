import abjad
import random


class LoopWindow():
    r"""xxx

    ..  container:: example

        xxx

        >>> xxx
    """

    def __init__(container: abjad.Container,
                 *,
                 window_size=(4, 1),
                 step_size=(1, 16),
                 allow_repetition: bool = False,
                 max_steps: int = 1,
                 initial_head_position: int = 0,
                 ):
        if not isinstance(container, abjad.Container):
            raise TypeError("'container' must be 'abjad.Container' or "
                            "child class")
        if not isinstance(window_size,
                          (int, float, tuple, str, abjad.Duration),
                          ):
            raise TypeError("'window_size' must be a duration")
        if not isinstance(step_size,
                  (int, float, tuple, str, abjad.Duration),
                  ):
            raise TypeError("'step_size' must be a duration")
        if not isinstance(allow_repetition, bool):
            raise TypeError("'allow_repetition' must be 'bool' or 'float'")
        if isinstance(allow_repetition, float):
            if allow_repetition < 0.0 or allow_repetition > 1.0:
                raise ValueError("'allow_repetition' must be between "
                                 "0.0 and 1.0")
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if not isinstance(initial_head_position,
                  (int, float, tuple, str, abjad.Duration),
                  ):
              raise TypeError("'initial_head_position' must be a duration")

        self._container = container
        self.current_head_position = initial_head_position
        self.window_size = window_size
        self.step_size = step_size
        self.allow_repetition = allow_repetition
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

    def _slice_container(self) -> abjad.Selection:
        # slice self._container
        # from self.current_head_position
        # to self.current_head_position + self.window_size
        return #sliced container

    def _move_head(self):
        if self.counter > 0:  # first window always the initial
            if self.allow_repetition:
                aux = random.random()
                if aux > self.allow_repetition: # if <= then repeats
                    self.current_head_position += \
                        self.step_size * random.randint(1, self.max_steps)
        self.counter += 1

    @staticmethod
    def _xxx(foo):
        return foo

# TODO: implement this, right now this is just a slightly altered copy of
# LoopWindowByElements. This has NOT been properly implemented yet
