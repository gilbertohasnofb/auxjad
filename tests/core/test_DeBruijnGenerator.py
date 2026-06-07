import pytest

import auxjad


def is_valid_de_bruijn_cyclic(sequence, order, alphabet_size):
    if len(sequence) != alphabet_size**order:
        return False
    sequence_length = len(sequence)
    subgroups = set()
    for i in range(sequence_length):
        # converting subgroups to tuples as lists are not hashable and thus not allowed in sets
        subgroup = tuple(sequence[(i + j) % sequence_length] for j in range(order))
        subgroups.add(tuple(subgroup))
    return len(subgroups) == alphabet_size**order


def is_valid_de_bruijn_linear(sequence, order, alphabet_size):
    if len(sequence) != alphabet_size**order + (order - 1):
        return False
    subgroups = set()
    for i in range(len(sequence) - order + 1):
        # converting subgroups to tuples as lists are not hashable and thus not allowed in sets
        subgroup = tuple(sequence[i : i + order])
        subgroups.add(subgroup)
    return len(subgroups) == alphabet_size**order


class TestInit:
    def test_contents_not_list_raises(self):
        with pytest.raises(TypeError):
            auxjad.DeBruijnGenerator((0, 1), order=2)

    def test_contents_too_short_raises(self):
        with pytest.raises(ValueError):
            auxjad.DeBruijnGenerator([0], order=2)

    def test_contents_empty_raises(self):
        with pytest.raises(ValueError):
            auxjad.DeBruijnGenerator([], order=2)

    def test_order_not_int_raises(self):
        with pytest.raises(TypeError):
            auxjad.DeBruijnGenerator([0, 1], order=2.0)

    def test_order_zero_raises(self):
        with pytest.raises(ValueError):
            auxjad.DeBruijnGenerator([0, 1], order=0)

    def test_order_negative_raises(self):
        with pytest.raises(ValueError):
            auxjad.DeBruijnGenerator([0, 1], order=-1)

    def test_algorithm_not_str_raises(self):
        with pytest.raises(TypeError):
            auxjad.DeBruijnGenerator([0, 1], order=2, algorithm=1)

    def test_algorithm_invalid_raises(self):
        with pytest.raises(ValueError):
            auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="granddaddy")

    def test_cyclic_not_bool_raises(self):
        with pytest.raises(TypeError):
            auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=1)

    def test_default_algorithm_is_pcr1(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        assert db_generator.algorithm == "pcr1"

    def test_default_cyclic_is_false(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        assert db_generator.cyclic is False

    def test_contents_are_copied_on_init(self):
        original = [0, 1, 2]
        db_generator = auxjad.DeBruijnGenerator(original, order=2)
        original.append(3)
        assert len(db_generator) == 3

    def test_initial_state_before_any_call(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        assert db_generator.previous_element is None
        assert db_generator.previous_element_index is None
        assert db_generator.last_selected_index_of_sequence is None


class TestDeBruijnCorrectness:
    @pytest.mark.parametrize(
        "order, k",
        [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (2, 4),
            (2, 5),
        ],
    )
    def test_pcr1_cyclic_valid(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(
            list(range(k)), order=order, algorithm="pcr1", cyclic=True
        )
        assert is_valid_de_bruijn_cyclic(db_generator.output_all(), order, k)

    @pytest.mark.parametrize(
        "order, k",
        [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (2, 4),
            (2, 5),
        ],
    )
    def test_pcr2_cyclic_valid(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(
            list(range(k)), order=order, algorithm="pcr2", cyclic=True
        )
        assert is_valid_de_bruijn_cyclic(db_generator.output_all(), order, k)

    @pytest.mark.parametrize(
        "order, k",
        [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (2, 4),
            (2, 5),
        ],
    )
    def test_pcr1_linear_valid(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(
            list(range(k)), order=order, algorithm="pcr1", cyclic=False
        )
        assert is_valid_de_bruijn_linear(db_generator.output_all(), order, k)

    @pytest.mark.parametrize(
        "order, k",
        [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (1, 3),
            (2, 3),
            (3, 3),
            (2, 4),
            (2, 5),
        ],
    )
    def test_pcr2_linear_valid(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(
            list(range(k)), order=order, algorithm="pcr2", cyclic=False
        )
        assert is_valid_de_bruijn_linear(db_generator.output_all(), order, k)

    @pytest.mark.parametrize(
        "order, k",
        [
            (2, 2),
            (3, 2),
            (4, 2),
            (2, 3),
            (2, 4),
        ],
    )
    def test_cyclic_length_is_k_to_the_n(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(list(range(k)), order=order, cyclic=True)
        assert db_generator.sequence_length == k**order

    @pytest.mark.parametrize(
        "order, k",
        [
            (2, 2),
            (3, 2),
            (4, 2),
            (2, 3),
            (2, 4),
        ],
    )
    def test_linear_length_is_k_to_the_n_plus_order_minus_1(self, order, k):
        db_generator = auxjad.DeBruijnGenerator(list(range(k)), order=order, cyclic=False)
        assert db_generator.sequence_length == k**order + (order - 1)

    @pytest.mark.parametrize(
        "algorithm, alphabet, order, expected",
        [
            ("pcr1", [0, 1], 2, [0, 0, 1, 1]),
            ("pcr1", [0, 1], 3, [0, 0, 0, 1, 0, 1, 1, 1]),
            ("pcr1", [0, 1, 2], 2, [0, 0, 1, 0, 2, 1, 1, 2, 2]),
            ("pcr1", [0, 1, 2, 3], 2, [0, 0, 1, 0, 2, 0, 3, 1, 1, 2, 1, 3, 2, 2, 3, 3]),
            ("pcr2", [0, 1], 2, [0, 0, 1, 1]),
            ("pcr2", [0, 1], 3, [0, 0, 0, 1, 0, 1, 1, 1]),
            ("pcr2", [0, 1, 2], 2, [0, 0, 1, 1, 0, 2, 1, 2, 2]),
            ("pcr2", [0, 1, 2, 3], 2, [0, 0, 1, 1, 0, 2, 1, 2, 2, 0, 3, 1, 3, 2, 3, 3]),
        ],
    )
    def test_pinned_sequence_cyclic(self, algorithm, alphabet, order, expected):
        db_generator = auxjad.DeBruijnGenerator(
            alphabet, order=order, algorithm=algorithm, cyclic=True
        )
        assert db_generator.output_all() == expected

    @pytest.mark.parametrize(
        "algorithm, alphabet, order, expected",
        [
            ("pcr1", [0, 1], 2, [0, 0, 1, 1, 0]),
            ("pcr1", [0, 1, 2], 2, [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]),
            ("pcr2", [0, 1], 2, [0, 0, 1, 1, 0]),
            ("pcr2", [0, 1, 2], 2, [0, 0, 1, 1, 0, 2, 1, 2, 2, 0]),
        ],
    )
    def test_pinned_sequence_linear(self, algorithm, alphabet, order, expected):
        db_generator = auxjad.DeBruijnGenerator(
            alphabet, order=order, algorithm=algorithm, cyclic=False
        )
        assert db_generator.output_all() == expected

    def test_pcr1_and_pcr2_differ_for_order_4_binary(self):
        db_generator_pcr1 = auxjad.DeBruijnGenerator([0, 1], order=4, algorithm="pcr1", cyclic=True)
        db_generator_pcr2 = auxjad.DeBruijnGenerator([0, 1], order=4, algorithm="pcr2", cyclic=True)
        assert db_generator_pcr1.output_all() != db_generator_pcr2.output_all()

    def test_cyclic_sequence_starts_with_order_zeros(self):
        order = 3
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=order, cyclic=True)
        assert db_generator.output_all()[:order] == [0] * order

    def test_linear_sequence_starts_with_order_zeros(self):
        order = 3
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=order, cyclic=False)
        assert db_generator.output_all()[:order] == [0] * order

    def test_non_integer_alphabet_cyclic(self):
        alphabet = ["A", "B", "C"]
        db_generator = auxjad.DeBruijnGenerator(alphabet, order=2, cyclic=True)
        index_seq = [alphabet.index(e) for e in db_generator.output_all()]
        assert is_valid_de_bruijn_cyclic(index_seq, 2, 3)

    def test_non_integer_alphabet_linear(self):
        alphabet = ["A", "B", "C"]
        db_generator = auxjad.DeBruijnGenerator(alphabet, order=2, cyclic=False)
        index_seq = [alphabet.index(e) for e in db_generator.output_all()]
        assert is_valid_de_bruijn_linear(index_seq, 2, 3)

    def test_sequence_property_does_not_advance_generator(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        _ = db_generator.sequence
        _ = db_generator.sequence
        assert db_generator.last_selected_index_of_sequence is None

    def test_sequence_property_matches_output_all(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        seq = db_generator.sequence
        assert db_generator.output_all() == seq


class TestCall:
    def test_call_returns_elements_in_sequence_order(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        assert db_generator() == 0
        assert db_generator() == 0
        assert db_generator() == 1
        assert db_generator() == 1

    def test_call_raises_stop_iteration_when_exhausted_linear(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator.output_all()
        with pytest.raises(StopIteration):
            db_generator()

    def test_call_wraps_around_when_cyclic(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        first_run = db_generator.output_all()
        second_run = [db_generator() for _ in range(db_generator.sequence_length)]
        assert second_run == first_run

    def test_call_returns_deep_copy(self):
        db_generator = auxjad.DeBruijnGenerator([[1, 2], [3, 4]], order=2, cyclic=True)
        element = db_generator()
        element.append(99)
        db_generator.reset()
        assert 99 not in db_generator()

    def test_next_is_equivalent_to_call(self):
        db_generator1 = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator2 = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        assert next(db_generator1) == db_generator2()
        assert next(db_generator1) == db_generator2()


class TestIterator:
    def test_iter_returns_self(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        assert iter(db_generator) is db_generator

    def test_iter_for_loop_exhausts_linear_sequence(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=False)
        assert list(db_generator) == [0, 0, 1, 1, 0]

    def test_iter_cyclic_wraps_with_manual_break(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        seq_length = db_generator.sequence_length
        results = []
        for i, element in enumerate(db_generator):
            if i == seq_length * 2:
                break
            results.append(element)
        full_seq = db_generator.sequence
        assert results == full_seq * 2


class TestOutputAll:
    def test_output_all_returns_full_sequence_from_start(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        assert db_generator.output_all() == [0, 0, 1, 1]

    def test_output_all_returns_remainder_after_partial_output(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        db_generator()
        assert db_generator.output_all() == [0, 1, 1]

    def test_output_all_after_output_n_returns_remainder(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, algorithm="pcr1", cyclic=False)
        db_generator.output_n(3)
        assert db_generator.output_all() == [0, 2, 1, 1, 2, 2, 0]

    def test_output_all_raises_when_exhausted_linear(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator.output_all()
        with pytest.raises(StopIteration):
            db_generator.output_all()

    def test_output_all_cyclic_auto_resets_and_repeats(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        first = db_generator.output_all()
        second = db_generator.output_all()
        assert first == second

    def test_output_all_after_reset_gives_full_sequence(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        db_generator.output_n(3)
        db_generator.reset()
        assert db_generator.output_all() == [0, 0, 1, 0, 2, 1, 1, 2, 2, 0]

    def test_output_all_advances_index_to_end(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator.output_all()
        assert db_generator.last_selected_index_of_sequence == db_generator.sequence_length - 1


class TestOutputN:
    def test_output_n_returns_correct_elements(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        assert db_generator.output_n(2) == [0, 0]
        assert db_generator.output_n(2) == [1, 1]

    def test_output_n_negative_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(ValueError):
            db_generator.output_n(-1)

    def test_output_n_zero_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(ValueError):
            db_generator.output_n(0)

    def test_output_n_non_int_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(TypeError):
            db_generator.output_n(1.0)

    def test_output_n_raises_with_partial_count_when_exhausted(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator.output_n(3)
        with pytest.raises(StopIteration, match="2 of 5"):
            db_generator.output_n(5)

    def test_output_n_cyclic_wraps_across_boundary(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=True)
        full_seq = db_generator.sequence
        result = db_generator.output_n(db_generator.sequence_length * 2)
        assert result == full_seq * 2

    def test_output_n_then_output_all_gives_remainder(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=False)
        first_two = db_generator.output_n(2)
        rest = db_generator.output_all()
        db_generator.reset()
        assert first_two + rest == db_generator.output_all()


class TestReset:
    def test_reset_allows_full_sequence_to_be_output_again(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, algorithm="pcr1", cyclic=False)
        first_run = db_generator.output_all()
        db_generator.reset()
        assert db_generator.output_all() == first_run

    def test_reset_clears_last_selected_index(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator.output_all()
        db_generator.reset()
        assert db_generator.last_selected_index_of_sequence is None

    def test_reset_clears_previous_element(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator()
        db_generator.reset()
        assert db_generator.previous_element is None

    def test_reset_clears_previous_element_index(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=False)
        db_generator()
        db_generator.reset()
        assert db_generator.previous_element_index is None

    def test_reset_mid_sequence_restarts_from_beginning(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=False)
        db_generator.output_n(4)
        db_generator.reset()
        db_generator.output_n(4)
        assert db_generator.last_selected_index_of_sequence == 3


class TestProperties:
    def test_previous_element_is_none_before_first_call(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        assert db_generator.previous_element is None

    def test_previous_element_updated_after_call(self):
        db_generator = auxjad.DeBruijnGenerator(
            ["A", "B", "C"], order=2, algorithm="pcr1", cyclic=True
        )
        db_generator()
        assert db_generator.previous_element == "A"
        db_generator()
        assert db_generator.previous_element == "A"

    def test_previous_element_returns_deep_copy(self):
        db_generator = auxjad.DeBruijnGenerator([[1, 2], [3, 4]], order=2, cyclic=True)
        db_generator()
        retrieved = db_generator.previous_element
        retrieved.append(99)
        assert 99 not in db_generator.previous_element

    def test_previous_element_index_is_none_before_first_call(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        assert db_generator.previous_element_index is None

    def test_previous_element_index_updated_after_call(self):
        db_generator = auxjad.DeBruijnGenerator(
            ["A", "B", "C"], order=2, algorithm="pcr1", cyclic=True
        )
        db_generator()
        assert db_generator.previous_element_index == 0
        db_generator()
        assert db_generator.previous_element_index == 0

    def test_last_selected_index_is_none_before_first_call(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        assert db_generator.last_selected_index_of_sequence is None

    def test_last_selected_index_increments_with_each_call(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator()
        assert db_generator.last_selected_index_of_sequence == 0
        db_generator()
        assert db_generator.last_selected_index_of_sequence == 1

    def test_last_selected_index_resets_to_zero_on_cyclic_wraparound(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator.output_all()
        db_generator()
        assert db_generator.last_selected_index_of_sequence == 0

    def test_sequence_length_cyclic(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=3, cyclic=True)
        assert db_generator.sequence_length == 2**3

    def test_sequence_length_linear(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=3, cyclic=False)
        assert db_generator.sequence_length == 2**3 + 2

    def test_sequence_property_returns_correct_elements(self):
        db_generator = auxjad.DeBruijnGenerator(
            ["A", "B", "C"], order=2, algorithm="pcr1", cyclic=True
        )
        assert db_generator.sequence == ["A", "A", "B", "A", "C", "B", "B", "C", "C"]

    def test_repr_returns_string_of_contents(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        assert repr(db_generator) == str([0, 1, 2])

    def test_len_returns_alphabet_size(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        assert len(db_generator) == 3


class TestContentsSetter:
    def test_contents_setter_same_length_does_not_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        db_generator.contents = [10, 20, 30]
        assert db_generator.last_selected_index_of_sequence == 0

    def test_contents_setter_same_length_maps_new_values(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator.output_n(4)
        db_generator.contents = ["A", "B", "C"]
        assert db_generator.output_all() == ["C", "B", "B", "C", "C"]

    def test_contents_setter_different_length_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        db_generator.contents = [0, 1]
        assert db_generator.last_selected_index_of_sequence is None
        assert db_generator.sequence_length == 2**2

    def test_contents_setter_not_list_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(TypeError):
            db_generator.contents = (0, 1)

    def test_contents_are_copied_by_setter(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        new_contents = [10, 20, 30]
        db_generator.contents = new_contents
        new_contents.append(40)
        assert len(db_generator) == 3


class TestAlgorithmSetter:
    def test_algorithm_setter_changes_sequence(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=4, algorithm="pcr1", cyclic=True)
        seq_pcr1 = db_generator.output_all()
        db_generator.algorithm = "pcr2"
        assert db_generator.output_all() != seq_pcr1

    def test_algorithm_setter_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator()
        db_generator.algorithm = "pcr2"
        assert db_generator.last_selected_index_of_sequence is None

    def test_algorithm_setter_invalid_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(ValueError):
            db_generator.algorithm = "pcr3"

    def test_algorithm_setter_not_str_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(TypeError):
            db_generator.algorithm = 1


class TestOrderSetter:
    def test_order_getter(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2)
        assert db_generator.order == 2

    def test_order_setter_updates_sequence_length(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator.order = 3
        assert db_generator.sequence_length == 3**3

    def test_order_setter_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        db_generator.order = 3
        assert db_generator.last_selected_index_of_sequence is None

    def test_order_setter_not_int_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(TypeError):
            db_generator.order = 2.0

    def test_order_setter_zero_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(ValueError):
            db_generator.order = 0

    def test_order_setter_negative_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(ValueError):
            db_generator.order = -1


class TestCyclicSetter:
    def test_cyclic_setter_changes_sequence_length(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=3, cyclic=True)
        cyclic_len = db_generator.sequence_length
        db_generator.cyclic = False
        assert db_generator.sequence_length == cyclic_len + 2

    def test_cyclic_setter_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2, cyclic=True)
        db_generator()
        db_generator.cyclic = False
        assert db_generator.last_selected_index_of_sequence is None

    def test_cyclic_setter_not_bool_raises(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=2)
        with pytest.raises(TypeError):
            db_generator.cyclic = 1


class TestIndexingAndSlicing:
    def test_getitem_returns_correct_element(self):
        db_generator = auxjad.DeBruijnGenerator([10, 20, 30], order=2)
        assert db_generator[1] == 20

    def test_getitem_slice_returns_correct_sublist(self):
        db_generator = auxjad.DeBruijnGenerator([10, 20, 30], order=2)
        assert db_generator[0:2] == [10, 20]

    def test_setitem_updates_element(self):
        db_generator = auxjad.DeBruijnGenerator([10, 20, 30], order=2)
        db_generator[1] = 99
        assert db_generator.contents == [10, 99, 30]

    def test_setitem_same_length_does_not_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        db_generator[0] = 99
        assert db_generator.last_selected_index_of_sequence == 0

    def test_setitem_length_change_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        db_generator[1:2] = [10, 20, 30]
        assert db_generator.last_selected_index_of_sequence is None

    def test_delitem_removes_element(self):
        db_generator = auxjad.DeBruijnGenerator([10, 20, 30], order=2)
        del db_generator[2]
        assert db_generator.contents == [10, 20]

    def test_delitem_triggers_reset(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        db_generator()
        del db_generator[2]
        assert db_generator.last_selected_index_of_sequence is None
        assert len(db_generator) == 2

    def test_delitem_updates_sequence_length(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1, 2], order=2, cyclic=True)
        del db_generator[2]
        assert db_generator.sequence_length == 2**2


class TestEdgeCases:
    def test_order_1_binary_contains_both_symbols(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=1, cyclic=True)
        assert sorted(db_generator.output_all()) == [0, 1]

    def test_two_element_alphabet_order_1_linear(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=1, cyclic=False)
        assert sorted(db_generator.output_all()) == [0, 1]

    def test_large_order_sequence_length_is_correct(self):
        db_generator = auxjad.DeBruijnGenerator([0, 1], order=8, cyclic=True)
        assert db_generator.sequence_length == 2**8
