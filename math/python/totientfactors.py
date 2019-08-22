def test_period():
    n = 60
    for b in range(4, n):
        for x in range(2, n):
            outputs = [b]
            break_flag = False
            t = b
            while True:
                t = (t * x) % n
                if t in outputs:
                    break
                if t == 0:
                    print t, b, x, len(outputs)
                    break_flag = True
                    break
                outputs.append(t)
            #if break_flag:
            #    break

if __name__ == "__main__":
    test_period()
