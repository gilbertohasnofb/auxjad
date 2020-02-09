import abjad
import random


class CartographyContainer():
    r"""xxx

    ..  container:: example

        xxx

        >>> xxx
    """

    def __init__(self,
                 container: list,
                 decay_rate: float = 0.75,
                 ):
        if not isinstance(container, list):
            raise TypeError("'container' must be 'list")
        if not isinstance(decay_rate, float):
            raise TypeError("'decay_rate' must be float")
        if decay_rate <= 0.0 or decay_rate >= 1.0:
            raise ValueError("'decay_rate' must be between 0.0 and 1.0")
        self.container = container[:]
        self.last_index = None
        self.weights = []
        for n in range(self.__len__()):
            self.weights.append(decay_rate ** n)

    def __call__(self):
        self.last_index = random.choices([n for n in range(self.__len__())],
                                         weights=self.weights,
                                         )[0]
        return self.container[self.last_index]

    def __len__(self):
        return len(self.container)

    def append(self, new_element):
        self.container = self.container[1:] + [new_element]

    def append_keeping_n(self, new_element, n: int):
        self.container = self.container[:n] \
                       + self.container[n+1:] \
                       + [new_element]

    def prepend(self, new_element):
        self.container = [new_element] + self.container[:-1]

    def randomise(self):
        random.shuffle(self.container)

    def get_element(self, index: int):
        return self.container[index]

    def replace_element(self, new_element, index: int):
        self.container = self.container[:index] \
                       + [new_element] \
                       + self.container[index+1:]

    def set_container(self, new_container: list):
        if not isinstance(new_container, list):
            raise TypeError("'new_container' must be 'list")
        if len(new_container) != len(self.container):
            raise ValueError("'new_container' must have the same length as "
                             "the initial 'container'")
        self.container = new_container[:]

    def set_decay_ratio(self, new_decay_ratio: float):
        if not isinstance(new_decay_ratio, float):
            raise TypeError("'new_decay_ratio' must be float")
        if new_decay_ratio <= 0.0 or new_decay_ratio >= 1.0:
            raise ValueError("'new_decay_ratio' must be between 0.0 and 1.0")
        self.weights = []
        for n in range(self.__len__()):
            self.weights.append(new_decay_ratio ** n)






cartography_container = CartographyContainer([0, 1, 2, 3, 4])
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.append(5)
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.append_keeping_n(100, 2)
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.prepend(10)
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.randomise()
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.set_container([10, 20, 30, 40, 50])
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.replace_element(100, 2)
print(cartography_container.container)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

cartography_container.set_decay_ratio(0.2)
print(cartography_container.container)
print(cartography_container.weights)
for _ in range(30):
    print(cartography_container(), end=' ')
print()
print('***')

n = cartography_container.last_index
print(cartography_container.get_element(n))
print(cartography_container.get_element(n))
print(cartography_container.get_element(n))
