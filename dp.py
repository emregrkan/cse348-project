def F(i, j):
    h1, h2 = 1, 1
    if i > 1:
        h1 = F(i-1, j)
    elif j > 1:
        h2 = F(i, j-1)
    else:
        return h1 + h2 - 1

print('a')
