import math
import matplotlib.pyplot as plt


def f(x):
    return x+1


num = 5

x = [0]*num
y = [0]*num


for i in range(num):
    #tempcords = [x, f(x)]
    x.append(i)
    y.append(f(i))

plt.plot(x, y)
plt.ylabel('some numbers')
plt.show()

