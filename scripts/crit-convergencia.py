import os
import matplotlib
import matplotlib.pyplot as plt
import time
import numpy as np

os.system('./build/tp2')

f_eps = open('./results/met-pot-eps-errors.out', 'r')

x_eps = []
y_eps = []
y_eps_time = []

for line in f_eps.read().splitlines():
  splited_line = line.split(',')
  x_eps.append(splited_line[0])
  y_eps.append(splited_line[1])
  y_eps_time.append(splited_line[2])

fig, ax = plt.subplots()
ax.plot(x_eps, y_eps)

ax.set(xlabel='Epsilon vs. error absoluto', ylabel='accuaracy',
      title='Error de calculo de autovalores - variando epsilon')
ax.grid()

fig.savefig("results/epsilon_vs_error{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
plt.show()

plt.clf()

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Epsilon')
ax1.set_ylabel('Error absoluto', color=color)
ax1.plot(x_eps, y_eps, color=color)
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=90)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Tiempo de ejec.', color=color)  # we already handled the x-label with ax1
ax2.plot(x_eps, y_eps_time, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

fig.savefig("results/epsilon_vs_error_2_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
plt.show()

plt.clf()

f_eps = open('./results/met-pot-it-errors.out', 'r')

x_it = []
y_it = []
y_it_time = []

for line in f_eps.read().splitlines():
  splited_line = line.split(',')
  x_it.append(splited_line[0])
  y_it.append(splited_line[1])
  y_it_time.append(splited_line[2])

fig, ax = plt.subplots()
ax.plot(x_it, y_it)

ax.set(xlabel='Cant. iteraciones vs. error absoluto', ylabel='accuaracy',
      title='Error de calculo de autovalores - vriando cant. de iteraciones')
ax.grid()

fig.savefig("results/its_vs_error{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))
plt.show()

plt.clf()

fig, ax1 = plt.subplots()

ticks = np.arange(0, 10001, 1000)
print(ticks)

color = 'tab:red'
ax1.set_xlabel('Cant. de iteraciones')
ax1.set_ylabel('Error absoluto', color=color)
ax1.plot(x_it, y_it, color=color)
ax1.tick_params(axis='y', labelcolor=color, labelsize=4)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Tiempo de ejec.', color=color)  # we already handled the x-label with ax1
ax2.plot(x_it, y_it_time, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

fig.savefig("results/its_vs_error_2_{0}.png".format(time.strftime("%Y%m%d-%H%M%S")))

plt.show()

plt.clf()
