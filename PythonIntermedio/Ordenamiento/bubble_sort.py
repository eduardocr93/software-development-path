def bubble_sort(list_to_sort):
    for i in range (len(list_to_sort)):
        swapped = False
        for index in range(0, len(list_to_sort) - 1 - i):
            current_element = list_to_sort[index]
            next_element = list_to_sort[index + 1]
            if current_element > next_element:
                list_to_sort[index] = next_element
                list_to_sort[index + 1] = current_element
                swapped = True
        print(f"Iteración {i}: {list_to_sort}")
        if not swapped:
            break   
    print(list_to_sort)

list_test = [18, 4, 2, -11, 50, 78, 5]
bubble_sort(list_test)