# Dash_LA_CRIME
Data visualization - data cleaning - preprocessing - dashboard via Plotly's dash

Analysis about LA's crime per area, hour, time, day, month etc... from 2020 until today,

We are updating the file via the preprocess.py file where we dl the updated file from data.lacity.org:

data description & file link can be found at :https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8

Find my preprocess.py file with the data cleaning, reformatting and analysis of what to keep, add or remove from the dataset.

The app.py file is about the set up of the dash web app and the interactive callbacks to analyze by year/month/ hours & area.

I put a range slider regarding time to choose , a multi-option dropdown to select area.

I oonly used plotly.express to draw graphs.

FYI : App can be find @ http://riss.pythonanywhere.com/

Due to conditions of free tier deployment with pythonanywhere, 

I had to make some change regarding the size of the dataset (100000 lines only i.o more than 600000),

I didn't put in my program the code to deploy the app, I just follow their tutorial and adapt my code to it.



      __ assets -->typography.css

      __ app.py
      
      __ dashapp.py
      
      __ preprocess.py



