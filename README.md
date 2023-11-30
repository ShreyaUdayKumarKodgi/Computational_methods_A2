# COMPUTATIONAL METHODS ASSIGNMENT - 2
# Audio Restoration using Median Filter and Cubic Spline method

## High-level Description of the project
This assignment builds on Assignment I. We assume that we have successfully detected the clicks and we are applying different interpolation methods to restore the audio, such as
- Median Filter - Med_filter.py
- Cubic Spline - cubic_spline.py

1. Median Filter - This is a method of interpolating where it replaces the original value with the median value of neighboring points for the chosen kernel size.
2. Cubic Spline - This is a method for constructing a smooth curve that passes through a set of given discrete data points.
---

## Installation and Execution

The first step is to create an environment.
```
pip install -r requirements.txt 
```
After creating an environment, we install the following libraries
```
numpy==1.26.2 
scikit_learn==1.3.2
matplotlib==3.8.2
tqdm==4.66.1
scipy==1.11.4
datetime==5.3 
playsound==1.3.0                             
```
After installation, the files are run by 
```
python Med_filter.py
python cubic_spline.py
```
For more details check [here](https://github.com/bndr/pipreqs)

---

## Methodology and Results
The main script of the file calls different functions - `append_zeros`, `my_median`, `median`, `plot`, and a unittest main function `TestFilter`. 

The overall methodology involves -

1. Importing the libraries
2. Loading audio data
3. Detecting clicks
4. Applying a median filter around the detected clicks
5. Visualizing the signals
6. Playing the audio
7. Evaluating the performance using MSE
8. Ensuring the correctness of the filtering process using Unit-Test.




**Results**

1. For the median filter, different lengths of filter were explored to test the effectiveness of the restoration. In particular, Six were tested and size = 3 was observed to deliver the lowest MSE, as shown in the figure below.

<img src="Figure_1.png" width="550">

The restored waveform <output_medianFilter.wav> with the optimal filter length is given below:

<img src="two.png" width="750">


2. Using the cubic splines, we observe that there are no clicks in the audio signal.

The restored waveform <output_cubicSplines.wav> with the optimal filter length is given below:
<img src="spline2.png" width="750">

3. Comparing the two different interpolation methods, we notice that cubic spline achieves a lower MSE. The runtime of cubic spline is 0.089005 seconds and the runtime of median filter is 1.117534 seconds. 

After listening to the two restored files, we notice that the degraded signal is restored without any clicks using two interpolating methods.


---
## Credits

This code was developed for purely academic purposes by Shreya Uday Kumar Kodgi as part of the Computational Methods module Assignment.

Resources:
- [Cubic Spline](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html)
- [Unit-Test](https://realpython.com/python-testing/)





