import pytest
from Functions import sum_list, reverse, quantity_upper_lower, order_alphabetic, prime_number 

def test_function_sum_list_correctly():
    #Arrange
    arr = [4,6,2,29]
    expected = 41
    #act
    result = sum_list(arr)
    #assert
    assert result == expected; 

def test_sum_list_empty_returns_zero():
    arr = []
    expected = 0
    result = sum_list(arr)
    assert result == expected

def test_sum_list_with_negatives():
    arr = [10, -3, -7, 5]
    expected = 5
    result = sum_list(arr)
    assert  result == expected

def test_function_reverse_correctly():
    #Arrange
    text= "Hello World"
    expected = "dlroW olleH"
    #act
    result = reverse(text)
    #assert
    assert result == expected;

def test_reverse_empty_string():
    text = ""
    result = reverse(text)
    assert result == ""

def test_reverse_with_spaces_and_symbols():
    text = "a b-c!"
    result = reverse(text)
    assert result == "!c-b a"

def test_function_quantity_upper_lowe_correctly():
    #Arrange
    text= "Hello World"
    expected = [2,8]
    #act
    result = quantity_upper_lower(text)
    #assert
    assert result == expected;

def test_quantity_upper_lower_all_lowercase():
    text = "python"
    expected = [0, 6]
    result = quantity_upper_lower(text)
    assert result == expected

def test_quantity_upper_lower_mixed_with_accents():
    text = "I love Nación Sushi"
    expected = [3, 13]
    result = quantity_upper_lower(text)
    assert result == expected

def test_order_alphabetic_basic():
    text = "python-variable-function"
    assert order_alphabetic(text) == "function-python-variable"

def test_order_alphabetic_already_sorted():
    text = "a-b-c"
    assert order_alphabetic(text) == "a-b-c"

def test_order_alphabetic_with_duplicates():
    text = "banana-apple-banana"
    assert order_alphabetic(text) == "apple-banana-banana"

def test_prime_number_mixed_list():
    nums = [1, 4, 6, 7, 13, 9, 67]
    assert prime_number(nums) == [7, 13, 67]

def test_prime_number_all_primes():
    nums = [2, 3, 5, 7, 11]
    assert prime_number(nums) == [2, 3, 5, 7, 11]

def test_prime_number_no_primes():
    nums = [-3, -1, 0, 1, 4, 6, 8, 9, 10]
    assert prime_number(nums) == []