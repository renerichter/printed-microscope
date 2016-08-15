# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

# for x in range(0,100000):
#     x += 1
#     print ser.readline()



buffer = []
for x in range(0, 1000):
    val = ser.readline()
    buffer.append(val.rstrip())  # stores all data received into a list
    # print(val)
    x += 1

# print buffer # prints all data ever received

for x in range(0, len(buffer)):
    try:
        buffer[x] = float(buffer[x])
    except:
        buffer[x] = float(0.00)

# Number of samplepoints
N = 1000
# sample spacing

T = 1.0 / 1000
x = np.linspace(0.0, 1000, 1)

yf = scipy.fftpack.fft(buffer)
xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)

fig, ax = plt.subplots()
ax.plot(xf, 2.0 / N * np.abs(yf[:N / 2]))
plt.show()
