import pytest
from goodcode import Dictionary


def test_node_construction_from_kwargs():
    n = Dictionary(a=1, b=2)

    assert 'a' in n and 'b' in n
    assert sorted(n.keys) == ['a', 'b']
    assert n.a == 1
    assert n.b == 2


def test_node_construction_with_sublist():
    n = Dictionary(a=[{'b': 1}, {'b': 2}])

    assert len(n.a) == 2
    assert n.a[0].b == 1
    assert n.a[1].b == 2


def test_node_construction_with_subdict():
    n = Dictionary(a={'b': 1})
    assert n.a.b == 1


