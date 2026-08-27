"""Unit tests for the NeuralNet model architecture."""

import torch

from nnet import NeuralNet


def test_forward_shape():
    model = NeuralNet(input_size=10, hidden_size=16, num_classes=5)
    sample = torch.zeros(1, 10)
    output = model(sample)
    assert output.shape == (1, 5)


def test_layer_sizes():
    model = NeuralNet(input_size=10, hidden_size=16, num_classes=5)
    assert model.l1.in_features == 10
    assert model.l1.out_features == 16
    assert model.l3.out_features == 5


def test_forward_produces_finite_values():
    model = NeuralNet(input_size=8, hidden_size=8, num_classes=3)
    output = model(torch.randn(2, 8))
    assert torch.isfinite(output).all()
