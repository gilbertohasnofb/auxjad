import random
from typing import Union

import abjad

from ..utilities.inspect import inspect
from ..utilities.mutate import mutate


class _LooperParent():
    r"""This is the parent class of all Looper classes. It implements all
    common methods and properties, and initialises those using their @setter
    methods.
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_contents',
                 '_head_position',
                 '_window_size',
                 '_step_size',
                 '_max_steps',
                 '_repetition_chance',
                 '_forward_bias',
                 '_current_window',
                 '_is_first_window',
                 '_process_on_first_call',
                 )

    ### INITIALISER ###

    def __init__(self,
                 head_position,
                 window_size,
                 step_size,
                 max_steps,
                 repetition_chance,
                 forward_bias,
                 process_on_first_call,
                 ):
        r'Initialises self.'
        if not isinstance(process_on_first_call, bool):
            raise TypeError("'process_on_first_call' must be 'bool'")
        self.head_position = head_position
        self.window_size = window_size
        self.step_size = step_size
        self.max_steps = max_steps
        self.repetition_chance = repetition_chance
        self.forward_bias = forward_bias
        self.process_on_first_call = process_on_first_call
        self._is_first_window = True
        self._current_window = None

    ### SPECIAL METHODS ###

    def __call__(self) -> abjad.Selection:
        r"""Calls the looping process for one iteration, returning an
        |abjad.Selection|.
        """
        self._move_head()
        if self._done:
            raise RuntimeError("'contents' has been exhausted")
        self._slice_contents()
        return self.current_window

    def __next__(self) -> abjad.Selection:
        r"""Calls the looping process for one iteration, returning an
        |abjad.Selection|.
        """
        self._move_head()
        if self._done:
            raise StopIteration
        self._slice_contents()
        return self.current_window

    def __iter__(self):
        r'Returns an iterator, allowing instances to be used as iterators.'
        return self

    ### PUBLIC METHODS ###

    def output_all(self,
                   *,
                   tie_identical_pitches: bool = False,
                   ) -> abjad.Selection:
        r"""Goes through the whole looping process and outputs a single
        |abjad.Selection|.
        """
        if not isinstance(tie_identical_pitches, bool):
            raise TypeError("'tie_identical_pitches' must be 'bool'")
        dummy_container = abjad.Container()
        while True:
            try:
                if not tie_identical_pitches or len(dummy_container) == 0:
                    dummy_container.append(self.__call__())
                else:
                    new_window = self.__call__()
                    leaf1 = abjad.select(new_window).leaf(0)
                    leaf2 = abjad.select(dummy_container).leaf(-1)
                    if inspect((leaf1, leaf2)).leaves_are_tieable():
                        abjad.attach(abjad.Tie(), dummy_container[-1])
                    dummy_container.append(new_window)
            except RuntimeError:
                break
        mutate(dummy_container[:]).remove_repeated_time_signatures()
        mutate(dummy_container[:]).reposition_dynamics()
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    def output_n(self,
                 n: int,
                 *,
                 tie_identical_pitches: bool = False,
                 ) -> abjad.Selection:
        r"""Goes through ``n`` iterations of the looping process and outputs a
        single |abjad.Selection|.
        """
        if not isinstance(n, int):
            raise TypeError("first positional argument must be 'int'")
        if n < 1:
            raise ValueError("first positional argument must be a positive "
                             "'int'")
        if not isinstance(tie_identical_pitches, bool):
            raise TypeError("'tie_identical_pitches' must be 'bool'")
        dummy_container = abjad.Container()
        for _ in range(n):
            if not tie_identical_pitches or len(dummy_container) == 0:
                dummy_container.append(self.__call__())
            else:
                new_window = self.__call__()
                leaf1 = abjad.select(new_window).leaf(0)
                leaf2 = abjad.select(dummy_container).leaf(-1)
                if inspect((leaf1, leaf2)).leaves_are_tieable():
                    abjad.attach(abjad.Tie(), dummy_container[-1])
                dummy_container.append(new_window)
        mutate(dummy_container[:]).remove_repeated_time_signatures()
        mutate(dummy_container[:]).reposition_dynamics()
        output = dummy_container[:]
        dummy_container[:] = []
        return output

    ### PRIVATE METHODS ###

    def _move_head(self):
        r"""Moves the head by a certain number of steps of fixed size, either
        forwards or backwards according to the forward bias.
        """
        if not self._is_first_window or self._process_on_first_call:
            if (self._repetition_chance == 0.0
                    or random.random() > self._repetition_chance):
                step = self._step_size * random.randint(1, self._max_steps)
                diretion = self._biased_choice(self._forward_bias)
                self._head_position += step * diretion
        self._is_first_window = False

    def _slice_contents(self):
        r"""Slices :attr:`contents`, will be defined for each individual child
        class.
        """
        pass

    @staticmethod
    def _biased_choice(bias):
        r'Returns either +1 or -1 according to a bias value.'
        return random.choices([1, -1], weights=[bias, 1.0 - bias])[0]

    @staticmethod
    def _remove_all_time_signatures(container):
        r'Removes all time signatures of an |abjad.Container|.'
        for leaf in abjad.select(container).leaves():
            if abjad.inspect(leaf).effective(abjad.TimeSignature):
                abjad.detach(abjad.TimeSignature, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r""":attr:`contents` property will be defined for each individual child
        class.
        """
        pass

    @contents.setter
    def contents(self):
        pass

    @property
    def head_position(self) -> int:
        r'The position of the head at the start of a looping window.'
        return self._head_position

    @head_position.setter
    def head_position(self,
                      head_position: int,
                      ):
        if not isinstance(head_position, int):
            raise TypeError("'head_position' must be 'int'")
        if head_position < 0:
            raise ValueError("'head_position' must be a positive 'int'")
        if head_position >= self.__len__():
            raise ValueError("'head_position' must be smaller than the length "
                             "of 'contents'")
        self._is_first_window = True
        self._head_position = head_position

    @property
    def window_size(self) -> int:
        r'The length of the looping window.'
        return self._window_size

    @window_size.setter
    def window_size(self,
                    window_size: int,
                    ):
        if not isinstance(window_size, int):
            raise TypeError("'window_size' must be 'int'")
        if window_size < 1:
            raise ValueError("'window_size' must be greater than zero")
        if window_size > self.__len__():
            raise ValueError("'window_size' must be smaller than or equal to "
                             "the length of 'contents'")
        self._window_size = window_size

    @property
    def step_size(self) -> int:
        r'The size of each step when moving the head.'
        return self._step_size

    @step_size.setter
    def step_size(self,
                  step_size: int,
                  ):
        if not isinstance(step_size, int):
            raise TypeError("'step_size' must be 'int'")
        if step_size < 1:
            raise ValueError("'step_size' must be greater than zero")
        if step_size >= self.__len__():
            raise ValueError("'step_size' must be smaller than the length of "
                             "'contents'")
        self._step_size = step_size

    @property
    def max_steps(self) -> int:
        r'The maximum number of steps per operation.'
        return self._max_steps

    @max_steps.setter
    def max_steps(self,
                  max_steps: int,
                  ):
        if not isinstance(max_steps, int):
            raise TypeError("'max_steps' must be 'int'")
        if max_steps < 1:
            raise ValueError("'max_steps' must be greater than zero")
        self._max_steps = max_steps

    @property
    def repetition_chance(self) -> float:
        r'The chance of the head not moving, thus repeating the output.'
        return self._repetition_chance

    @repetition_chance.setter
    def repetition_chance(self,
                          repetition_chance: float,
                          ):
        if not isinstance(repetition_chance, float):
            raise TypeError("'repetition_chance' must be 'float'")
        if repetition_chance < 0.0 or repetition_chance > 1.0:
            raise ValueError("'repetition_chance' must be between 0.0 and 1.0")
        self._repetition_chance = repetition_chance

    @property
    def forward_bias(self) -> float:
        r"""The chance of the window moving forward instead of backwards. It
        should range from ``0.0`` to ``1.0`` (default ``1.0``, which means the
        window can only move forwards. A value of ``0.5`` gives :math:`50\%`
        chance of moving forwards while a value of ``0.0`` will move the window
        only backwards).
        """
        return self._forward_bias

    @forward_bias.setter
    def forward_bias(self,
                     forward_bias: float,
                     ):
        if not isinstance(forward_bias, float):
            raise TypeError("'forward_bias' must be 'float'")
        if forward_bias < 0.0 or forward_bias > 1.0:
            raise ValueError("'forward_bias' must be between 0.0 and 1.0")
        self._forward_bias = forward_bias

    @property
    def process_on_first_call(self) -> bool:
        r"""If ``True`` then :attr:`contents` will be processed in the very
        first call.
        """
        return self._process_on_first_call

    @process_on_first_call.setter
    def process_on_first_call(self,
                              process_on_first_call: bool,
                              ):
        if not isinstance(process_on_first_call, bool):
            raise TypeError("'process_on_first_call' must be 'bool'")
        self._process_on_first_call = process_on_first_call

    @property
    def current_window(self) -> Union[abjad.Selection, None]:
        r'Read-only property, returns the window at the current head position.'
        if self._current_window is None:
            return self._current_window
        current_window = abjad.mutate(self._current_window).copy()
        if self._omit_time_signatures:
            self._remove_all_time_signatures(current_window)
        return current_window

    ### PRIVATE PROPERTIES ###

    @property
    def _done(self) -> bool:
        r""":obj:`bool` indicating whether the process is done (i.e. whether
        the head position has overtaken the :attr:`contents`'s length).
        """
        return (self._head_position >= self.__len__()
                or self._head_position < 0)
