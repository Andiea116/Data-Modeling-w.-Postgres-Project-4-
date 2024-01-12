# Project: Data Modeling with Postgres
By Andrea Bredesen

## Project overview:

This project is set up to assist Sparkify set up a database with 5 tables to hold data. The data is currently in a JSON format within the Data Folder at different levels.  The Data within the Song file will be used to load the Artist and Song tables. The log files will load the user and time tables.  The Songs Plays table will loaded based on a query from the Artist and Song tables with additional information, such as user ID, the user's location, session, and level of membership. This information will allow Sparkify to answer questions such as "What songs are users playing most often?", "How many songs are users playing?", and "What access level are users most commonly at?".

## File Information

`etl.ipyng`
This is the main execution file. Following through this file you'll see at a minor level the process the `etl.py` file will go through. Please note, the creation of the tables need to be completed in the following order : Time, Users, and Artists tables are created first as they do not have a foreign key relation.  Songs must be created before Songs Played table. Songs Played has foreign keys to Time, Users, Artists, and songs tables. Songs table has foreign keys to Artists table. 
        
Due to the Foreign Keys in the Songs table, the Artists table will need to be loaded first. 
        
The "ts" in log file is the timestamp in milliseconds. This is converted to datetime and extracted into hour, day, week of the year, month, year, and day of the week for loading into the Times table. 

Upon loading into the users table, there were many duplicates. Drop_Duplicates was performed prior to loading. 

The songs play table was loaded based on a query of the songs and artists tables as this data was from the Songs files. The remaining data was loaded from the log file. 

The final execution in this file is to run the etl.py script which will completely load the tables. 

`sql_queries`
Will hold the SQL verbage for the tables being created, inserted into, and dropped.  The "create_table_queries" was updated with the tables in order based on foreign key collisions. 

`create_tables.py`
Holds the function definitions that will be called in the etl.py script. 

## How to load files
1. Open `etl.ipynb`
2. You may preview the process in full by running each command OR run the first 2 commands  and last command to load tables. 
3. Opening the `test.ipynb` file, you'll be able to do a small query and a count query for each table for a general overview of the created database and tables. 






