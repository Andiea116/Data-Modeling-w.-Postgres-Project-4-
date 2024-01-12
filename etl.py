import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    THIS FUNCTION IS CALLED FROM process_data ON FIRST CALL IN MAIN:
    - The process_data passed a directory row from the array to this function
    - Function will open the directory row and create the Song Dataframe from the JSON file.
    - The Dataframe will become an array passed to the appropriate data table insert function as called within this function
    - Function definitions artist_table_insert & song_table_insert are found in the create_tables.py.
    - The functions within create_tables.py will point to sql_queries for the actual create verbaged describing column names and dTypes.
    """
    
    # open song file
    songdf = pd.read_json(filepath, lines=True)
    
    # insert artist records
    artist_data = songdf[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)
    
    # insert song records
    song_data = songdf[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """
    THIS FUNCTION IS CALLED FROM process_data ON SECOND CALL IN MAIN:
    - The process_data passed a directory row from the array to this function
    - Function will open the directory row and create the Log Dataframe from the JSON file.
    - The Dataframe will become an array passed to the appropriate data table insert function as called within this function
    - Function definitions time_table_insert & user_table_insert are found in the create_tables.py.
    - The functions within create_tables.py will point to sql_queries for the actual create verbaged describing column names and dTypes.
    - This function also calls Song_select function to query the tables created in the process_song_funciton.
    """
    # open log file
    logdf = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    logdf = logdf.query('page == "NextSong"').copy()
    logdf['timestamp'] = pd.to_datetime(logdf.ts, unit ='ms')
    
    # convert timestamp column to datetime
    t = pd.to_datetime(logdf.ts, unit ='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.dayofweek) 
    column_labels = ("timestamp", "hour", "day", "week_of_year", "month", "year", "weekday")
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data))) 

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = logdf[['userId', 'firstName', 'lastName', 'gender', 'level']] 

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in logdf.iterrows():
 
    # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.timestamp, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    THIS FUNCTION IS CALLED TWICE IN MAIN
    - The function will walk the file path from data/___ as passed from main function. 
    - It will append each file path to an array all_files.
    - After walking all file paths and appending to the array, the function will pass the array to the next function
    FIRST PASS:
    - This function passes the array to the Process Song File function.
    SECOND PASS:
    - This function passes the array to the Process Log File function.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()