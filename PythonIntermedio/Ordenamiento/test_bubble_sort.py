import pytest
from bubble_sort import bubble_sort

def test_bubble_sort_with_small_list():
    #Arrange
    arr = [12,14,16,-10]
    #act
    bubble_sort(arr)
    #assert
    assert arr == [-10, 12, 14, 16]

def test_bubble_sort_with_large_list():
    # Arrange
    arr = list(range(150, 0, -1))
    expected = list(range(1, 151))

    # Act
    bubble_sort(arr)

    # Assert
    assert arr == expected


def test_bubble_sort_with_empty_list():
    #Arrange
    arr = []
    #act
    bubble_sort(arr)
    #assert
    assert arr == []

def test_bubble_sort_raises_error_if_not_list():
    with pytest.raises(TypeError):
        bubble_sort(123)

    with pytest.raises(TypeError):
        bubble_sort(None)