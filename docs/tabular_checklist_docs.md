# Tabular Checklist Docs

## Setup
* Ensure you have set up and activated the checklist_requirements.yml environment as explained on the project readme.
* Run the notebooks locally using Jupyter Lab.
___

Here is a short video to guide you through using the tabular notebook checklist: <br>
<p align="center">
  <a href="https://youtu.be/TJd8kijuTqo">
    <img src="./images/setup_thumbnail_img.png" alt="Data Readiness Setup Video" height="250", width="auto">
  </a>
</p>

### Hidden widget code
We have used ipywidgets to create data entry fields for the checklist questions to make the process more accessible. <br>

The code to generate these is contained in the hidden cells with ... ellipses. 
<img src="images/hidden_widget_code.png" width="auto" height="65">

You can open these by clicking on the ... if you wish to review the code. To close them click the blue bar on the left. 
<img src="images/hidden_widget_code_open.png" width="auto" height="180">
___

### Save your answers.

Use the save buttons placed throuhgout the notebooks to save each section. This will save your answers to the .json file. 
<img src="images/save_button.png" width="auto" height="40">


___

### Print your results.

At the end of each notebook you will find a print json results button that will enable you to review your stored results.  
<br>
<img src="images/print_results.png" width="auto" height="400">

___



## Helper functions to support template completion. 
There are a range of functions used throughout the tabular checklist notebook to help you investigate your dataset and find the appropriate answers. 
These functions are stored in the project utils.py file.

Review the function doc strings for more information on what they do and how to use them. 


## Notebook part 1 & 2:


### Load data
We have provided a ```read_file()``` function which can load a variety of different tabular file formats into a Pandas DataFrame.
<img src="images/tabular_checklist_docs/1_load_data.png" width="auto" height="450">
___


### Expected spatial coverage
The ```check_spatial_coverage()``` function can review the expected latitude and longitude and inform you if any points in the tabular dataset are outside the bounds expected. 

<img src="images/tabular_checklist_docs/2_spatial_coverage.png" width="auto" height="350">
___

### Expected temporarl coverage
The ```check_temporal_coverage()``` function can review the expected time period and time frequency and inform you if there are missing dates. 
<img src="images/tabular_checklist_docs/3_temporal_coverage.png" width="auto" height="300">
___


### Dataset size
The ```csv_size_info()``` function demonstrates how you could investigate the size of a tabular dataset file, and its size in memory.
<img src="images/tabular_checklist_docs/4_dataset_size.png" width="auto" height="350">
___


## Notebook part 5:


### Null values
The ```null_percent()``` function presents the null values as a new DataFrame with the count and percentage. 
<img src="images/tabular_checklist_docs/5_null_values.png" width="auto" height="450">

Many datasets have missing values which been assigned an arbitary value to represent a missing value such as 99.99, 999.9, 9999.9 etc. The ```mask_values()``` function will enable you to pass an array of these values and replace them will np.nan or some other value such as 0. <br>
We can then run the ```null_percent()``` function again to review the missing values properly. 
<img src="images/tabular_checklist_docs/6_null_values.png" width="auto" height="500">

___


### Outliers
The ```.describe()``` method is very useful for gaining a general understanding of key data statistics such as the mean, min and max which might give you an initial suspicion if any values might be outliers. 
![image](images/tabular_checklist_docs/7_outliers.png)


It can be helpful to visualise your data to check for outliers. Here is an example idea using a function called ```plot_violin_samples()```
![image](images/tabular_checklist_docs/8_outliers.png)


Calculating Z-Scores can also be useful when looking for outliers.The ```print_z_scores()``` function can help you analyse the chance of containing outliers.
<img src="images/tabular_checklist_docs/9_outliers.png" width="auto" height="500">







