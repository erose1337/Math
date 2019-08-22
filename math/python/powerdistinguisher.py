from math import factorial

def compute_differences(numbers):
    output = []
    for index in range(len(numbers) - 1):
        output.append((numbers[index + 1] - numbers[index]) % 257)
    if any(output) == False:
        raise ValueError("No differences left")
    return output

def test_distinguisher(maximum=257):
    inputs = range(1, maximum)

    for power in range(2, maximum - 1):
        outputs = [pow(inputs[index], power, 257) for index in range(len(inputs))]
        differences = compute_differences(outputs)
        order = 1
        distinguisher = factorial(power) % 257
        while not all(difference == distinguisher for difference in differences):
            differences = compute_differences(differences)
            order += 1            
        assert differences, (power, order)
        assert order == power, (order, power)
        assert differences[0] == distinguisher

if __name__ == "__main__":
    test_distinguisher(257)
