import random


class CartographyContainer():
    r"""A container used to store, manipulate, and select objects using a
    decaying weighted function.

    ..  container:: example

        The container should be initialised with a list of objects. The
        contents of the list can be absolutely anything.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]

        The default decay rate is 0.75; that is, the weight of any given
        elements is the weight of the previous one multiplied by 0.75. The
        weights are associated with the index position, not the elements
        themselves.

        >>> container.weights
        [1.0, 0.75, 0.5625, 0.421875, 0.31640625]

        Applying the ``len()`` function to the container will give the length
        of the container.

        >>> len(container)
        5

        Calling the container will output one of its elements, selected
        according to its weight function.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(container())
        >>> result
        203001402200011111101400310140

    ..  container:: example

        Calling the container with the optional keyword argument ``no_repeat``
        set to ``True`` will forbid immediate repetitions among consecutive
        calls.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(container(no_repeat=True))
        >>> result
        210421021020304024230120241202

    ..  container:: example

        The keyword argument ``decay_rate`` can be used to set a different
        decay rate when creating a container.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4],
        ...                                         decay_rate=0.5,
        ...                                         )
        >>> cartography_container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]

        The decay rate can also be set after the creation of a container,
        using the property ``decay_rate``.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.decay_rate = 0.2
        >>> container.weights
        [1.0, 0.2, 0.04000000000000001, 0.008000000000000002,
        0.0016000000000000003]
        >>> result = ''
        >>> for _ in range(30):
        ...     result += str(container())
        >>> result
        '000001002100000201001030000100'

    ..  container:: example

        Appending is a type of container transformation. It discards the first
        element of the container, shifts all others leftwards, and then appends
        the new element to the rightmost index.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.append(5)
        >>> container.contents
        [1, 2, 3, 4, 5]
        >>> container.append(42)
        >>> container.contents
        [2, 3, 4, 5, 42]

    ..  container:: example

        The method ``append_keeping_n()`` is similar to ``append()``, but it
        keeps the first n indeces untouched. It thus discards the n+1-th
        element, shifts all the next ones lefwards and then appends the new
        element at the end of the container.

        >>> container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
        >>> container.contents
        [10, 7, 14, 31, 98]
        >>> container.append_keeping_n(100, 2)
        >>> container.contents
        [10, 7, 31, 98, 100]

    ..  container:: example

        Prepending is another type of container transformation. It discards the
        last element of the container, shifts all others rightwards, and then
        prepends the new element to the leftmost index.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.prepend(-1)
        >>> container.contents
        [-1, 0, 1, 2, 3]
        >>> container.prepend(71)
        >>> container.contents
        [71, -1, 0, 1, 2]

    ..  container:: example

        Rotation is another type of container transformation. It rotates all
        elements rightwards, while moving the rightmost element into the
        leftmost index. It can take the optional keyword argument anticlockwise
        which if set to ``True`` will rotate in the opposite direction.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.rotate()
        >>> container.contents
        [1, 2, 3, 4, 0]
        >>> container.rotate(anticlockwise=True)
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.rotate(anticlockwise=True)
        >>> container.contents
        [1, 2, 3, 4, 0]

    ..  container:: example

        It is also possible to mirror two elements around a pivot at the centre
        of the container; given an element (selected by its index), this
        operation will locate and swap it for its complementary element. The
        complementary element is defined as that one which is at a same
        distance from the centre pivot but in the opposite direction.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.mirror(0)
        >>> container.contents
        [4, 1, 2, 3, 0]
        >>> container.mirror(0)
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.mirror(3)
        >>> container.contents
        [0, 3, 2, 1, 4]
        >>> container.mirror(2)
        >>> container.contents
        [0, 3, 2, 1, 4]

    ..  container:: example

        To mirror a random pair of complementary elements, use the
        ``mirror_random()`` method. In case of a container with an odd number
        of elements, this method will never pick an element at the pivot point
        since the operation would not change the contents.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.mirror_random()
        >>> container.contents
        [4, 1, 2, 3, 0]
        >>> container.mirror_random()
        >>> container.contents
        [4, 3, 2, 1, 0]
        >>> container.mirror_random()
        >>> container.contents
        [4, 1, 2, 3, 0]

    ..  container:: example

        The method ``randomise()`` will randomise the position of the elements
        of a container.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.randomise()
        >>> container.contents
        [1, 4, 3, 0, 2]

    ..  container:: example

        The contents of a container can also be altered after it has been
        initialised using the ``container`` property. The length of the
        container can change as well.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4],
        ...                                         decay_rate=0.5,
        ...                                         )
        >>> len(container)
        5
        >>> container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]
        >>> container.contents = [10, 7, 14, 31, 98, 47, 32]
        >>> container.contents
        [10, 7, 14, 31, 98, 47, 32]
        >>> len(container)
        7
        >>> container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]

    ..  container:: example

        This class allows indecing and slicing just like regular lists. This
        can be used to both access and alter elements.

        >>> container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
        >>> container[1]
        7
        >>> container[1:4]
        [7, 14, 31]
        >>> container[:]
        [10, 7, 14, 31, 98]
        >>> container()
        31
        >>> previous_index = container.previous_index
        >>> previous_index
        3
        >>> container[previous_index]
        31
        >>> container.contents
        [10, 7, 14, 31, 98]
        >>> container[2] = 100
        >>> container.contents
        [10, 7, 100, 31, 98]
    """

    def __init__(self,
                 container: list,
                 *,
                 decay_rate: float = 0.75,
                 ):
        if not isinstance(container, list):
            raise TypeError("'container' must be 'list'")
        if not isinstance(decay_rate, float):
            raise TypeError("'decay_rate' must be 'float'")
        if decay_rate <= 0.0 or decay_rate > 1.0:
            raise ValueError("'decay_rate' must be larger than 0.0 and "
                             "less than or equal to 1.0")
        self._contents = container[:]
        self.previous_index = None
        self._decay_rate = decay_rate
        self._generate_weights()

    def __repr__(self) -> str:
        return str(self._contents)

    def __call__(self, no_repeat=False):
        if not no_repeat:
            new_index = random.choices(
                [n for n in range(self.__len__())],
                weights=self.weights,
                )[0]
        else:
            new_index = self.previous_index
            while (new_index == self.previous_index):
                new_index = random.choices(
                    [n for n in range(self.__len__())],
                    weights=self.weights,
                    )[0]
        self.previous_index = new_index
        return self._contents[self.previous_index]

    def __len__(self) -> int:
        return len(self._contents)

    def __getitem__(self, key: int):
        return self._contents[key]

    def __setitem__(self, key, value):
        self._contents[key] = value

    @property
    def contents(self) -> list:
        return self._contents

    @contents.setter
    def contents(self,
                 new_container: list
                 ):
        if not isinstance(new_container, list):
            raise TypeError("'new_container' must be 'list")
        self._contents = new_container[:]
        self._generate_weights()

    @property
    def decay_rate(self) -> float:
        return self._decay_rate

    @decay_rate.setter
    def decay_rate(self,
                   new_decay_rate: float):
        if not isinstance(new_decay_rate, float):
            raise TypeError("'new_decay_rate' must be float")
        if new_decay_rate <= 0.0 or new_decay_rate > 1.0:
            raise ValueError("'new_decay_rate' must be larger than 0.0 and "
                             "less than or equal to 1.0")
        self._decay_rate = new_decay_rate
        self._generate_weights()

    def append(self, new_element):
        self._contents = self._contents[1:] + [new_element]

    def append_keeping_n(self, new_element, n: int):
        self._contents = self._contents[:n] \
                      + self._contents[n+1:] \
                      + [new_element]

    def prepend(self, new_element):
        self._contents = [new_element] + self._contents[:-1]

    def rotate(self, anticlockwise=False):
        if not anticlockwise:
            self._contents = self._contents[1:] + self._contents[:1]
        else:
            self._contents = self._contents[-1:] + self._contents[:-1]

    def mirror(self, index: int):
        aux = self._contents[index]
        self._contents[index] = self._contents[-1 - index]
        self._contents[-1 - index] = aux

    def mirror_random(self):
        max_index = self.__len__() // 2 - 1
        self.mirror(random.randint(0, max_index))

    def randomise(self):
        random.shuffle(self._contents)

    def _generate_weights(self):
        self.weights = []
        for n in range(self.__len__()):
            self.weights.append(self._decay_rate ** n)
