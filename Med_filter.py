# To import Libraries
import sys
import scipy
from scipy.io import wavfile
import scipy.signal
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from datetime import datetime
from playsound import playsound
import unittest
from time import sleep
from tqdm import tqdm

# To check the filter size based on whether it is even or odd and to create a pad_width array

def append_zeros(size, pad_width, degraded_data):
    
    if size % 2 != 0:

        #'np.pad' to create a pad_widthed array for the given filter size '''
        return np.pad(degraded_data, (pad_width, pad_width), 'constant', constant_values=(0, 0))

    else:
        print(" Please provide odd number for filter size ")
        sys.exit()
'''
    The input arguments are size (integer), pad_width(integer) which is number of zeros to add to the degraded data and degraded_data(array) 
    which contains degraded data value and returns a zero_pad_widthed array if the filter size is even or throws an error if size is odd

'''
# To create a function to find median

def median(pad_width_list):
   
    medianlist = []
    for i in range(len(pad_width_list) - size + 1):

        # To sort the pad_widthed_list
        sorted_list = np.sort(pad_width_list[i: i + size])

        # To find the median value in the sorted list
        median = (sorted_list[int((size)/2)])

        # To store all the median values
        medianlist.append(median)

    return medianlist
     
'''
    The input arguments are pad_widthed_list and returns the pad_widthed_list and
    returns medianlist(array) which is an array that contains the median value of the given input_list

'''

# To create a function for median filter

def my_median(data, actual_click, clicks, size):
    filtered_data = data
    for k in range(clicks):

        # To create an input list of data
        degraded_data = data[actual_click[k] -
                        pad_width: actual_click[k] + (pad_width + 1)]

        # To create an array that pads zero 
        pad_width_array = append_zeros(size, pad_width, degraded_data)

        # To create an array that gives the output of the median number across the click
        median_array = np.array(median(pad_width_array))

        # The median filtered data is applied back to the signal
        filtered_data[actual_click[k] -
                      pad_width: actual_click[k] + (pad_width + 1)] = median_array

    return filtered_data
'''
        The input arguments are data, actual clicks on data, number of clicks and filter size and
        returns the filtered_data which is restored audio signal from the clicks

'''
# To create a function to plot the data
def plot(data, sample_rate):
    
    # To calculate the length and width of the graph 
    length = data.shape[0] / sample_rate
    time = np.linspace(0., length, data.shape[0])

    # Size of the figure 
    plt.figure(figsize=(5, 5))

    # The labels and display value
    plt.plot(time, data, label="Degraded Signal")
    plt.xlabel("Time in seconds")
    plt.ylabel("Amplitude")
    return plt.show()
'''
    The input arguments are data which is an array and sample rate of the given signal and 
    returns the plotted graph of the signal using the matplotlib function.

'''
# To read sample rate and data
sample_rate, data = wavfile.read("degraded (1).wav")

# To create a copy of data files
data_copy = data
system_filtered_data = data

# To plot the input data
input_plot = plot(data, sample_rate)

# To load click point from matlab file
click_points = scipy.io.loadmat('detect.mat')

# To extract error signal key
errors = click_points['click_detection']

# To find the click
click = np.where(errors == 1)

# To find the actual click 
actual_click = click[0]

# To count the number of clicks
clicks = len(actual_click)

# Filter size and Pad width for extracting data
size = 3
pad_width = int((size - 1)/2)

# To initiate the counter
start_time = datetime.now()

# The progess bar for median filter
for s in tqdm(range(100)):
    sleep(0.01)

# To call the filter function
filtered_data = my_median(data, actual_click, clicks, size)

# To terminate the counter's count

print("FINISH")
end_time = datetime.now()
time_duration = end_time - start_time
print("The duration for the median filter is" + str(time_duration))

# To plot the restored values
output_plot = plot(filtered_data, sample_rate)

# To create and play the restored audio
write("restored.wav", sample_rate, filtered_data.astype(np.int16))

# To play the degraded signal

print("Playing the degraded audio")
playsound(r"C:\Users\sujathaa\Desktop\Shreya\degraded (1).wav")

# To play the restored signal

print("Playing the restored audio")
playsound(r"C:\Users\sujathaa\Desktop\Shreya\restored.wav")

# To read the original file
sample_rate_new, data_new = wavfile.read("clean (1).wav")

# Scaling the data
data_new=data_new/2**16
filtered_data=filtered_data/2**16

# To calculate the Mean Squared Error
mse = (np.sum((data_new-filtered_data)**2)/134)
print("The Mean square error between the restored signal and original signal is ", + mse)

class TestFilter(unittest.TestCase):
    '''
    Test_filter is defined as a subclass of unittest.TestCase
    '''

    def test_len(self):
        length1 = len(filtered_data)
        length2 = len(system_filtered_data)
        self.assertEqual(length1, length2)

# To execute the test case
if __name__ == '__main__':
    unittest.main()