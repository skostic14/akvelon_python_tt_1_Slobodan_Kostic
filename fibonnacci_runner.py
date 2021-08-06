from utils import fibonacci

correct_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

for i in range(len(correct_sequence)):
    print('Running fibonacci(%d) - expected result: %d' % (i, correct_sequence[i]))
    print('Result: %d' % fibonacci(i))

print('Running Fibonacci for char A')
try:
    fibonacci('A')
except TypeError as te:
    print('Caught error: %s' % te)