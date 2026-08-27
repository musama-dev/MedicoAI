"""Unit tests for the bag-of-words tokenization helper."""

import numpy as np

from nltk_utils import bag_of_words


def test_bag_of_words_matches_known_word():
    bag = bag_of_words(["headache"], ["headache", "fever", "cough"])
    assert bag[0] == 1.0
    assert bag[1] == 0.0


def test_bag_of_words_is_case_insensitive():
    bag = bag_of_words(["HEADACHE"], ["headache"])
    assert bag[0] == 1.0


def test_bag_of_words_shape_matches_vocabulary():
    vocab = ["a", "b", "c", "d"]
    bag = bag_of_words(["a", "b"], vocab)
    assert bag.shape == (4,)
    assert bag.dtype == np.float32


def test_bag_of_words_no_match_is_all_zeros():
    bag = bag_of_words(["zebra"], ["headache", "fever"])
    assert not bag.any()
