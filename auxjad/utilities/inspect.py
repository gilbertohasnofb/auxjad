import collections
from typing import Iterable, Union

import abjad

from .inspections.extract_time_signatures import extract_time_signatures
from .inspections.leaves_are_tieable import leaves_are_tieable
from .inspections.selection_is_full import selection_is_full
from .inspections.selections_are_identical import selections_are_identical
from .inspections.underfull_duration import underfull_duration


class Inspection:
    r"""Inspection class containing all of Auxjad's inspection methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.inspect(staff[2:])
        Inspection(client=Selection([Note("d'4"), Note("f'4")]))

    .. note::

        Auxjad automatically adds all methods of :class:`Inspection` as
        extension methods to |abjad.inspect()|. Therefore they can be used from
        either :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> auxjad.inspect(container[:]).selection_is_full()
        True
        >>> abjad.inspect(container[:]).selection_is_full()
        True
    """

    ### CLASS VARIABLES ###

    __slots__ = ('_client',)

    ### INITIALISER ###

    def __init__(self,
                 client: Union[abjad.Component,
                               Iterable[abjad.Component],
                               ] = None,
                 ):
        r'Initialises self.'
        assert not isinstance(client, str), repr(client)
        if not isinstance(client, (abjad.Component,
                                   collections.abc.Iterable,
                                   type(None),
                                   )):
            raise TypeError('must be component, non-string iterable or None: '
                            f'(not {client!r}).')
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Gets interpreter representation.'
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC METHODS ###

    def extract_time_signatures(self,
                                *,
                                do_not_use_none: bool = False,
                                implicit_common_time: bool = True,
                                omit_repeated: bool = False,
                                ) -> list:
        return extract_time_signatures(
            self._client,
            do_not_use_none=do_not_use_none,
            implicit_common_time=implicit_common_time,
            omit_repeated=omit_repeated,
        )

    def leaves_are_tieable(self) -> bool:
        return leaves_are_tieable(self._client)

    def selection_is_full(self) -> bool:
        return selection_is_full(self._client)

    def selections_are_identical(self,
                                 *,
                                 include_indicators: bool = True,
                                 ) -> bool:
        return selections_are_identical(self._client,
                                        include_indicators=include_indicators,
                                        )

    def underfull_duration(self) -> abjad.Duration:
        return underfull_duration(self._client)

    ### PUBLIC PROPERTIES ###

    @property
    def client(self) -> Union[abjad.Component,
                              Iterable[abjad.Component],
                              None,
                              ]:
        r'Gets client. Returns component.'
        return self._client


### METHOD DOCSTRINGS ###

Inspection.extract_time_signatures.__doc__ = extract_time_signatures.__doc__
Inspection.leaves_are_tieable.__doc__ = leaves_are_tieable.__doc__
Inspection.selection_is_full.__doc__ = selection_is_full.__doc__
Inspection.selections_are_identical.__doc__ = selections_are_identical.__doc__
Inspection.underfull_duration.__doc__ = underfull_duration.__doc__


### FUNCTIONS ###

def inspect(client):
    r"""Makes an inspection agent. See :class:`Inspection` for the
    documentation of all of its methods.

    Example:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> auxjad.inspect(staff[2:])
        Inspection(client=Selection([Note("d'4"), Note("f'4")]))

    .. note::

        Auxjad automatically adds all methods of :class:`Inspection` as
        extension methods to |abjad.inspect()|. Therefore they can be used from
        either :func:`auxjad.inspect()` or |abjad.inspect()|, as shown below:

        >>> container = abjad.Container(r"c'4 d'4 e'4 f'4")
        >>> auxjad.inspect(container[:]).selection_is_full()
        True
        >>> abjad.inspect(container[:]).selection_is_full()
        True
    """
    return Inspection(client)


### EXTENSION METHODS ###

abjad.Inspection.extract_time_signatures = Inspection.extract_time_signatures
abjad.Inspection.leaves_are_tieable = Inspection.leaves_are_tieable
abjad.Inspection.selection_is_full = Inspection.selection_is_full
abjad.Inspection.selections_are_identical = Inspection.selections_are_identical
abjad.Inspection.underfull_duration = Inspection.underfull_duration
