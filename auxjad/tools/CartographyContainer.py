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

        Applying the len() function to the container will give the length of
        the container.

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

        The keyword argument decay_rate can be used to set a different decay
        rate when creating a container.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4],
        ...                                         decay_rate=0.5,
        ...                                         )
        >>> cartography_container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]

        The decay rate can also be set after the creation of a container,
        using the method set_decay_rate().

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.set_decay_rate(0.2)
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

        The method append_keeping_n() is similar to append(), but it keeps the
        first n indeces untouched. It thus discards the n+1-th element, shifts
        all the next ones lefwards and then appends the new element at the end
        of the container.

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
        which if set to True will rotate in the opposite direction.

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

        The method randomise() will randomise the position of the elements of
        a container.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4])
        >>> container.contents
        [0, 1, 2, 3, 4]
        >>> container.randomise()
        >>> container.contents
        [1, 4, 3, 0, 2]

    ..  container:: example

        The contents of a container can also be altered after it has been
        initialised using the set_container() method. The length of the
        container can change too.

        >>> container = auxjad.CartographyContainer([0, 1, 2, 3, 4],
        ...                                         decay_rate=0.5,
        ...                                         )
        >>> len(container)
        5
        >>> container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625]
        >>> container.set_container([10, 7, 14, 31, 98, 47, 32])
        >>> container.contents
        [10, 7, 14, 31, 98, 47, 32]
        >>> len(container)
        7
        >>> container.weights
        [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]

    ..  container:: example

        To method replace_element() replaces a specific element at a specified
        index.

        >>> container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
        >>> container.contents
        [10, 7, 14, 31, 98]
        >>> container.replace_element(100, 2)
        >>> container.contents
        [10, 7, 100, 31, 98]

    ..  container:: example

        The attribute previous_index stores the previously selected index. It
        can be used with the get_element() method in order to retrieve the last
        value output by the object.

        >>> container = auxjad.CartographyContainer([10, 7, 14, 31, 98])
        >>> container()
        31
        >>> previous_index = container.previous_index
        >>> previous_index
        3
        >>> container.get_element(previous_index)
        31
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
        self.contents = container[:]
        self.previous_index = None
        self._decay_rate = decay_rate
        self._generate_weights()

    def __call__(self):
        self.previous_index = random.choices(
            [n for n in range(self.__len__())],
            weights=self.weights,
            )[0]
        return self.contents[self.previous_index]

    def __len__(self):
        return len(self.contents)

    def append(self, new_element):
        self.contents = self.contents[1:] + [new_element]

    def append_keeping_n(self, new_element, n: int):
        self.contents = self.contents[:n] \
                      + self.contents[n+1:] \
                      + [new_element]

    def prepend(self, new_element):
        self.contents = [new_element] + self.contents[:-1]

    def rotate(self, anticlockwise=False):
        if not anticlockwise:
            self.contents = self.contents[1:] + self.contents[:1]
        else:
            self.contents = self.contents[-1:] + self.contents[:-1]

    def randomise(self):
        random.shuffle(self.contents)

    def get_element(self, index: int):
        return self.contents[index]

    def replace_element(self, new_element, index: int):
        self.contents = self.contents[:index] \
                      + [new_element] \
                      + self.contents[index+1:]

    def set_container(self, new_container: list):
        if not isinstance(new_container, list):
            raise TypeError("'new_container' must be 'list")
        self.contents = new_container[:]
        self._generate_weights()

    def set_decay_rate(self, new_decay_rate: float):
        if not isinstance(new_decay_rate, float):
            raise TypeError("'new_decay_rate' must be float")
        if new_decay_rate <= 0.0 or new_decay_rate > 1.0:
            raise ValueError("'new_decay_rate' must be larger than 0.0 and "
                             "less than or equal to 1.0")
        self._decay_rate = new_decay_rate
        self._generate_weights()

    def _generate_weights(self):
        self.weights = []
        for n in range(self.__len__()):
            self.weights.append(self._decay_rate ** n)
