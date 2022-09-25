import numpy as np

def sorting_choice(myArray, order):
    numpy_array = np.array(myArray)
    if order == "desc":
        print(numpy_array[::-1].sort())
        return numpy_array[::-1].sort()
    else:
        print(numpy_array)
        return numpy_array.sort()

mark2 = [55, 88, 78, 90, 79, 94, 3210]
print('%d' % sorting_choice(mark2, 'desc')[0])
