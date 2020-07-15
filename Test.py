A = [3,2,2,2,3,2,4,2,3,6,2]

def ret_index(X,Y):
    for i in range(len(X)):
        if X[i] == Y:
            yield i
        else:
            continue

gen_A = ret_index(A,3)

for i in range(len(A)):
    try:
        print(next(gen_A))
    except StopIteration:
        break