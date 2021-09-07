

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler


analytics_march = pd.read_csv("daily_tweet_activity_metrics_ADHOrg_20210301_20210401_en.csv")
analytics_april = pd.read_csv("daily_tweet_activity_metrics_ADHOrg_20210401_20210501_en.csv")
analytics_may = pd.read_csv("daily_tweet_activity_metrics_ADHOrg_20210501_20210601_en.csv")
analytics_june = pd.read_csv("daily_tweet_activity_metrics_ADHOrg_20210601_20210701_en.csv")
analytics_july = pd.read_csv("daily_tweet_activity_metrics_ADHOrg_20210701_20210731_en.csv")

frames = [analytics_march, analytics_april, analytics_may, analytics_june, analytics_july]
analytics_total = pd.concat(frames)
#print(analytics_total.head())
df_new = analytics_total[['Date','impressions','engagements','engagement rate','retweets','replies','likes', 'user profile clicks', 'url clicks', 'hashtag clicks', 'detail expands', 'permalink clicks']]
#check for nans
df_new = df_new.replace('-',np.nan)
df_new.isna().sum()



#add weekday column
df_new['Date'] = pd.to_datetime(df_new['Date'], format='%Y-%m-%d')
df_new['day'] = df_new['Date'].dt.weekday
df_new['day_name'] = df_new['Date'].dt.day_name()
#print(df_new.head(2))
df_new = df_new.rename(columns = {
                                  'user profile clicks':'profile_clicks', 'url clicks':'url_clicks', 'engagement rate':'engagement_rate',
                                  'hashtag clicks':'hashtag_clicks', 'detail expands':'detail_expands',
                                  'permalink clicks':'permalink_clicks',
                                  'Date':'date'
                                })
#check
df_new.columns

#create a column with # & mention count
def hm_count(row, h_or_m):
    c = row.count(h_or_m)
    return c



tweets_sorted = df_new['date'].sort_values(ascending=True)

earliest_tweet = tweets_sorted.head(1).iloc[0].strftime("%Y-%m-%d")
latest_tweet = tweets_sorted.tail(1).iloc[0].strftime("%Y-%m-%d")
#calculate averages
print(df_new.describe().loc['mean'])


print(df_new.describe().loc['min']['impressions'])
print(df_new.describe().loc['max']['impressions'])

print(f'''Basic stats about the dataset:
\nThe full dataset includes all tweets between {earliest_tweet} , and, {latest_tweet}.
\nThere are {len(df_new)} tweets in the dataset.
''')
#df_new.to_csv('engagement.csv')
#engagement rate column
fig = plt.figure(figsize=(8,10))
df_new['engagement_rate'].plot.box()
df_new['engagement_rate'].describe()
m = max(df_new['engagement_rate'])
def ecdf(data):

    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y
#plot ecdf
#empirical data
x,y = ecdf(df_new['engagement_rate'])

mean = df_new['engagement_rate'].mean()
std = df_new['engagement_rate'].std()
samples = np.random.normal(mean, std, 1000)

#theoretical data
x_theor, y_theor = ecdf(samples)

plt.figure(figsize=(10,6))
plt.plot(x_theor, y_theor, marker=".", linestyle="none")
plt.plot(x, y, marker=".", linestyle="none")

plt.xlabel("Engagement")
plt.ylabel("ECDF")
plt.legend(('Normal Distribution', 'Empirical Data'), loc='lower right')
#plt.show()
from scipy import stats
print(stats.normaltest(df_new["engagement_rate"]))

#week stats#########################################################################


#pick only relevant columns
week_df = df_new[['impressions', 'engagements', 'engagement_rate', 'retweets','replies',
                  'likes', 'profile_clicks', 'url_clicks', 'date','day','day_name',
                  ]]

# create a group by object
weekday_grouped = df_new.groupby('day_name')

#create a df with means sorted by day
week_mean = weekday_grouped.mean().sort_values(by="day")
week_mean_norm = StandardScaler().fit_transform(week_mean.values)
week_mean_norm_df = pd.DataFrame(week_mean_norm, columns=week_mean.columns, index= week_mean.index)
print(week_mean_norm_df)
#week_mean_norm_df.to_csv('week_mean.csv')


def plot_means_by_weekday(dataframe, variable_1, variable_2=None, variable_3=None):
    # create a figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # set x and y axes
    x = dataframe.index
    y1 = dataframe[variable_1]
    # plot
    ax.plot(x, y1, label=variable_1)

    # add other plots if variables given
    if variable_2 != None:
        y2 = dataframe[variable_2]
        ax.plot(x, y2, label=variable_2)

    if variable_3 != None:
        y3 = dataframe[variable_3]
        ax.plot(x, y3, label=variable_3)

    # format title and labels
    plt.xticks(rotation=45)
    plt.title(f"Average values by day of the week", fontsize=14)
    plt.legend()
    #plt.show()

print(plot_means_by_weekday(week_mean,'engagements', 'retweets', variable_3='likes'))

#####################what can we learn about impressions
# create a group by object
weekday_grouped_1 = df_new.groupby(['day_name','day'])
#plot number of tweets and mean impressions
weekday_count = weekday_grouped_1.agg(['count','mean'])

#pick the impressions column and turn into a separate df
week_impressions = weekday_count['impressions']
#set index to be the day
week_impressions = week_impressions.reset_index()
week_impressions = week_impressions.set_index('day_name')
#sort days
week_impressions = week_impressions.sort_values(by='day')

print(week_impressions)
#plot mean impressions
fig, ax = plt.subplots(figsize=(10,8))

labels = week_impressions.index
width = 0.4

# set x and y axes
x = np.arange(len(labels))
y1 = week_impressions['count']
y2 = week_impressions['mean']

#plot
_ = ax.bar(x + width , y1, width, label='Number of tweets')
_ = ax.bar(x, y2, width, label='Mean impressions')

#format title and labels
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
plt.title("Number of tweets vs mean of impressions by day of the week", fontsize=14)
plt.legend()
plt.show()
#create a column for ratios
s = week_impressions['count']/week_impressions['mean']
week_impressions['ratio'] = s
#print(week_impressions)
#week_impressions.to_csv('week_impressions.csv')

#plot the ratios
#plot mean impressions
fig, ax = plt.subplots(figsize=(10,8))

labels = week_impressions.index

# set x and y axes
x = np.arange(len(labels))
y = week_impressions['ratio']

#plot
_ = ax.bar(x, y, width)

#format title and labels
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.xticks(rotation=45)
plt.title("Ratio of tweets vs impressions day of the week", fontsize=14)

#####################################correlations
df_correl = df_new[['impressions', 'engagements', 'engagement_rate', 'retweets',
       'replies', 'likes', 'profile_clicks', 'url_clicks',  'day']]

corr = df_correl.corr()
corr.to_csv('correlations.csv')

#pairs of corrlations sorted by value
corr_pairs = corr.unstack().sort_values(kind="quicksort")
#plot correlations
fig, ax = plt.subplots(figsize=(17,15))
_ = sns.heatmap(corr, annot = True, ax=ax)

plt.title("Correlation matrix of engagement metrics", fontsize=16)
#plt.show()
#get strong positive
strong_positive = corr_pairs[(corr_pairs >= 0.7) & (corr_pairs < 1)]
# strong get negative correlations
strong_negative = corr_pairs[corr_pairs <= -0.7]
print(f'''There are strong positive correlations between the following pairs of values: \n{strong_positive} 
\nand strong negative correlations between the following pairs of values
\n{strong_negative}
''')


############### hour stats ###################
hour_df = df_new[['impressions', 'engagements', 'engagement_rate', 'retweets','replies',
                  'likes', 'profile_clicks', 'url_clicks', 'date','day','day_name',
                  ]]

# create a group by object
weekday_grouped = df_new.groupby('day_name')

#create a df with means sorted by day
week_mean = weekday_grouped.mean().sort_values(by="day")
week_mean_norm = StandardScaler().fit_transform(week_mean.values)
week_mean_norm_df = pd.DataFrame(week_mean_norm, columns=week_mean.columns, index= week_mean.index)
print(week_mean_norm_df)
#week_mean_norm_df.to_csv('week_mean.csv')


def plot_means_by_weekday(dataframe, variable_1, variable_2=None, variable_3=None):
    # create a figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # set x and y axes
    x = dataframe.index
    y1 = dataframe[variable_1]
    # plot
    ax.plot(x, y1, label=variable_1)

    # add other plots if variables given
    if variable_2 != None:
        y2 = dataframe[variable_2]
        ax.plot(x, y2, label=variable_2)

    if variable_3 != None:
        y3 = dataframe[variable_3]
        ax.plot(x, y3, label=variable_3)

    # format title and labels
    plt.xticks(rotation=45)
    plt.title(f"Average values by day of the week", fontsize=14)
    plt.legend()
    #plt.show()

print(plot_means_by_weekday(week_mean,'engagements', 'retweets', variable_3='likes'))


