# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
#I rearranged the order of create tables to allow foreign keys to be created also.
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
    timestamp timestamp PRIMARY KEY, 
    hour int,
    day int,
    week_of_year int NOT NULL, 
    month int, 
    year int, 
    weekday int NOT NULL
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY,
    first_Name varchar NOT NULL, 
    last_Name varchar NOT NULL, 
    gender varchar,
    level varchar NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,
    artist_name varchar NOT NULL, 
    artist_location varchar,
    artist_latitude numeric,
    artist_longitude numeric
    );
""")

###Update Songs with FOREIGN KEYS
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY,
    title varchar NOT NULL, 
    artist_id varchar NOT NULL,
    year int,
    duration numeric NOT NULL, 
    FOREIGN KEY (artist_id)
        REFERENCES artists (artist_id)
        );
""")

###Update songplays with Foreign keys:
###    FOREIGN KEY (song_id)
###     REFERENCES songs (song_id),
### FOREIGN KEY (artist_id)
###     REFERENCES artists (artist_id)
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
    songplay_id serial PRIMARY KEY,
    timestamp timestamp NOT NULL, 
    userId int NOT NULL,  
    level varchar NOT NULL, 
    song_id varchar, 
    artist_id varchar, 
    sessionId int, 
    location varchar,
    userAgent varchar, 
    FOREIGN KEY (song_id)
        REFERENCES songs (song_id),
    FOREIGN KEY (artist_id)
        REFERENCES artists (artist_id),
    FOREIGN KEY (timestamp)
        REFERENCES time (timestamp),
    FOREIGN KEY (userId)
        REFERENCES users (user_id)
    );
""") 

### CREATE A UNIQUE INDEX FOR THE ON CONFLICT FOR 3 COLUMNS
### THIS IS LIST LAST IN THE create_table_queries LIST BELOW
songplay_table_unique_index = ("""
    CREATE UNIQUE INDEX songplay_unique_index 
    ON songplays (timestamp, userId, sessionId
    );
""") 

### ALTER TABLE WITH THE UNIQUE INDEX FOR THE ON CONFLICT FOR 3 COLUMNS
### THIS IS LIST LAST IN THE create_table_queries LIST BELOW
songplay_Altertable_unique_index = (""" 
    ALTER TABLE songplays 
    ADD CONSTRAINT unique_ids_songplay 
    UNIQUE USING INDEX songplay_unique_index;
""") 


# INSERT RECORDS
songplay_table_insert = (""" INSERT INTO songplays (timestamp, userId, level, song_id, artist_id, sessionId, location, userAgent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT ON CONSTRAINT unique_ids_songplay DO NOTHING;
""")

user_table_insert = (""" INSERT INTO users (user_id, first_Name, last_Name, gender, level) 
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (user_id)
                            DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year, duration) 
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (song_id)
                            DO NOTHING
""")

artist_table_insert = (""" INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) 
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (artist_id)
                            DO UPDATE SET artist_location = EXCLUDED.artist_location, 
                            artist_latitude = EXCLUDED.artist_latitude, 
                            artist_longitude = EXCLUDED.artist_longitude;
""")


time_table_insert = (""" INSERT INTO time (timestamp, hour, day, week_of_year, month, year, weekday) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (timestamp)
                            DO NOTHING
""")

# FIND SONGS
song_select = ("""
    SELECT song_id, songs.artist_id 
    FROM songs 
    JOIN artists ON artists.artist_id = songs.artist_id
    WHERE title = %s AND artist_name = %s AND duration = %s;
""")

# QUERY LISTS
create_table_queries = [time_table_create, user_table_create, artist_table_create, song_table_create, songplay_table_create, songplay_table_unique_index, songplay_Altertable_unique_index]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]