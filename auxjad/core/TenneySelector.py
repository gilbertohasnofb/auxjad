import random


class TenneySelector():
    r"""This in an implementation of the Dissonant Counterpoint Algorithm by
    James Tenney. This class can be used to randomly select elements from an
    input list, giving more weight to elements which have not been selected in
    recent iterations. In other words, Tenney's algorithm uses feedback in
    order to lower the weight of recently selected elements.

    This implementation is based on the paper: Polansky, L., A. Barnett, and
    M. Winter (2011). 'A Few More Words About James Tenney: Dissonant
    Counterpoint and Statistical Feedback'. In: Journal of Mathematics and
    Music 5(2). pp. 63--82.

    ..  container:: example

        The selector should be initialised with a list of objects. The contents
        of the list can be absolutely anything.

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> selector.contents
        ['A', 'B', 'C', 'D', 'E', 'F']

        Applying the ``len()`` function to the selector will give the length
        of the input list.

        >>> len(selector)
        6

        When no other keyword arguments are used, the default probabilities of
        each element in the list is 1.0. Probabilities are not normalised. Use
        the previous_index attribute to check the previously selected index
        (default is None).

        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.previous_index
        None

        Calling the selector will output one of its elements, selected
        according to the current probability values.

        >>> selector()
        C

        Alternatively, use the ``next()`` function or ``__next__()`` method to
        get the next result.

        >>> selector.__next__()
        A
        >>> next(selector)
        D

        After each call, the object updates all probability values, setting the
        previously selected element's probability at 0.0 and raising all other
        probabilities according to a growth function (more on this below).

        >>> result = ''
        >>> for _ in range(30):
        ...     result += selector()
        >>> result
        EDFACEABAFDCEDAFADCBFEDABEDFEC

        From the result above it is possible to see that there are no immediate
        repetitions of elements (since once selected, their probability is
        always set to 0.0 and will take at least one iteration to grow to a
        non-zero value). Checking the probabilities and previous_index
        attributes will give us their current values.

        >>> selector.probabilities
        [6.0, 5.0, 0.0, 3.0, 1.0, 2.0]
        >>> selector.previous_index
        2

    ..  container:: example

        This class can take two optional keywords argument during its
        instantiation, namely ``weights`` and ``curvature``. ``weights`` takes
        a list of floats with the individual weights of each element; by
        default,  all weights are set to 1.0. These weights affects the
        effective probability of each element. The other argument,
        ``curvature``, is the exponent of the growth function for all elements.
        The growth function takes as input the number of iterations since an
        element has been last selected, and raise this number by the curvature
        value. If ``curvature`` is set to 1.0 (which is its default value), the
        growth is linear with each iteration. If set to a value larger than 0.0
        and less than 1.0, the growth is negative (or concave), so that the
        chances of an element which is not being selected will grow at ever
        smaller rates as the number of iterations it has not been selected
        increase. If the ``curvature`` is set to 1.0, the growth is linear with
        the number of iterations. If the ``curvature`` is larger than 1.0, the
        curvature is positive (or convex) and the growth will accelerate as the
        number of iterations an element has not been selected grows. Setting
        the curvature to 0.0 will result in an static probability vector with
        all values set to 1.0, except for the previously selected one which
        will be set to 0.0; this will result in a uniformly random selection
        without repetition.

        With linear curvature (default value of 1.0):

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> selector.curvature
        1.0
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector()
        'B'
        >>> selector.curvature
        1.0
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [2.0, 0.0, 2.0, 2.0, 2.0, 2.0]

    ..  container:: example

        Using a convex curvature:

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
        ...                                  curvature=0.2,
        ...                                  )
        >>> selector.curvature
        0.2
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector()
        'C'
        >>> selector.curvature
        0.2
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [1.148698354997035, 1.148698354997035, 0.0, 1.148698354997035,
        1.148698354997035, 1.148698354997035]

        With a convex curvature, the growth of the probability of each
        non-selected term gets smaller as the number of times it is not
        selected increases. The smaller the curvature is, the less difference
        there will be between any non-previously selected elements. This
        results in sequences which have more chances of a same element being
        near each other. In the sequence below, note how there are many cases
        of a same element being separated only by a single other one, such as
        ``'ACA'`` in index 6.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += selector()
        >>> result
        DACBEDFACABDACECBEFAEDBAFBABFD

        Checking the probability values at this point outputs:

        >>> selector.probabilities
        [1.2457309396155174, 1.148698354997035, 1.6952182030724354, 0.0,
        1.5518455739153598, 1.0]

        As we can see, all non-zero values are relatively close to each other,
        which is why there is a high chance of an element being selected again
        just two iterations apart.

    ..  container:: example

        Using a concave curvature:

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'],
        ...                                  curvature=15.2,
        ...                                  )
        >>> selector.curvature
        0.2
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector()
        'C'
        >>> selector.curvature
        0.2
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [37640.547696542824, 37640.547696542824, 37640.547696542824, 0.0,
        37640.547696542824, 37640.547696542824]

        With a concave curvature, the growth of the probability of each
        non-selected term gets larger as the number of times it is not selected
        increases. The larger the curvature is, the larger difference there
        will be between any non-previously selected elements. This results in
        sequences which have less chances of a same element being near each
        other. In the sequence below, with a curvature of 15.2, note how the
        elements are as far apart from each other, resulting in a repeating
        string of ``'DFAECB'``.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += selector()
        >>> result
        DFAECBDFAECBDFAECBDFAECBDFAECB

        Checking the probability values at this point outputs:

        >>> selector.probabilities
        [17874877.39956566, 0.0, 1.0, 42106007735.02238,
        37640.547696542824, 1416810830.8957152]

        As we can see, the non-zero values vary wildly. The higher the
        curvature, the higher the difference between these values, making some
        of them much more likely to be selected.

    ..  container:: example

        Each element can also have a fixed weight to themselves. This will
        affect the probability calculation. The example below uses the default
        linear curvature.

        >>> selector = auxjad.TenneySelector(
        ...     ['A', 'B', 'C', 'D', 'E', 'F'],
        ...     weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
        >>> )
        >>> selector.weights
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> selector.probabilities
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> result = ''
        >>> for _ in range(30):
        ...     result += selector()
        >>> result
        FBEFECFDEADFEDFEDBFECDAFCEDCFE
        >>> selector.weights
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> selector.probabilities
        [7.0, 12.0, 10.0, 15.0, 0.0, 20.0]

    ..  container:: example

        To reset the probability distribution of all elements to its initial
        value (an uniform distribution), use the method
        ``reset_probabilities()``.

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     selector()
        >>> selector.probabilities
        [4.0, 3.0, 1.0, 0.0, 5.0, 2.0]
        >>> selector.reset_probabilities()
        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    ..  container:: example

        This class allows slicing to get and set values of contents of the
        selector. This will not affect the current probability vector, and the
        new element will have the same probability as the one it replaced.

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     selector()
        >>> selector.probabilities
        [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]
        >>> selector[2]
        'C'
        >>> selector[1:4]
        ['B', 'C', 'D']
        >>> selector[2] = 'foo'
        >>> selector.contents
        ['A', 'B', 'foo', 'D', 'E', 'F']
        >>> selector[:] = ['foo', 'bar', 'X', 'Y', 'Z', '...']
        >>> selector.contents
        ['foo', 'bar', 'X', 'Y', 'Z', '...']
        >>> selector.probabilities
        [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]

        You can also check if the instance contains a specific element. In the
        case of the selector above, we have:

        >>> 'foo' in selector
        True
        >>> 'A' in selector
        False

    ..  container:: example

        A new list of an arbitrary length can be set at any point using the
        property ``contents``. Do notice that the probabilities will be reset
        at that point. This method can take the optional keyword argument
        weights similarly to when instantiating the class.

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     selector()
        >>> selector.probabilities
        [2.0, 1.0, 4.0, 3.0, 0.0, 5.0]
        >>> selector.contents
        ['A', 'B', 'C', 'D', 'E', 'F']
        >>> selector.contents = [2, 4, 6, 8]
        >>> selector.contents
        [2, 4, 6, 8]
        >>> len(selector)
        4
        >>> selector.weights
        [1.0, 1.0, 1.0, 1.0]
        >>> selector.probabilities
        [1.0, 1.0, 1.0, 1.0]

    ..  container:: example

        To change the curvature value at any point, simply set the property
        ``curvature`` to a different value.

        >>> selector = auxjad.TenneySelector(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> selector.curvature
        1.0
        >>> selector.curvature = 0.25
        >>> selector.curvature
        0.25
    """

    ### INITIALISER ###

    def __init__(self,
                 contents: list,
                 *,
                 weights: list = None,
                 curvature: float = 1.0,
                 ):
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list'")
        if weights:
            if not isinstance(weights, list):
                raise TypeError("'weights' must be 'list'")
            if not len(contents) == len(weights):
                raise ValueError("'weights' must have the same length "
                                 "as 'contents'")
            if not all(isinstance(weight, (int, float))
                       for weight in weights):
                raise TypeError("'weights' elements must be "
                                "'int' or 'float'")
        if not isinstance(curvature, float):
            raise TypeError("'curvature' must be 'float'")
        if curvature < 0.0:
            raise ValueError("'curvature' must be larger than 0.0")

        self._contents = contents[:]
        if weights:
            self._weights = weights[:]
        else:
            self._weights = [1.0 for _ in range(self.__len__())]
        self._curvature = curvature
        self._counter = [1 for _ in range(self.__len__())]
        self._generate_probabilities()
        self._previous_index = None

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        r'Outputs the representation of ``contents``.'
        return str(self._contents)

    def __call__(self):
        r'Call the selection process and outputs one element of ``contents``.'
        self._previous_index = random.choices(
            [n for n in range(self.__len__())],
            weights=self.probabilities,
            )[0]
        self._regenerate_counts()
        self._generate_probabilities()
        return self._contents[self._previous_index]

    def __next__(self):
        r'Call the selection process and outputs one element of ``contents``.'
        return self.__call__()

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

    def reset_probabilities(self):
        r"""Resets the probability distribution of all elements to an uniform
        distribution.
        """
        self._counter = [1 for _ in range(self.__len__())]
        self._generate_probabilities()

    ### PRIVATE METHODS ###

    def _regenerate_counts(self):
        r"""Increases the count of all elements except for the previously
        selected one, whose count is reset to zero.
        """
        for i in range(self.__len__()):
            if i == self._previous_index:
                self._counter[i] = 0
            else:
                self._counter[i] += 1

    def _generate_probabilities(self,
                                reset: bool = False,
                                ):
        r"""Generates the probabilities given the weights of the elements as
        well as their count numbers (which are fed into the growth function).
        """
        if reset:
            self._counter = [1 for _ in range(self.__len__())]
        self.probabilities = []
        for weight, count in zip(self._weights, self._counter):
            self.probabilities.append(weight * self._growth_function(count))

    def _growth_function(self, count):
        r'Applies the growth exponent given a number of counts.'
        return count ** self._curvature

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self) -> list:
        r'The ``list`` from which the selector picks elements.'
        return self._contents

    @contents.setter
    def contents(self,
                 contents: list,
                 ):
        if not isinstance(contents, list):
            raise TypeError("'contents' must be 'list")
        self._contents = contents[:]
        self.weights = [1.0 for _ in range(self.__len__())]

    @property
    def weights(self) -> list:
        r'The ``list`` with weights for each element of ``contents``.'
        return self._weights

    @weights.setter
    def weights(self,
                weights: list,
                ):
        if not isinstance(weights, list):
            raise TypeError("'weights' must be 'list'")
        if not self.__len__() == len(weights):
            raise ValueError("'weights' must have the same length "
                             "as the contents of the object")
        if not all(isinstance(weight, (int, float))
                   for weight in weights):
            raise TypeError("'weights' elements must be "
                            "'int' or 'float'")
        self._weights = weights[:]
        self._generate_probabilities(reset=True)

    @property
    def curvature(self) -> list:
        r'The exponent of the growth function.'
        return self._curvature

    @curvature.setter
    def curvature(self,
                  curvature: float,
                  ):
        if not isinstance(curvature, float):
            raise TypeError("'curvature' must be 'float'")
        if curvature < 0.0:
            raise ValueError("'curvature' must be larger than 0.0")
        self._curvature = curvature
        self._generate_probabilities()

    @property
    def previous_index(self):
        r"""Read-only property, returns the index of the previously output
        element.
        """
        return self._previous_index
