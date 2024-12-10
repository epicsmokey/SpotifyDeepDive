import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import os

#--- SETUP --- #
#Enter the years you want to include in the visuals. Only include years that exist in your data.
desired_years = [2022,2023,2024]
os.listdir()
folder_path = 'audio_json_files'

# Get a list of all JSON files in the folder
filenames = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]

# get info from files
data = []
for filename in filenames:
    with open(filename, encoding="utf8") as f:
        data.append(json.load(f))

# Convert to DataFrames and combine
data = [pd.DataFrame(pd.json_normalize(datum)) for datum in data]
df = pd.concat(data)

# Convert 'ts' column to datetime
df['ts'] = pd.to_datetime(df['ts'])

# Extract the year
df['year'] = df['ts'].dt.year

# Debugging step: Check unique years
print("Unique years in dataset:", df['year'].unique())


# desired_years = [2016,2017,2018,2019,2020,2021,2022,2023,2024]
# Filter for the years only
filtered_df = df[df['year'].isin(desired_years)]

# Verify filtered data
print("Unique years after filtering:", filtered_df['year'].unique())

df = filtered_df

# get rid of duplicates or NaN entries
df.drop_duplicates(inplace=True)
df.dropna(inplace=True, subset=["master_metadata_album_artist_name", "master_metadata_track_name", "spotify_track_uri"])

uniques = df[["master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name"]].nunique()
print("Unique Songs: " + str(uniques["master_metadata_track_name"]))
print("Unique Artists: " + str(uniques["master_metadata_album_artist_name"]))
print("Unique Albums: " + str(uniques["master_metadata_album_album_name"]))
print("Average Songs/Artist: " + str(uniques["master_metadata_track_name"]/uniques["master_metadata_album_artist_name"])[0:5])
total_songs_played = len(df)
print(f"Total number of songs played overall: {total_songs_played}")


#--- TOP ARTISTS BY PLAYCOUNT --- #

number_artists = 25
top_artists = df.value_counts(subset="master_metadata_album_artist_name").head(number_artists)
plt.figure().set_figheight(number_artists/4)
plt.barh(top_artists.index, top_artists, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Artists")
plt.xlabel("Songs Listened")
plt.margins(0.05, 0.005)
plt.show()


#--- TOP ARTISTS BY TIME --- #

# Calculate total minutes played for each artist
artist_minutes = df.groupby("master_metadata_album_artist_name")["ms_played"].sum() / (1000 * 3600)

# Sort by minutes played in descending order and select the top 25
top_artists_by_minutes = artist_minutes.sort_values(ascending=False).head(25)

plt.figure().set_figheight(number_artists/4)
plt.barh(top_artists.index, top_artists_by_minutes, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Artists")
plt.xlabel("Hours Listened")
plt.margins(0.05, 0.005)
plt.show()

#--- TOP SONGS BY PLAYCOUNT --- #

number_songs = 25
top_songs = df.value_counts(subset="master_metadata_track_name").head(number_songs)
plt.figure().set_figheight(number_songs/4)
plt.barh(top_songs.index, top_songs, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Songs")
plt.xlabel("Times Listened")
plt.margins(0.05, 0.005)
plt.show()


#--- TOP SONGS BY TIME --- #

# Calculate total minutes played for each song
song_minutes = df.groupby("master_metadata_track_name")["ms_played"].sum() / (1000 * 3600)

# Sort by minutes played in descending order and select the top 25
top_songs_by_minutes = artist_minutes.sort_values(ascending=False).head(25)

plt.figure().set_figheight(number_songs/4)
plt.barh(top_songs.index, top_songs_by_minutes, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Songs")
plt.xlabel("Hours Listened")
plt.margins(0.05, 0.005)
plt.show()

#--- TOP ALBUMS --- #
number_albums = 25
top_albums = df.value_counts(subset="master_metadata_album_album_name").head(number_albums)
plt.figure().set_figheight(number_albums/4)
plt.barh(top_albums.index, top_albums, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Albums")
plt.xlabel("Tracks Listened")
plt.margins(0.05, 0.005)
plt.show()

top_albums_minutes = [df[df["master_metadata_album_album_name"]==album]["ms_played"].sum()/(1000*3600) for album in top_albums.index]

df.value_counts(subset="master_metadata_album_album_name").head(number_albums)
plt.figure().set_figheight(number_albums/4)
plt.barh(top_albums.index, top_albums_minutes, align='center', height=.8)
plt.gca().invert_yaxis()
plt.title("Top Albums")
plt.xlabel("Hours Listened")
plt.margins(0.05, 0.005)
plt.show()

#time trends
# All time

data_start = df.index.min()  # df_of_interest.index.min()
data_end = df.index.max()  # df_of_interest.index.max()
try:
    months = pd.date_range(data_start, data_end, freq='MS').strftime("%Y-%m").tolist()
    monthly_minutes = []
    for month in months:
        try:
            monthly_minutes.append(df.filter(like=month, axis=0)["ms_played"].sum() / (60 * 1000))
            # sum of minutes
        except:
            print("eyipes")

    months = pd.date_range(data_start, data_end, freq='MS').strftime("%b-%y").tolist()

    # add up total time that artist/whatever each month
    # plot month vs amount listened

    plt.figure().set_figheight(5)
    plt.figure().set_figwidth(len(months))
    plt.plot(months, monthly_minutes)
    plt.title(f"Time listened over time")
    plt.xlabel("Minutes listened per month")
    plt.margins(.5 / len(months), 0.05)
    plt.show()
except:
    print("something went horribly wrong send help")

#--- SPECIFIC DRILL DOWN FROM TOMMY ---#

# take top five songs, artists, albums
# then allow prompt of any song or artist or album
# procedure same for all

# def across_time(record_type, name):
#     if record_type == "song":
#         col_name = "master_metadata_track_name"
#     elif record_type == "artist":
#         col_name = "master_metadata_album_artist_name"
#     elif record_type == "album":
#         col_name = "master_metadata_album_album_name"
#     else:
#         raise Exception("Enter 'song', 'artist', or 'album'")
#
#     df_of_interest = df[df[col_name] == name]
#
#     data_start = df.index.min()  # df_of_interest.index.min()
#     data_end = df.index.max()  # df_of_interest.index.max()
#
#     try:
#         months = pd.date_range(data_start, data_end, freq='MS').strftime("%Y-%m").tolist()
#         monthly_minutes = []
#         for month in months:
#             try:
#                 monthly_minutes.append(df_of_interest[
#                                            (df_of_interest[col_name] == name)
#                                        ].filter(like=month, axis=0)["ms_played"].sum() / (60 * 1000))
#                 # sum of minutes where name is name
#             except:
#                 print("eyipes")
#
#         months = pd.date_range(data_start, data_end, freq='MS').strftime("%b-%y").tolist()
#
#         # add up total time that artist/whatever each month
#         # plot month vs amount listened
#
#         plt.figure().set_figheight(5)
#         plt.figure().set_figwidth(len(months))
#         plt.plot(months, monthly_minutes)
#         plt.title(f"Time listened to {str(record_type)} {str(name)} over time")
#         plt.xlabel("Minutes listened per month")
#         plt.margins(.5 / len(months), 0.05)
#         plt.show()
#     except:
#         print(f"{name} not found, verify artist/song/album name")
#
# #across time with items
# across_time("artist", "Caamp")
# across_time("album", "Caamp")
# across_time("album", "By and By")


#--- MOST SKIPPED SONGS --- #

# Filter data for skips within the first 10 seconds
#If you want a different length than 10 seconds, change the 10000ms value below
df_skipped = df[(df['ms_played'] <= 10000) & (df['skipped'] == True)]

# Count skips per song
top_skipped_songs = df_skipped['master_metadata_track_name'].value_counts().head(25)
total_skipped = len(df_skipped)
ratio_skipped = round((total_skipped/total_songs_played),2)
print(f"Total skipped songs within the first 10 seconds: {total_skipped}, or {ratio_skipped}%")

# Create bar chart
plt.figure(figsize=(10, 8))
plt.barh(top_skipped_songs.index, top_skipped_songs.values, align='center', height=0.8)
plt.gca().invert_yaxis()
plt.title("Top 25 Songs Skipped Within First 10 Seconds")
plt.xlabel("Number of Skips")
plt.ylabel("Song Title")
plt.tight_layout()
plt.show()


#--- SHUFFLE VS. NON-SHUFFLE SONGS --- #
shuffle_counts = df.groupby('shuffle').size()
played_on_shuffle = shuffle_counts.get(True, 0)
played_not_on_shuffle = shuffle_counts.get(False, 0)

print(f"Number of songs played on shuffle: {played_on_shuffle}")
print(f"Number of songs played not on shuffle: {played_not_on_shuffle}")

# visualize shuffle vs non-shuffle plays
plt.figure(figsize=(6, 6))
labels = ['On Shuffle', 'Not on Shuffle']
sizes = [played_on_shuffle, played_not_on_shuffle]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Proportion of Songs Played on Shuffle vs Not on Shuffle")
plt.show()


#--- FREQUENCY PLAYED AT EACH HOUR OF DAY --- #

# Change convert timezone if not Chicago
df['ts'] = df['ts'].dt.tz_convert('America/Chicago')
# Extract hour from timestamp
df['hour'] = df['ts'].dt.hour

# Calculate total minutes listened per hour
hourly_minutes = df.groupby('hour')['ms_played'].sum() / (1000 * 60)

# Visualize
plt.figure(figsize=(10, 6))
plt.bar(hourly_minutes.index, hourly_minutes.values, color='skyblue')
plt.title("Listening Trends by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Minutes Listened")
plt.xticks(range(0, 24))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


#--- SONG FREQUENCY BY SEASON --- #
df['month'] = df['ts'].dt.month
df['season'] = pd.cut(
    df['month'],
    bins=[0, 2, 5, 8, 11, 12],  # Define month ranges for seasons
    labels=['Winter', 'Spring', 'Summer', 'Fall', 'Late Winter'],  # Ensure unique labels
    right=False
)

# Aggregate minutes by season
seasonal_minutes = df.groupby('season')['ms_played'].sum() / (1000 * 60)

# Visualize
plt.figure(figsize=(8, 6))
seasonal_minutes.plot(kind='bar', color='orange', alpha=0.8)
plt.title("Listening Trends by Season")
plt.xlabel("Season")
plt.ylabel("Minutes Listened")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


#--- VISUAL OF TOP ARTISTS EACH YEAR WITH OVERLAP --- #
#this prints the max for each year
# Group by year and artist, calculate total minutes played
yearly_artists = df.groupby(['year', 'master_metadata_album_artist_name'])['ms_played'].sum().reset_index()
yearly_artists['hours_played'] = yearly_artists['ms_played'] / (1000 * 3600)

# Get top artist for each year
top_artists_per_year = yearly_artists.loc[yearly_artists.groupby('year')['ms_played'].idxmax()]
print(top_artists_per_year[['year', 'master_metadata_album_artist_name', 'hours_played']])

# Visualize
plt.figure(figsize=(10, 6))
for year, group in yearly_artists.groupby('year'):
    top_10 = group.sort_values('hours_played', ascending=False).head(10)
    plt.barh(top_10['master_metadata_album_artist_name'], top_10['hours_played'], label=str(year), alpha=0.6)

plt.title("Top Artists by Year")
plt.xlabel("Hours Played")
plt.legend(title="Year")
plt.tight_layout()
plt.show()


#--- TOTAL HOURS LISTENED EACH YEAR --- #

yearly_hours = df.groupby('year')['ms_played'].sum() / (1000 * 3600)

# Visualize
plt.figure(figsize=(10, 6))
plt.plot(yearly_hours.index, yearly_hours.values, marker='o', color='teal')
plt.title("Total Hours Listened by Year")
plt.xlabel("Year")
plt.ylabel("Hours Listened")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


#--- FREQUENCY PLAYED ON A GIVEN DAY --- #

# Extract day of the week
df['day_of_week'] = df['ts'].dt.day_name()

# Group by day and calculate total hours listened
day_hours = df.groupby('day_of_week')['ms_played'].sum() / (1000 * 3600)

# Sort days in the correct order
day_hours = day_hours.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Visualize
plt.figure(figsize=(10, 6))
plt.bar(day_hours.index, day_hours.values, color='orange')
plt.title("Listening Trends by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Hours Listened")
plt.show()





#--- THE FOLLOWING ARE PRINT OUTPUTS YOU WILL SEE IN CONSOLE, NOT A VISUAL --- #

#--- SONGS LISTENED TO MORE THAN 25 TIMES IN A WEEK --- #
#this may get long, it's an ugly printout
# Extract week number
df['week'] = df['ts'].dt.isocalendar().week
# Group by song and week
replays = df.groupby(['master_metadata_track_name', 'week']).size().reset_index(name='play_count')
# Filter songs replayed more than 5 times in a week
replayed_songs = replays[replays['play_count'] > 25]
print("Songs replayed more than 25 times in a week:")
print(replayed_songs)


#--- TOTAL HOURS LISTENED ACROSS ALL SONGS IN YEARS SELECTED --- #

# Calculate total hours listened
total_hours_listened = df['ms_played'].sum() / (1000 * 3600)
# Print the result
print(f"Total hours spent listening to music: {total_hours_listened:.2f}")


#--- LONGEST CONTINOUS LISTENING STREAK --- #

# Sort data by timestamp
df = df.sort_values('ts')
# Calculate time gaps between consecutive rows
df['time_gap'] = df['ts'].diff().dt.total_seconds()
# Identify continuous listening streaks (e.g., <10 minutes gap)
df['is_streak'] = df['time_gap'] < 600  # 600 seconds = 10 minutes
# Calculate streak durations
streaks = df.groupby((df['is_streak'] == False).cumsum())['ms_played'].sum() / (1000 * 3600)
# Find the longest streak
longest_streak = streaks.max()
print(f"Longest listening streak: {longest_streak:.2f} hours")


#--- AVERAGE PLAYTIME FOR SONGS ON SHUFFLE VS NON-SHUFFLE --- #
# Calculate average playtime for shuffle and non-shuffle
shuffle_avg = df[df['shuffle'] == True]['ms_played'].mean() / (1000 * 60)
non_shuffle_avg = df[df['shuffle'] == False]['ms_played'].mean() / (1000 * 60)

print(f"Average playtime on shuffle: {shuffle_avg:.2f} minutes")
print(f"Average playtime not on shuffle: {non_shuffle_avg:.2f} minutes")