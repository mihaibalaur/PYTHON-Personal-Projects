import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Data Reading
url = "https://raw.githubusercontent.com/mihaibalaur/PYTHON-Personal-Projects/main/Netflix_Data/netflix_titles.csv"
nf = pd.read_csv(url)

# nf = pd.read_csv("netflix_titles.csv")

# EDA - Exploratory Data Analysis

# 1. A quick overview of the DataSet.
nf.info()

# 2. DataSet Size - the number of columns and rows.
shape = nf.shape
print(shape)

# 3. Display Setting - in order to view all the columns.
pd.options.display.max_columns = None
print(nf.head())

# 4. Columns Display
cols = nf.columns
print(cols)

# 5. Duplicate Values
duplicates = nf.duplicated().sum()
print(duplicates)
# OUTPUT - 0
# Therefore, there are no duplicate values.

# 6. Unique Values
unique_val = nf.nunique()
print(unique_val)

# 7. Calculate the missing data from DataSet.
for column in nf.columns:
    null_values_sum = nf[column].isna().sum()
    total_no_rows = len(nf)
    null_values_rate = null_values_sum / total_no_rows * 100
    if null_values_rate > 0:
        print("""The "{:^10}" column's null rate is: {}%.""".format(column, round(null_values_rate, 2)))

# 8. Create a Copy of the DataSet
netflix = nf.copy()

# 9. Drop the N/A Values
netflix = netflix.dropna()
print(netflix.shape)

# 10. Display the last 5 rows of the DataSet
netflix.tail()
print(netflix.tail())

# 11. Display the number of elements
size = netflix.size
print(size)

# 12. Convert Date Time Format & Display the Types of Each Series
netflix["date_added"] = pd.to_datetime(netflix["date_added"])
netflix["day_added"] = (netflix["date_added"]).dt.day.astype(int)
netflix["month_added"] = (netflix["date_added"]).dt.month.astype(int)
netflix["year_added"] = (netflix["date_added"]).dt.year.astype(int)

print(netflix.dtypes)

# 13. How much memory each column uses in bytes
mem_us = netflix.memory_usage()
print(mem_us)

# 14. Data Description - Basic Statistics - only performed on numeric columns
data_description = netflix.describe().applymap(lambda x: f"{x:0.0f}")
print(data_description)

# SELECT SPECIFIC ROWS

# 1 Specific Column/Series
# The OUTPUT is a Series - 1-dimensional.
col = netflix["type"]
print(col)

# 2. Specific Columns
# The OUTPUT is a DataFrame - 2-dimensional.
cast_and_title = netflix[["cast", "title"]]
print(cast_and_title)

# 3. Display all the the Movies released in 2020.
movies_2020 = netflix[
              (netflix["release_year"] == 2020) & (netflix["type"] == "Movie")]
print(movies_2020.head())
# OUTPUT - DataFrame

# 4. Filter the DataFrame by excluding the N/A Values from 2 columns.
na_values = netflix[
            (netflix["date_added"].notna()) & (netflix["director"].notnull())]
print(na_values.head())
# OUTPUT - DataFrame

# 5. Display the first 7 rows ordered by columns in descending order.
f_7rows = nf.nlargest(7, "release_year")
print(f_7rows)
# OUTPUT - DataFrame

# SELECT SPECIFIC ROWS & COLUMNS

# 1. Display the Titles of all the TV Shows that were released in France.
titles_tv_france = netflix.loc[
                   (netflix["type"] == "TV Show") &
                   (netflix["country"] == "France"), "title"]
print(titles_tv_france.head())
# OUTPUT - Series

# 2. Display the cast of actors/actresses that appeared in productions released in 2006, 2012 and 1978.
cast = netflix.loc[
       netflix["release_year"].isin([2006, 2012, 1978]), "cast"]
print(cast.head())
# OUTPUT - Series

# 3. Display all the Directors who released only horror & thriller TV Shows.
director_horror = netflix.loc[
                  (netflix["listed_in"].str.contains("Horror", "Thriller")) &
                  (netflix["type"] == "TV Show"), "director"]
print(director_horror.head())
# OUTPUT - Series

# 4. Display the Ratings of content from Portugal or United States of America between 1989-2002.
countries = netflix.loc[
            ((netflix["country"] == "Portugal") | (netflix["country"] == "United States")) &
            ((netflix["release_year"] >= 1989) & (netflix["release_year"] <= 2002)), "rating"]
print(countries.head())
# OUTPUT - Series

# 5. Display specific rows and columns, based on their position in DataFrame.
specific = netflix.iloc[259:3897, 5:9]
print(specific)
# OUTPUT - DataFrame

# OPERATIONS

# 1. Aggregation across 2 columns.
agg = netflix.agg({"release_year": ["max", "median"],
                   "year_added": ["min", "sum"]})
print(agg)

# 2. The mean of 2 columns grouped by a 3rd one.
group_by = netflix[["release_year", "day_added", "duration"]].groupby("duration").mean().round(0)
print(group_by)

# 3. Values counting & descending order sorting.
val_c = netflix["date_added"].value_counts().sort_values(ascending=False)
print(val_c)

# 4. Sort values by alphabetical order.
abc_order = netflix.sort_values(by="description")
print(abc_order.head())

# 5. Rename the name of a Series
netflix.rename(columns={'show_id': 'content_id'},
               inplace=True)
netflix.info()

# DATA VISUALIZATION

# 1. Netflix Brand Color Pallete
sns.set_theme()
colors = ['#221f1f',
          '#b20710',
          '#e50914',
          '#3a4749',
          '#f5f5f1']
sns.palplot(colors)
plt.show(block=True)

# 2. Count of TV Shows and Movies Released By Year
netflix_release_year = netflix["release_year"].value_counts()

fig, ax = plt.subplots()
netflix_release_year.plot(kind="bar",
                          color="#e50914",
                          figsize=[15, 5],
                          title="Count of TV Shows and Movies Released By Year")
ax.grid()
plt.show(block=True)

# 3. Trends of Content produced since 1990
nf1 = netflix[['type', 'release_year']]
nf2 = nf1.groupby(['release_year', 'type']).size().reset_index(name='Total Content')
nf2 = nf2[nf2['release_year'] >= 1990]
fig = px.line(nf2,
              x="release_year",
              y="Total Content",
              color='type',
              color_discrete_sequence=["#221f1f",
                                       "#b20710"],
              title='Trends of Content produced since 1990')
fig.show()

# 4. Distribution of Content Ratings
nf1 = netflix.groupby(['rating']).size().reset_index(name='Total Counts')
fig = px.pie(nf1,
             values='Total Counts',
             names='rating',
             title='Distribution of Content Ratings',
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.show()

# 5. Top 5 Directors on Netflix

# create the DataFrame
pd.DataFrame()

# split the values from the "director" Column separated by ','
# the values must be stacked, using the stack() function
stack_dir = netflix['director'].str.split(',', expand=True).stack()
fil_dir = stack_dir.to_frame()

# rename the column "director"
fil_dir.columns = ['Director']

# using the size() function, the number of objects are counted
director = fil_dir.groupby(['Director']).size().reset_index(name='Total Content')

# order the values by Total Content in a descending order
director = director.sort_values(by=['Total Content'], ascending=False)

# display only the Top 5 Directors
dirTop5 = director.head()
dirTop5 = dirTop5.sort_values(by=['Total Content'])

fig = px.bar(dirTop5,
             x='Total Content',
             y='Director',
             title='Top 5 Directors on Netflix')
fig.show()

# 6. Top 5 Actors/Actresses on Netflix
pd.DataFrame()

stack_act = netflix['cast'].str.split(',', expand=True).stack()

fil_act = stack_act.to_frame()
fil_act.columns = ['Actors']

act = fil_act.groupby(['Actors']).size().reset_index(name='Total Content')
act = act.sort_values(by=['Total Content'], ascending=False)

actTop5 = act.head()
actTop5 = actTop5.sort_values(by=['Total Content'])

fig = px.bar(actTop5,
             x='Total Content',
             y='Actors',
             title='Top 5 Actors/Actresses on Netflix')
fig.show()

# 7. Trends of Movies added on Netflix by Month
nf1 = netflix[['type', 'month_added']]
nf2 = nf1.groupby(['month_added', 'type']).size().reset_index(name='Total Content')
nf2 = nf2[nf2["type"] == "Movie"]
fig = px.line(nf2,
              x="month_added",
              y="Total Content",
              color='type',
              color_discrete_sequence=["#221f1f",
                                       "#b20710"],
              title='Trends of Movies added on Netflix by Month')
fig.show()

# 8. Scatter Plot of Content by Genre
pd.DataFrame()
genre = netflix['listed_in'].str.split(',', expand=True).stack()
genre = genre.to_frame()
genre.columns = ['Genre']

genre_type = genre.groupby(['Genre']).size().reset_index(name='Total Content')

fig = px.scatter(genre_type,
                 x="Genre",
                 y="Total Content",
                 color='Genre',
                 color_discrete_sequence=['#221f1f',
                                          '#b20710',
                                          '#e50914',
                                          '#3a4749'],
                 title='Scatter Plot of Content by Genre')
fig.show()
