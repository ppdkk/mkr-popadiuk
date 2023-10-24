import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2,3,4,5,6,7,8])
y = x
plt.figure()
plt.scatter(x,y)
plt.scatter(x[:2], y[:2], s = 70, c = 'violet', label = 'Tall')
plt.scatter(x[2:], y[2:], s = 70, c = 'yellow', label = 'Short')
plt.xlabel('number1')
plt.ylabel('number2')
plt.title('Title wow')

plt.legend(loc = 'best', frameon = True, title = 'Legend my')


lineardata = np.array([1,2,3,4,5,6,7,8])
expon = lineardata**2
#plt.figure()
plt.plot(lineardata, '-o', expon, '-o')
plt.plot([22,44,55,125], '--r')
plt.gca().fill_between(range(len(lineardata)), lineardata, expon, facecolor = 'orange', alpha = 0.15)

from matplotlib.artist import Artist

#
# def rec(art, depth=0):
#     if isinstance(art, Artist):
#         print(" " * depth + str(art))
#         for child in art.get_children():
#             rec(child, depth + 2)
#
#
# rec(f.legend())

plt.show()
