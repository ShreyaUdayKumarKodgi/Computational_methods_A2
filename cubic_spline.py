# To Import libraries
from sklearn.metrics import mean_squared_error
from scipy.io import wavfile
import scipy.io
from scipy.io.wavfile import write
from scipy.interpolate import CubicSpline
import numpy as np
from time import sleep
from tqdm import tqdm
from playsound import playsound
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from datetime import datetime

def plot(data, samplerate):
    
    '''
     The input arguments are data (array) which has the audio data and sample rate of the given signal and returns the plotted graph of the audio signal.

    '''
    # To calculate the length and width of the plot
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])

    # The size of the figure
    plt.figure(figsize=(10, 5))

    # The labels and display value
    plt.plot(time, data, label="Degraded Signal")
    plt.xlabel("Time in seconds")
    plt.ylabel("Amplitude")
    return plt.show()


# To read the clean and degraded signals
samplerate_new, data_new = wavfile.read(r"C:\Users\sujathaa\Desktop\Shreya\clean (1).wav")
samplerate_deg, data_deg = wavfile.read(r"C:\Users\sujathaa\Desktop\Shreya\degraded (1).wav")

# To plot the input data
inp_waveform = plot(data_deg, samplerate_deg)

# To load click point from matlab file
click_point = scipy.io.loadmat('detect.mat')

# To extract error signal key
errors = click_point['click_detection']

# To search the click
click = np.where(errors == 1)

# To find the actual click
actual_click = click[0]

# The number of clicks
click_num = len(actual_click)

# Assigning index for the degraded signal
index_deg = np.arange(len(data_deg))

# To delete the clicks from the degraded data array
y = np.delete(data_deg, actual_click)

# To create index without clicks
x = np.delete(index_deg, actual_click)

# To initiate the counter
start_time = datetime.now()

# To copy the degraded data
cubic_splined_data = data_deg

# The progess bar for median filter
for z in tqdm(range(10)):
    # Applying the cubic spline function
    cs = CubicSpline(x, y, bc_type='natural')

# To train the clicked data with prediction of cubic_splined data
for i in range(click_num):
    cubic_splined_data[actual_click[i]] = cs(actual_click)[i]

# To terminate the counter's count
end_time = datetime.now()
durationTime = end_time - start_time
print('Done')
print("The duration for the cubic spline filter is " + str(durationTime))

# To plot the cubic spline data
cs_data = plot(cubic_splined_data, samplerate_new)

# To create and play the restored audio
write("rest_c.wav", samplerate_deg, cubic_splined_data.astype(np.int16))


# To calculate the Mean square error
data_new=data_new/2**16
cubic_splined_data=cubic_splined_data/2**16
mse = (np.square(np.subtract(cubic_splined_data, data_new)).mean())
print("The Mean square error is ", + mse)

# To play the degraded signal

print("Playing the degraded audio")
playsound("degraded (1).wav")

# To play the restored signal

print("Playing the restored audio from cubic spline")
playsound(r"C:\Users\sujathaa\Desktop\Shreya\restored.wav")