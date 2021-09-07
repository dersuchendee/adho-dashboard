

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
pd.set_option('display.max_colwidth',1000)
pd.set_option('display.max_rows', 500)


analytics_april = pd.read_csv("tweet_activity_metrics_ADHOrg_20210401_20210501_en.csv")
analytics_may = pd.read_csv("tweet_activity_metrics_ADHOrg_20210501_20210601_en.csv")
analytics_june = pd.read_csv("tweet_activity_metrics_ADHOrg_20210601_20210701_en.csv")
analytics_july = pd.read_csv("tweet_activity_metrics_ADHOrg_20210701_20210801_en.csv")
analytics_august = pd.read_csv("tweet_activity_metrics_ADHOrg_20210801_20210831_en.csv")
frames = [analytics_april, analytics_may, analytics_june, analytics_july, analytics_august]
analytics_total = pd.concat(frames)
#create a new df keeping only the useful columns
df_new = analytics_total[['Tweet text','time','impressions','engagements','engagement rate','retweets','replies','likes', 'user profile clicks', 'url clicks', 'hashtag clicks', 'detail expands', 'permalink clicks']]
df_new.head(2)

#check for nans
df_new = df_new.replace('-',np.nan)
df_new.isna().sum()
df_new = df_new.dropna()
df_new.isna().sum()

#split the time column into hour and date
df_new['date'] = df_new['time'].astype(str)
# split date into 3 columns
df_new[['date_1','hour','remove']] = df_new['date'].astype(str).str.split(expand=True)
#drop unnecessary columns
df_new = df_new.drop(labels=['time','date','remove'], axis=1)
df_new.head(2)
from datetime import datetime
df_new['hour']= df_new['hour'].astype(str)
#format hour column as date time
df_new['hour'] =pd.to_datetime(df_new['hour']).dt.hour


#format date column as date time
df_new['date_1'] = pd.to_datetime(df_new['date_1'], format='%Y-%m-%d')
#add weekday column
df_new['day'] = df_new['date_1'].dt.weekday
df_new['day_name'] = df_new['date_1'].dt.day_name()

#rename columns
df_new = df_new.rename(columns = {'Tweet text':'text',
                                  'user profile clicks':'profile_clicks', 'url clicks':'url_clicks', 'engagement rate':'engagement_rate',
                                  'hashtag clicks':'hashtag_clicks', 'detail expands':'detail_expands',
                                  'permalink clicks':'permalink_clicks',
                                  'date_1':'date'
                                })


#df_new['hour'] = df_new['hour'].apply(pd.Timestamp)
#df_new.hour.astype('datetime64[h]')
#df_new['hour'] = df_new.timestamp.apply(lambda x: x.hour)
# create a group by object
print(df_new['hour'].dtype)

weekday_grouped = df_new.groupby('hour')

#create a df with means sorted by day
week_mean = weekday_grouped.mean().sort_values(by="hour")
week_mean_norm = StandardScaler().fit_transform(week_mean.values)
week_mean_norm_df =  pd.DataFrame(week_mean_norm, columns=week_mean.columns, index= week_mean.index)
print(week_mean)
week_mean.to_csv('hours_stats.csv')

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
    plt.show()

print(plot_means_by_weekday(week_mean,'engagements', 'retweets', variable_3='likes'))


