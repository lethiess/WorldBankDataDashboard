# WorldBankDataDashboard
Simple flask app for data visualization of environment data from (World Bank)[https://www.worldbank.org/]. Via the World Bank API the app feteches the requested directly into the app.  

Currently the webapp runs only a local server.

This project is part of Udacity's Data Science Nanodegree.


## Prerequisites

To install the app, you need:
- python3
- python packages in the environment.yml or requirements.txt file
 
Using Anaconda:
```
conda env create -f environment.yml
```

Install required packages using pip:
``` 
 pip install -r requirements.txt
```


## Run the webapp

Open a terminal in the project main directory and run ```python woldbank.py ```.

After a successful server startup, open a browser and type in following address: [http://127.0.0.1:3001/](http://127.0.0.1:3001/).
