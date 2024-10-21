# AI Data Readiness Checklist


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
### Clone the repository

```bash
git clone git@github.com:informatics-lab/ai_data_readiness.git 
```

### Create an environment 

Use [Conda](https://www.anaconda.com/download) to create environments for running the Jupyter Notebooks and Python scripts. All of the YAML files to create the Conda environments are stored in the env/ directory. Use the commands below to create the conda environment for the checklist notebooks.

```bash
conda env create -f env/checklist_requirements.yml
```

### Run the checklist
The notebooks use Jupyter Widgets (ipywidgets) to make the data entry process more effecient by utilising drop down menus to provide suggested answers. It also enables the collation of results which are stored in a json file for potential future use and will enable you to reload your answers and also view them as a data structure object. A theme of this project was making ML processes more accessible and we wanted to explore whether building more accessible UI was beneficial. We were also motivated to store the checklist answers in a structured and accessible way to enable future work and checklist assessment comparisons. 

* To load the widgets select 'Run' from the ribbon menu and then 'Run All Cells'
* Use the save buttons to periodically save your answers in the json file.
* You can view all your results by using the button in the finished section at the end of each notebook.

## **Examples**
We have completed the checklist with a variety of datasets to demonstrate how to use it. 
Whilst completing the questions is important, we are also using the notebooks to evidence the process used to discover the answers. Such as how to identify outliers, null values etc.
Some of the completed checklist folders include simple example machine learning (ML) projects to demonstrate how the datasets could be used. You could use these as a starting point for your own ML exploration or try and improve the example project performance. 

| Dataset | Organization | Data Summary | Machine Learning Summary | Environment Directory | 
| - | - | - | - | - |
| ERA5 | ECMWF | Global Geospatial Gridded Climate Reanalysis | Autoencoder: Compress data | env/era5_requirements.yml |
| Global Summary of the Day | NOAA | *Description* | XGBoost: Predict Class  | env/gsod_xgboost_requirements.yml |
| Global Summary of the Day | NOAA | *Description* | LSTM: *Summary* | env/gsod_lstm_requirements.yml |
| HadCRUT5 | Met Office | *Description* | XGBoost: *Summary* | env/hadcrut5_requirements.yml |
| HadCRUT5 | Met Office | *Description* | CNN: *Summary* | env/hadcrut5_requirements.yml |
| HadUK-Grid | Met Office | UK Geospatial Gridded | CNN: Forecast future values | env/haduk_grid_requirements.yml |

## **Dataset Suggestions**
Find suggested datasets here: [datasets.md](./datasets.md)
