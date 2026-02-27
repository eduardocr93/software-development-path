import pytest
from Functions import sum_list, reverse, quantity_upper_lower

def test_function_sum_list_correctly():
    #Arrange
    arr = [4,6,2,29]
    expected = 41
    #act
    result = sum_list(arr)
    #assert
    assert result == expected; 

def test_function_reverse_correctly():
    #Arrange
    text= "Hello World"
    expected = "dlroW olleH"
    #act
    result = reverse(text)
    #assert
    assert result == expected;

def test_function_quantity_upper_lowe_correctly():
    #Arrange
    text= "Hello World"
    expected = [2,8]
    #act
    result = quantity_upper_lower(text)
    #assert
    assert result == expected;