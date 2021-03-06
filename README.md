# Project 1 Python team_26

Created by `Arathi Biju` and `Dexter Pham`

---
## Introduction
This Git repo describes how we setup and run the `Handwritten Digit Recogniser` software using `Visual Studio Code` and `Miniconda3` packet and environment manager to set up a separate environment to run our software without interfering your usual version of Python in your normal environment.

For this project, we are using `Visual Studio Code`, `Python 3.8`, `Miniconda3 for Python 3.8` and the following libraries:
`PyQt5 torch torchvision numpy matplotlib opencv-python`

If you're familiar with all of this, just make sure you have all the required libraries then go straight to the `Running the project` section
  

## Navigation


## Installation Guide
**1. Install VSCode**

https://code.visualstudio.com/
  
**2. Install Python Extension for Visual Studio Code**

**3. Install Miniconda3 for Python 3.8**

https://docs.conda.io/en/latest/miniconda.html

**4. Set up conda environment**

 >  Open Anaconda Prompt (miniconda3)
 
 >  Check if conda env is available
 
  `conda env list`
  
  ---
 
 > We can start making a new environment if conda is available
 
 `conda create -n <name of your environment> python=3.8`
 
 For example: `conda create -n py302_project python=3.8`
 
 > Type [y] when prompted:
 
 ---
 
 > Activate your conda environment
 
 `conda activate <name of your environment>`
 
 For example:  `conda activate py302_project`
 
 > List all the package we are currently have
 
 `pip list`
 
 
 **5. Install the necessary libraries for this project**
 
  If you don't have a CUDA-Enabled GPU (Nvidia Graphics Card), then run this command:
 
 `pip install PyQt5 torch torchvision numpy matplotlib opencv-python`
 
 If you have a CUDA-Enabled GPU and want to use it
 > If you have a GTX graphics card: Then CUDA 10.2 is likely the best version for you 

```bash
 pip install PyQt5 numpy matplotlib opencv-python
 pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

 > If you have a RTX graphics card: Then CUDA 11.1 is the best version for you 

```bash
 pip install PyQt5 numpy matplotlib opencv-python
 pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```

 > If you have a Quadro graphics card, then try to find out if your card does have TPU or not, if it does then RTX guide above, else GTX.


## Running the project
 
 1. Clone the Github repo to your computer.
 
 2. Using VSCode to open the folder
 
 3. Run main.py or Controller.py
 
 4. Navigate to the train window, via the file menu.
 
 5. Download the MNIST dataset. 
 
 6. Select the type of DNN you wish to use for digit recognition then train (please allow a few minutes for training depending on your system).
 
 7. Load the trained model.
 
 8. Return to the main window. Use the mouse or a stylus to draw any digit on the canvas. Select clear if you wish to redraw.

 9. Click recognize to begin analysis. The graph and the underlying text will update to classify the digit.
 
 10. To change models at any time, open the train window and repeat steps 6 & 7.
 
 11. To view the training and testing images used by the model navigate to the View Model Images window, which displays the training and testing images.
 
 
 ...

### Acknowledgements 
The teaching staff of COMPSYS302 at the University of Auckland, in particular:
- Dr Ho Seok AHN
- Mr Jong Yoon Lim
- Ms Yuanyuan Hu

