import copy

def discrete_convolution_push(matrix, neighborhood="moore", _offsets=(-1, 0, 1)):
    before = sum(sum(row) for row in matrix)
    output = copy.deepcopy(matrix)
    q = len(matrix)
    assert all(len(row) == len(matrix) for row in matrix)
    for y, row in enumerate(matrix):
        for x, k in enumerate(row):
            convolve_neighborhood(matrix, output, x, y, q, _offsets)
    after = sum(sum(row) for row in output)
    assert before == after
    return output

def convolve_neighborhood(matrix, output, x, y, q, _offsets=(-1, 0, 1)):
    for y_offset in _offsets:
        for x_offset in _offsets:
            if not (y_offset or x_offset):
                continue
            xt, yt = (x + x_offset) % q, (y + y_offset) % q
            delta = matrix[yt][xt] / 8
            output[y][x] += delta
            output[yt][xt] -= delta

def moore_neighborhood(matrix, x, y, q, _offsets=(-1, 0, 1)):
    for y_offset in _offsets:
        for x_offset in _offsets:
            #if not (y_offset or x_offset):
            #    continue
            i = (y + y_offset) % q; j = (x + x_offset) % q
            yield matrix[i][j]

def discrete_convolution_pull(matrix, neighborhood="moore", _offsets=(-1, 0, 1), n=8):
    before = sum(sum(row) for row in matrix)
    output = copy.deepcopy(matrix)
    q = len(matrix)
    assert all(len(row) == len(matrix) for row in matrix)
    for y, row in enumerate(matrix):
        for x, k in enumerate(row):
            vy = min(matrix[(y - 1) % q][x], matrix[(y + 1) % q][x])
            vx = min(matrix[y][(x - 1) % q], matrix[y][(x + 1) % q])
            vw = min(matrix[(y - 1) % q][(x - 1) % q], matrix[(y + 1) % q][(x + 1) % q])
            vz = min(matrix[(y - 1) % q][(x + 1) % q], matrix[(y + 1) % q][(x - 1) % q])

            available = 2 * sum((vy, vx, vw, vz))
            if available >= n:
                output[(y - 1) % q][x] -= vy; output[(y + 1) % q][x] -= vy
                output[y][(x - 1) % q] -= vx; output[y][(x + 1) % q] -= vx
                output[(y - 1) % q][(x - 1) % q] -= vw; output[(y + 1) % q][(x + 1) % q] -= vw
                output[(y - 1) % q][(x + 1) % q] -= vz; output[(y + 1) % q][(x - 1) % q] -= vz
                output[y][x] += available
    after = sum(sum(row) for row in output)
    assert before == after
    return output

def basic_average(matrix, _offsets=(-1, 0, 1), n=9.0):
    q = len(matrix)
    before = sum(sum(row) for row in matrix)
    output = [[0] * q for _ in range(q)]
    for y, row in enumerate(matrix):
        for x, k in enumerate(row):
            output[y][x] = (k + sum(moore_neighborhood(matrix, x, y, q, _offsets))) / n
    after = sum(sum(row) for row in output)
    print("Before: {}; After: {}".format(before, after))
    return output

def print_state(matrix):
    print '\n'.join(str(row).replace(", ", " ") for row in matrix)

def test_discrete_convolution():
    from utilities import slide
    m = [[1, 0, 0, 0, 0],
         [1, 8, 0, 0, 0],
         [0, 0, 64, 0, 0],
         [0, 0, 0, 64, 0],
         [0, 0, 0, 0, 0]]
    m = [chunk for chunk in slide(range(25), 5)]
    print_state(m)
    while True:
        m = discrete_convolution_push(m)
        #m = discrete_convolution_pull(m)
        #m = basic_average(m)
        print
        print_state(m)
        raw_input()

if __name__ == "__main__":
    test_discrete_convolution()
