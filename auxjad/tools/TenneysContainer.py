import random


class TenneysContainer():
    r"""TenneysContainer in an implementation of the Dissonant Counterpoint
    Algorithm by James Tenney. This class can be used to randomly select
    elements from an input list, giving more weight to elements which have not
    been selected in recent iterations. In other words, Tenney's algorithm
    uses feedback in order to lower the weight of recently selected elements.

    This implementation is based on the paper: Polansky, L., A. Barnett, and
    M. Winter (2011). `A Few More Words About James Tenney: Dissonant
    Counterpoint and Statistical Feedback'. In: Journal of Mathematics and 
    Music 5(2). pp. 63--82.

    ..  container:: example

        The container should be initialised with a list of objects. The
        contents of the list can be absolutely anything.

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> container.contents
        ['A', 'B', 'C', 'D', 'E', 'F']

        Applying the len() function to the container will give the length of
        the container.

        >>> len(container)
        6

        When no other keyword arguments are used, the default probabilities of
        each element in the list is 1.0. Probabilities are not normalised. Use
        the previous_index attribute to check the previously selected index
        (default is None).

        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.previous_index
        None

        Calling the container will output one of its elements, selected
        according to the current probability values. After each call, the
        object updates all probability values, setting the previously selected
        element's probability at 0.0 and raising all other probabilities
        according to a growth function (more on this below).

        >>> result = ''
        >>> for _ in range(30):
        ...     result += container()
        >>> result
        'EDFACEABAFDCEDAFADCBFEDABEDFEC'

        From the result above it is possible to see that there are no immediate
        repetitions of elements (since once selected, their probability is
        always set to 0.0 and will take at least one iteration to grow to a
        non-zero value). Checking the probabilities and previous_index
        attributes will give us their current values.

        >>> container.probabilities
        [6.0, 5.0, 0.0, 3.0, 1.0, 2.0]
        >>> container.previous_index
        2

    ..  container:: example

        This class can take two optional keywords argument during its
        instantiation, namely weights and curvature. weights takes a list of
        floats with the individual weights of each element; by default, all
        weights are set to 1.0. These weights affects the effective
        probability of each element. The other argument, curvature, is the
        exponent of the growth function for all elements. The growth function
        takes as input the number of iterations since an element has been last
        selected, and raise this number by the curvature value. If curvature
        is set to 1.0 (which is its default value), the growth is linear with
        each iteration. If set to a value larger than 0.0 and less than 1.0,
        the growth is negative (or concave), so that the chances of an element
        which is not being selected will grow at ever smaller rates as the
        number of iterations it has not been selected increase. If the
        curvature is set to 1.0, the growth is linear with the number of
        iterations. If the curvature is larger than 1.0, the curvature is
        positive (or convex) and the growth will accelerate as the number of
        iterations an element has not been selected grows. Setting the
        curvature to 0.0 will result in an static probability vector with all
        values set to 1.0, except for the previously selected one which will be
        set to 0.0; this will result in a uniformly random selection without
        repetition.

        With linear curvature (default value of 1.0):

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> container.curvature
        1.0
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container()
        'B'
        >>> container.curvature
        1.0
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [2.0, 0.0, 2.0, 2.0, 2.0, 2.0]

    ..  container:: example

        Using a convex curvature:

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'],
        ...                                     curvature=0.2,
        ...                                     )
        >>> container.curvature
        0.2
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container()
        'C'
        >>> container.curvature
        0.2
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [1.148698354997035, 1.148698354997035, 0.0, 1.148698354997035,
        1.148698354997035, 1.148698354997035]

        With a convex curvature, the growth of the probability of each
        non-selected term gets smaller as the number of times it is not
        selected increases. The smaller the curvature is, the less difference
        there will be between any non-previously selected elements. This
        results in sequences which have more chances of a same element being
        near each other. In the sequence below, note how there are many cases
        of a same element being separated only by a single other one, such as
        'ACA' in index 6.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += container()
        >>> result
        'DACBEDFACABDACECBEFAEDBAFBABFD'

        Checking the probability values at this point outputs:

        >>> container.probabilities
        [1.2457309396155174, 1.148698354997035, 1.6952182030724354, 0.0,
        1.5518455739153598, 1.0]

        As we can see, all non-zero values are relatively close to each other,
        which is why there is a high chance of an element being selected again
        just two iterations apart.

    ..  container:: example

        Using a concave curvature:

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'],
        ...                                     curvature=15.2,
        ...                                     )
        >>> container.curvature
        0.2
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container()
        'C'
        >>> container.curvature
        0.2
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [37640.547696542824, 37640.547696542824, 37640.547696542824, 0.0,
        37640.547696542824, 37640.547696542824]

        With a concave curvature, the growth of the probability of each
        non-selected term gets larger as the number of times it is not selected
        increases. The larger the curvature is, the larger difference there
        will be between any non-previously selected elements. This results in
        sequences which have less chances of a same element being near each
        other. In the sequence below, with a curvature of 15.2, note how the
        elements are as far apart from each other, resulting in a repeating
        string of 'DFAECB'.

        >>> result = ''
        >>> for _ in range(30):
        ...     result += container()
        >>> result
        'DFAECBDFAECBDFAECBDFAECBDFAECB'

        Checking the probability values at this point outputs:

        >>> container.probabilities
        [17874877.39956566, 0.0, 1.0, 42106007735.02238,
        37640.547696542824, 1416810830.8957152]

        As we can see, the non-zero values vary wildly. The higher the
        curvature, the higher the difference between these values, making some
        of them much more likely to be selected.

    ..  container:: example

        Each element can also have a fixed weight to themselves. This will
        affect the probability calculation. The example below uses the default
        linear curvature.

        >>> container = auxjad.TenneysContainer(
        ...     ['A', 'B', 'C', 'D', 'E', 'F'],
        ...     weights=[1.0, 1.0, 5.0, 5.0, 10.0, 20.0],
        >>> )
        >>> container.weights
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> container.probabilities
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> result = ''
        >>> for _ in range(30):
        ...     result += container()
        >>> result
        'FBEFECFDEADFEDFEDBFECDAFCEDCFE'
        >>> container.weights
        [1.0, 1.0, 5.0, 5.0, 10.0, 20.0]
        >>> container.probabilities
        [7.0, 12.0, 10.0, 15.0, 0.0, 20.0]

    ..  container:: example

        To reset the probability to its initial value, use the method
        reset_probabilities().

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     container()
        >>> container.probabilities
        [4.0, 3.0, 1.0, 0.0, 5.0, 2.0]
        >>> container.reset_probabilities()
        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    ..  container:: example

        To replace an element in the container, use the method
        replace_element(). This will not affect the current probability vector,
        and the new element will have the same probability as the one it
        replaced.

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     container()
        >>> container.replace_element('foo', 2)
        >>> container.contents
        ['A', 'B', 'foo', 'D', 'E', 'F']
        >>> container.probabilities
        [3.0, 2.0, 1.0, 7.0, 5.0, 0.0]

    ..  container:: example

        A new container of an arbitrary length can be set at any point using
        the method set_container(). Do notice that the probabilities will be
        reset at that point. This method can take the optional keyword argument
        weights similarly to when instantiating the class.

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> for _ in range(30):
        ...     container()
        >>> container.probabilities
        [2.0, 1.0, 4.0, 3.0, 0.0, 5.0]
        >>> container.set_container([2, 4, 6, 8])
        >>> container.contents
        [2, 4, 6, 8]
        >>> len(container)
        4
        >>> container.weights
        [1.0, 1.0, 1.0, 1.0]
        >>> container.probabilities
        [1.0, 1.0, 1.0, 1.0]

    ..  container:: example

        To change the curvature value at any point, use the set_curvature()
        method.

        >>> container = auxjad.TenneysContainer(['A', 'B', 'C', 'D', 'E', 'F'])
        >>> container.curvature
        1.0
        >>> container.set_curvature(0.25)
        >>> container.curvature
        0.25
    """

    def __init__(self,
                 container: list,
                 *,
                 weights: list = None,
                 curvature: float = 1.0,
                 ):
        if not isinstance(container, list):
            raise TypeError("'container' must be 'list'")
        if weights:
            if not isinstance(weights, list):
                raise TypeError("'weights' must be 'list'")
            if not len(container) == len(weights):
                raise ValueError("'weights' must have the same length "
                                 "as 'container'")
            if not all(isinstance(weight, (int, float)) \
                       for weight in weights):
                raise TypeError("'weights' elements must be "
                                "'int' or 'float'")
        if not isinstance(curvature, float):
            raise TypeError("'curvature' must be 'float'")
        if curvature < 0.0:
            raise ValueError("'curvature' must be larger than 0.0")

        self.contents = container[:]
        if weights:
            self.weights = weights[:]
        else:
            self.weights = [1.0 for _ in self.contents]
        self._counter = [1 for _ in self.contents]
        self.previous_index = None
        self.curvature = curvature
        self._generate_probabilities()

    def __call__(self):
        self.previous_index = random.choices(
            [n for n in range(self.__len__())],
            weights=self.probabilities,
            )[0]
        self._regenerate_counts()
        self._generate_probabilities()
        return self.contents[self.previous_index]

    def __len__(self):
        return len(self.contents)

    def get_element(self, index: int):
        return self.contents[index]

    def replace_element(self, new_element, index: int):
        self.contents = self.contents[:index] \
                      + [new_element] \
                      + self.contents[index+1:]

    def set_container(self,
                      new_container: list,
                      *,
                      weights: list = None,
                      ):
        if not isinstance(new_container, list):
            raise TypeError("'new_container' must be 'list")
        if weights:
            if not isinstance(weights, list):
                raise TypeError("'weights' must be 'list'")
            if not len(new_container) == len(weights):
                raise ValueError("'weights' must have the same length "
                                 "as 'new_container'")
            if not all(isinstance(weight, (int, float)) \
                       for weight in weights):
                raise TypeError("'weights' elements must be "
                                "'int' or 'float'")

        self.contents = new_container[:]
        if weights:
            self.weights = weights[:]
        else:
            self.weights = [1.0 for _ in self.contents]
        self._generate_probabilities(reset=True)

    def set_curvature(self, new_curvature):
        if not isinstance(new_curvature, float):
            raise TypeError("'new_curvature' must be 'float'")
        if new_curvature < 0.0:
            raise ValueError("'new_curvature' must be larger than 0.0")
        self.curvature = new_curvature
        self._generate_probabilities()

    def reset_probabilities(self):
        self._counter = [1 for _ in self.contents]
        self._generate_probabilities()

    def _regenerate_counts(self):
        for i in range(self.__len__()):
            if i == self.previous_index:
                self._counter[i] = 0
            else:
                self._counter[i] += 1

    def _generate_probabilities(self, reset=False):
        if reset:
            self._counter = [1 for _ in self.contents]
        self.probabilities = []
        for weight, count in zip(self.weights, self._counter):
            self.probabilities.append(weight * self._growth_function(count))

    def _growth_function(self, count):
        return count ** self.curvature
