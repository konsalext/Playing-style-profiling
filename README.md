_Hello_ ,
in this repo i created a streamlit app for **profiling the playing style** of soccer teams competing in the **Greek
Superleague** the last 6 seasons.
The steps i took were :
- Collect the data (via Wyscout) ,
- Pull the data out of my database **in MySql** ,
- Did a bit of **wrangling** in MySql - created three additional metrics called Directness, % long pass share and final third entries ,
- Finally wrote the script code in Python.
All the values were adjusted per 90 and then transformed to **percentile scores** , a score 0-100 in each metric when compared to all the
teams that competed in the Greek Superleague the last 6 years.
The repo contains four files : an .xlsx file with the data (**all_seasons**) , the app script (**Style_app.py**) ,
the requirements file with the packages that are needed , and the **my_sql_script** file with the SQL code.

[Click here to see the app](https://konsalext-playing-style-profiling-style-app-yr5u7z.streamlit.app/)

_Hope you like it !_
