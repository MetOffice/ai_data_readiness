# AI Data Readiness


## **Overview**

### Checklist origin
The checklist is developed using the 2019 draft readiness matrix developed by the Office of Science and Technology Policy Subcommittee on Open Science as a basis. This checklist is developed through a collaboration of ESIP Data Readiness Cluster members include representatives from NOAA, NASA, USGS, and other organizations. 

ESIP Data Readiness Cluster (2023): Checklist to Examine AI-readiness for Open Environmental Datasets v.1.0. ESIP. Online resource. https://doi.org/10.6084/m9.figshare.19983722.v1

Readiness Matrix (2020): What is AI-Ready Open Data? NOAA. Online resource. https://www.star.nesdis.noaa.gov/star/documents/meetings/2020AI/presentations/202010/20201022_Christensen.pdf

### Prerequisits
Ideally for AI-ready assessment, a dataset should be defined as the minimum measurable bundle (i.e., a physical parameter/variable of observational datasets or model simulations). The assessment at this scale will enable better integration of data from different sources for research and development. However, it can be an intensive process for manual assessment without automation. Therefore, we recommend current assessments be done on the data file level. If the dataset has different versions, the checklist should be applied to each dataset type (e.g. raw, derived).

### Checklist sections
The checklist is broken up into 5 sections contained in 4 notebooks (part 1 & 2 are combined). 
* Part 1 - General Info
* Part 2 - Data Quality
* Part 3 - Data Documentation
* Part 4 - Data Access
* Part 5 - Data Preparation

### Checklist versions
This repository contains a checklist which will help you identify if your dataset is ready for machine learning model ingestion. There are different versions of the checklist:
* [Checklist Template Gridded Data Tutorial](https://github.com/informatics-lab/ai_data_readiness/tree/master/Checklist%20Template%20Gridded%20Data%20Tutorial) - a version of the template specifically tailored for gridded datasets.
* [Checklist Template Tabular Data Tutorial](https://github.com/informatics-lab/ai_data_readiness/tree/master/Checklist%20Template%20Tabular%20Data%20Tutorial) - a version of the template specifically tailored for tabular datasets. 
* [Checklist Template](https://github.com/informatics-lab/ai_data_readiness/tree/master/Checklist%20Template) - a generic blank version of the template



## **Setup**
### Set up your environment
#### **Clone the repository** 

#### **Create an environment** 

#### **Run the checklist**
The notebooks use Jupyter Widgets (ipywidgets) to make the data entry process more effecient by utilising drop down menus to provide suggested answers. It also enables the collation of results which are stored in a json file for potential future use and will enable you to reload your answers and also view them as a data structure object. A theme of this project was making ML processes more accessible and we wanted to explore whether building more accessible UI was beneficial. We were also motivated to store the checklist answers in a structured and accessible way to enable future work and checklist assessment comparisons. 

* To load the widgets select 'Run' from the ribbon menu and then 'Run All Cells'
* Use the save buttons to periodically save your answers in the json file.
* You can view all your results by using the button in the finished section at the end of each notebook.




