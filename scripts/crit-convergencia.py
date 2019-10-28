import os
import matplotlib
import matplotlib.pyplot as plt
import time

os.system('./build/tp2')

f_eps = open('./results/met-pot-eps-errors.out', 'r')

x_eps = []
y_eps = []

for line in f_eps.read().splitlines():
  splited_line = line.split(',')
  x_eps.append(splited_line[0])
  y_eps.append(splited_line[1])

fig, ax = plt.subplots()
ax.plot(x_eps, y_eps)

ax.set(xlabel='Epsilon vs. error absoluto', ylabel='accuaracy',
      title='Error de calculo de autovalores - variando epsilon')
ax.grid()

fig.savefig("results/epsilon_vs_error{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
plt.show()

plt.clf()

f_eps = open('./results/met-pot-it-errors.out', 'r')

x_it = []
y_it = []

for line in f_eps.read().splitlines():
  splited_line = line.split(',')
  x_it.append(splited_line[0])
  y_it.append(splited_line[1])

fig, ax = plt.subplots()
ax.plot(x_it, y_it)

ax.set(xlabel='Cant. iteraciones vs. error absoluto', ylabel='accuaracy',
      title='Error de calculo de autovalores - vriando cant. de iteraciones')
ax.grid()

fig.savefig("results/its_vs_error{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
plt.show()
