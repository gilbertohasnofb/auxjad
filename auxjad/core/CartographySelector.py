import random


class CartographySelector():
    r"""A selector used to store, manipulate, and select objects using a
    weighted function constructed with a fixed decay rate. The decay rate
    represents the ratio of probabilities of any index given the probability of
    the preceeding one. For instance, if the decay rate is set to ``0.75``
    (which is its default value), the probability of the element in index 1 of
    the input list being selected is 0.75 the probability of the element in
    index 0, and the probability of the element in index 2 is 0.5625 (0.75^2)
    the probability of the element in index 0. This is the selector used in my
    *Cartography* series of compositions.

    ..  container:: example

        The selector should be initialised with a list of objects. The contents
        of the list can be absolutely anything.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]

        The default decay rate is 0.75; that is, the weight of any given
        elements is the weight of the previous one multiplied by 0.75. The
        weights are associated with the index position, not the elements
        themselves.

        >>> selector.weights
        [1.0, 0.75, 0.5625, 0.421875, 0.31640625]

        Applying the ``len()`` function to the selector will give the length
        of the input list.

        >>> len(selector)
        5

        Calling the selector will output one of its elements, selected
        according to its weight function.

        >>> selector()
        2

        Alternatively, use the ``next()`` function or ``__next__()`` method to
        get the next result.

        >>> selector.__next__()
        1
        >>> next(selector)
        0

    ..  container:: example

        By default, only the weight function (defined by the decay rate) is
        taken into consideration when selecting an element. This means that
        repeated elements can appear, as shown below.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(selector())
        >>> result
        203001402200011111101400310140

        Calling the selector with the optional keyword argument ``no_repeat``
        set to ``True`` will forbid immediate repetitions among consecutive
        calls.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(selector(no_repeat=True))
        >>> result
        210421021020304024230120241202

    ..  container:: example

        The keyword argument ``decay_rate`` can be used to set a different
        decay rate when creating a selector.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4],
        ...                                       decay_rate=0.5,
        ...                                       )
        >>> selector.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]

        The decay rate can also be set after the creation of a selector using,
        the property ``decay_rate``.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.decay_rate = 0.2
        >>> selector.weights
        [1.0, 0.2, 0.04000000000000001, 0.008000000000000002,
        0.0016000000000000003]
        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(selector())
        >>> result
        '000001002100000201001030000100'

    ..  container:: example

        Appending is a type of content transformation. It discards the first
        element of the selector's ``contents``, shifts all others leftwards,
        and then appends the new element to the last index.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.append(5)
        >>> selector.contents
        [1, 2, 3, 4, 5]
        >>> selector.append(42)
        >>> selector.contents
        [2, 3, 4, 5, 42]

    ..  container:: example

        The method ``append_keeping_n()`` is similar to ``append()``, but it
        keeps the first ``n`` elements of ``contents`` untouched. It thus
        discards the n+1-th element, shifts all the next elements one position
        lefwards, and finally appends the new element at the last index.

        >>> selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
        >>> selector.contents
        [10, 7, 14, 31, 98]
        >>> selector.append_keeping_n(100, 2)
        >>> selector.contents
        [10, 7, 31, 98, 100]

    ..  container:: example

        Prepending is another type of content transformation. It discards the
        last element of the ``contents``, shifts all others rightwards, and
        then prepends the new element to the first index.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.prepend(-1)
        >>> selector.contents
        [-1, 0, 1, 2, 3]
        >>> selector.prepend(71)
        >>> selector.contents
        [71, -1, 0, 1, 2]

    ..  container:: example

        Rotation is another type of content transformation. It rotates all
        elements rightwards, moving the last element to the first index. If the
        optional keyword argument ``anticlockwise`` is set to ``True``, the
        rotation will be in the opposite direction.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.rotate()
        >>> selector.contents
        [1, 2, 3, 4, 0]
        >>> selector.rotate(anticlockwise=True)
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.rotate(anticlockwise=True)
        >>> selector.contents
        [1, 2, 3, 4, 0]

    ..  container:: example

        The mirror transformation swaps the element of the input index with its
        complementary element. Complementary elements are defined as the pair
        of elements which share the same distance from the centre of the
        ``contents`` (in terms of number of indeces), and are located at either
        side.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.mirror(0)
        >>> selector.contents
        [4, 1, 2, 3, 0]
        >>> selector.mirror(0)
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.mirror(3)
        >>> selector.contents
        [0, 3, 2, 1, 4]
        >>> selector.mirror(2)
        >>> selector.contents
        [0, 3, 2, 1, 4]

    ..  container:: example

        To mirror a random pair of complementary elements, use the
        ``mirror_random()`` method. In case of a selector with an odd number
        of elements, this method will never pick an element at the pivot point
        since the operation would not change the contents.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.mirror_random()
        >>> selector.contents
        [4, 1, 2, 3, 0]
        >>> selector.mirror_random()
        >>> selector.contents
        [4, 3, 2, 1, 0]
        >>> selector.mirror_random()
        >>> selector.contents
        [4, 1, 2, 3, 0]

    ..  container:: example

        The method ``randomise()`` will randomise the position of the elements
        of a selector's ``contents``.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4])
        >>> selector.contents
        [0, 1, 2, 3, 4]
        >>> selector.randomise()
        >>> selector.contents
        [1, 4, 3, 0, 2]

    ..  container:: example

        The contents of a selector can also be altered after it has been
        initialised using the ``contents`` property. The length of the
        contents can change as well.

        >>> selector = auxjad.CartographySelector([0, 1, 2, 3, 4],
        ...                                       decay_rate=0.5,
        ...                                       )
        >>> len(selector)
        5
        >>> selector.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]
        >>> selector.contents = [10, 7, 14, 31, 98, 47, 32]
        >>> selector.contents
        [10, 7, 14, 31, 98, 47, 32]
        >>> len(selector)
        7
        >>> selector.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]

    ..  container:: example

        Use the read-only properties ``previous_result`` and ``previous_index``
        to output the previous result and its index.

        >>> selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
        >>> selector()
        14
        >>> previous_index = selector.previous_index
        >>> previous_index
        2
        >>> selector.previous_result
        14

    ..  container:: example

        This class allows indecing and slicing just like regular lists. This
        can be used to both access and alter elements.

        >>> selector = auxjad.CartographySelector([10, 7, 14, 31, 98])
        >>> selector[1]
        7
        >>> selector[1:4]
        [7, 14, 31]
        >>> selector[:]
        [10, 7, 14, 31, 98]
        >>> selector()
        31
        >>> previous_index = selector.previous_index
        >>> previous_index
        3
        >>> selector[previous_index]
        31
        >>> selector.contents
        [10, 7, 14, 31, 98]
        >>> selector[2] = 100
        >>> selector.contents
        [10, 7, 100, 31, 98]
    """

    ### INITIALISER ###

    def __init__(self,
                 contents: list,
                 *,
                 decay_rate: float = 0.75,
                 ):
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list'")
        if not isinstance(decay_rate, float):
            raise TypeError("'decay_rate' must be 'float'")
        if decay_rate <= 0.0 or decay_rate > 1.0:
            raise ValueError("'decay_rate' must be larger than 0.0 and "
                             "less than or equal to 1.0")
        self._contents = contents[:]
        self._previous_index = None
        self._decay_rate = decay_rate
        self._generate_weights()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Outputs the representation of ``contents``.'
        return str(self._contents)

    def __call__(self,
                 *,
                 no_repeat: bool = False,
                 ):
        r'Call the selection process and outputs one element of ``contents``.'
        if not isinstance(no_repeat, bool):
            raise TypeError("'no_repeat' must be 'bool")
        if not no_repeat:
            new_index = random.choices(
                [n for n in range(self.__len__())],
                weights=self.weights,
            )[0]
        else:
            new_index = self._previous_index
            while (new_index == self._previous_index):
                new_index = random.choices(
                    [n for n in range(self.__len__())],
                    weights=self.weights,
                )[0]
        self._previous_index = new_index
        return self._contents[self._previous_index]

    def __next__(self,
                 *,
                 no_repeat: bool = False,
                 ):
        r'Call the selection process and outputs one element of ``contents``.'
        return self.__call__(no_repeat=no_repeat)

    def __len__(self) -> int:
        r'Outputs the length of ``contents``.'
        return len(self._contents)

    def __getitem__(self, key: int):
        r"""Implements reading elements of ``contents`` through indexing or
        slicing of instance.
        """
        return self._contents[key]

    def __setitem__(self, key, value):
        r"""Implements writing elements into ``contents`` through indexing or
        slicing of instance.
        """
        self._contents[key] = value

    ### PUBLIC METHODS ###

    def append(self, new_element):
        r"""A type of content transformation, it discards the first element of
        the ``contents``, shifts all others leftwards, and then appends the new
        element to the last index.
        """
        self._contents = self._contents[1:] + [new_element]

    def append_keeping_n(self, new_element, n: int):
        r"""A type of content transformation similar to ``append()``, it keeps
        the first ``n`` elements of ``contents`` untouched, it then discards
        the n+1-th element, shifts all the next elements one position lefwards,
        and finally appends the new element at the last index.
        """
        self._contents = (self._contents[:n]
                          + self._contents[n+1:]
                          + [new_element])

    def prepend(self, new_element):
        r"""A type of content transformation, it discards the last element of
        the ``contents``, shifts all others rightwards, and then prepends the
        new element to the first index.
        """
        self._contents = [new_element] + self._contents[:-1]

    def rotate(self, anticlockwise=False):
        r"""A type of content transformation, it rotates all elements
        rightwards, moving the last element to the first index. If the optional
        keyword argument ``anticlockwise`` is set to ``True``, the rotation
        will be in the opposite direction.
        """
        if not anticlockwise:
            self._contents = self._contents[1:] + self._contents[:1]
        else:
            self._contents = self._contents[-1:] + self._contents[:-1]

    def mirror(self, index: int):
        r"""A type of content transformation which swaps the element of the
        input index with its complementary element. Complementary elements are
        defined as the pair of elements which share the same distance from the
        centre of the ``contents`` (in terms of number of indeces), and are
        located at either side.
        """
        aux = self._contents[index]
        self._contents[index] = self._contents[-1 - index]
        self._contents[-1 - index] = aux

    def mirror_random(self):
        r"""A type of content transformation which swaps the element of a
        random index with its complementary element. Complementary elements are
        defined as the pair of elements which share the same distance from the
        centre of the ``contents`` (in terms of number of indeces), and are
        located at either side.
        """
        max_index = self.__len__() // 2 - 1
        self.mirror(random.randint(0, max_index))

    def randomise(self):
        r'Randomises the position of the elements of ``contents``.'
        random.shuffle(self._contents)

    ### PRIVATE METHODS ###

    def _generate_weights(self):
        r"""Given a decay rate, this method generates the weights of individual
        indeces.
        """
        self.weights = []
        for n in range(self.__len__()):
            self.weights.append(self._decay_rate ** n)

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> list:
        r'The ``list`` from which the selector picks elements.'
        return self._contents

    @contents.setter
    def contents(self,
                 contents: list
                 ):
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list")
        self._contents = contents[:]
        self._generate_weights()

    @property
    def decay_rate(self) -> float:
        r"""The decay rate represents the ratio of probabilities of any index
        given the probability of the preceeding one. For instance, if the decay
        rate is set to ``0.75`` (which is its default value), the probability
        of the element in index 1 of the input list being selected is 0.75 the
        probability of the element in index 0, and the probability of the
        element in index 2 is 0.5625 (0.75^2) the probability of the element in
        index 0.
        """
        return self._decay_rate

    @decay_rate.setter
    def decay_rate(self,
                   decay_rate: float):
        if not isinstance(decay_rate, float):
            raise TypeError("'decay_rate' must be float")
        if decay_rate <= 0.0 or decay_rate > 1.0:
            raise ValueError("'decay_rate' must be larger than 0.0 and less "
                             "than or equal to 1.0")
        self._decay_rate = decay_rate
        self._generate_weights()

    @property
    def previous_index(self):
        r"""Read-only property, returns the index of the previously output
        element.
        """
        return self._previous_index

    @property
    def previous_result(self):
        r'Read-only property, returns the previously output element.'
        return self._contents[self._previous_index]
