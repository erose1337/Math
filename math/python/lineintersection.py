from math import sqrt, sin
from itertools import imap, izip

def test_for_intersection(a1, a2, b1, b2):
    # test if two line segments intersect
    # -----------------------------------
    #
    #     a1   b2
    #       \/
    #       /\
    #      /  \
    #    b1    a2
    if ((a1 > b1 and a2 < b2) or
        (b1 > a1 and b2 < a2)):
        return True

#def calculate_midpoint(x1, x2, y1, y2):
#    x_diff = (x1 + x2) / 2.0
#    y_diff = y1 - y2
#    sign = 1
#    if y_diff < 0:
#        sign = -1
#    line1 = pythagorean_theorem(x_diff, y_diff)
#    return (x1 + x2) / 2.0, sign * line1

def calculate_intersection(prior_x, x, a1, a2, b1, b2):
    y1 = ((a1 + b2) / 2.0)# - min(a1, b2)
    y2 = ((a2 + b1) / 2.0)# - min(a2, b1)
    #x_diff = x - prior_x
    x_out = (prior_x + x) / 2.0
    y_diff = max(y1, y2) - min(y1, y2)

    slope = pythagorean_theorem(x_out, y_diff)
    y_out = max(y1, y2) - (slope * (x_out - prior_x))
    return x_out, y_out

def pythagorean_theorem(x, y):
    return sqrt((x ** 2) + (y ** 2))

def find_intersection_points(x_labels, f_points, g_points):
    points = izip(f_points, g_points)
    prior_f, prior_g = next(points)
    prior_x = next(x_labels)

    if prior_f == prior_g:
        yield (prior_x, prior_f)

    for f_point, g_point in points:
        x = next(x_labels)
        if f_point == g_point:
            #print prior_x, x
            yield (x, f_point)
        elif test_for_intersection(prior_f, f_point, prior_g, g_point):
        #    print prior_x, x
            x_mid, y_mid = calculate_intersection(prior_x, x, prior_f, f_point,
                                                  prior_g, g_point)
            assert y_mid < max(prior_f, f_point, prior_g, g_point)# or y_mid < g_point, (y_mid, f_point, g_point)
            assert y_mid > min(prior_f, f_point, prior_g, g_point), (y_mid, prior_f, f_point, prior_g, g_point)
            assert x_mid < (x - .1) and x_mid > prior_x + .1, (x_mid, y, prior_x)
        #    assert y_mid < prior_f or y_mid < prior_g,
            yield (x_mid, y_mid)
        prior_x, prior_f, prior_g = x, f_point, g_point

def generate_samples(f, x_iter):
    return imap(f, x_iter)

def samples_to_str(samples):
    return ' '.join(str(item) for item in samples)

def samples_to_gnuplot_points(samples):
    return '\n'.join("{} {}".format(x, y) for x, y in samples)

def test_find_intersections():
    def f(x):
        return sin(x) * (pow(x, 3) - pow(x, 2))
    def g(x):
        return sin(x) * (pow(x, 3) + pow(x, 2) - x)

    #_range = lambda: [-8, -7, -6, -5] + [(1.0 / x) * -4 for x in range(1, 101)] + [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    _range = lambda: xrange(-256, 256)
    f_samples = list(generate_samples(f, _range()))
    g_samples = list(generate_samples(g, _range()))
    intersections = find_intersection_points(iter(_range()),
                                             f_samples, g_samples)
    #import pprint
    print samples_to_gnuplot_points(izip(_range(), f_samples))
    #pprint.pprint(f_samples)
    #pprint.pprint(g_samples)
    with open("f_samples.txt", 'w') as _file:
        _file.write(samples_to_gnuplot_points(izip(_range(), f_samples)))
    with open("g_samples.txt", 'w') as _file:
        _file.write(samples_to_gnuplot_points(izip(_range(), g_samples)))
    with open("intersections.txt", 'w') as _file:
        _file.write(samples_to_gnuplot_points(intersections))

if __name__ == "__main__":
    test_find_intersections()
