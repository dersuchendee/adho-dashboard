import pandas as pd
import re
from dateutil.parser import parse
import plotly.express as px
import numpy as np
pd.set_option('display.max_colwidth',1000)
pd.set_option('display.max_rows', 500)

df = pd.read_csv('ok.csv')

### activity timeline
df['created_at'] = [x.replace(" ora legale Europa occidentale", "") for x in df['created_at']]
df['created_at'] = [x.replace(" ora solare Europa occidentale", "") for x in df['created_at']]
df['date'] = [parse(date).date() for date in df['created_at']]
df['monthyear'] = pd.to_datetime(df['date']).dt.to_period('M')
by_month = pd.to_datetime(df['date']).dt.to_period('M').value_counts().sort_index()
by_month.index = pd.PeriodIndex(by_month.index)
df_month = by_month.rename_axis('month').reset_index(name='counts')
df_month['month'] = df_month['month'].astype(str)
print(df_month)
df_july = pd.read_csv('daily_tweet_activity_metrics_ADHOrg_20210701_20210731_en.csv')
#print(df_july.columns)
july = df_july[['Date', 'Tweets published']].copy()
july['Date'] = pd.to_datetime(july['Date']).dt.to_period('M')
july.columns=['month', 'counts']
df1 = july.groupby('month', as_index=False)['counts'].sum()
merged_df = pd.concat([df_month, df1])
print(merged_df)
merged_df.to_csv('activity_07_2021.csv')
#df_month.to_csv('activity_timeline.csv')
#fig = px.line(df_month, x = 'month', y = 'counts', title='Tweets per month')
#fig.show()

### most used hashtags

new = df[['hashtags']].copy()
new = new.dropna()
new['hashtags'] = new['hashtags'].apply(lambda x: x.replace('[','').replace(']',''))
new['hashtags'] = new['hashtags'].str.split(',')
out =new.hashtags \
  .explode() \
  .value_counts() \
  .reset_index() \
  .rename(columns={"index": "hashtags", "hashtags": "counts"})
out = out.iloc[1: , :]
#print(out)
#out.to_csv('most_used_hashtags.csv')
#fig = px.bar(out, x = 'hashtags', y = 'counts', title='hashtags')
#fig.show()

### who do we retweet from?
regex = r"(?<=status).+"
regex2 = r"^[0-9]*$"
retweets = df[['quote_url']].copy()
retweets = retweets.dropna()
new_retweets = retweets.replace(to_replace =regex, value = '', regex = True)

new_retweets['quote_url'] = new_retweets['quote_url'].apply(lambda x: x.replace('https://twitter.com/','').replace('/status',''))

nrt = new_retweets.value_counts().rename_axis('quote_url').reset_index(name='count')
#nrt.to_csv('most_retweeted.csv')

#print(nrt)

#fig = px.bar(nrt, x = 'quote_url', y = 'count', title='Most retweeted')
#fig.show()

### tweets with more likes

likes = df[['tweet', 'likes_count']].copy()
likes = likes.dropna()
likes = likes.drop_duplicates()
likes = likes[likes.likes_count != 0]
likes = likes.sort_values(by=['likes_count'], ascending=False)
likes = likes[:30]
#out.to_csv('most_liked.csv')


#print(likes)
#fig = px.bar(likes, x = 'tweet', y = 'likes_count', title='Most liked')
#fig.show()

### tweets with the most replies
replies = df[['tweet', 'replies_count']].copy()
replies = replies.dropna()
replies = replies.drop_duplicates()
replies = replies[replies.replies_count != 0]
replies = replies.sort_values(by=['replies_count'], ascending=False)
replies = replies[:30]
#out.to_csv('most_replied.csv')


#print(replies)
#fig = px.bar(replies, x = 'tweet', y = 'replies_count', title='Tweets with most replies')
#fig.show()

### hours with most likes/replies/interaction
hours = df[['time', 'likes_count']].copy()
regex3 = r":[\s\S]*$"

hours = hours.dropna()
hours = hours.drop_duplicates()
hours = hours[hours.likes_count != 0]
hours = hours.replace(to_replace =regex3, value = '', regex = True)
hours = hours.groupby(by=["time"], as_index=False)['likes_count'].sum()
hours = hours.sort_values(by='likes_count', ascending=False)
hours = hours[:30]
#hours.to_csv('best_hours.csv')

#print(hours)
#fig = px.bar(hours, x = 'time', y = 'likes_count', title='Hours with the most likes')
#fig.show()



############ hashtags
# count number of mentions or hashtags
# takes in the symbol, returns an object with number of unique items, sorted frequency, a list of all itmes, top 10
# in the WHOLE dataset
df_new= df.copy()

def extract_list(hashtag_or_mention):
    item_list = []
    for row in df_new['tweet']:
        items = [tag.strip(hashtag_or_mention) for tag in row.split() if tag.startswith(hashtag_or_mention)]
        punct = [".", "?", "!", ":", "'", "]", "[", ";", ","]
        # remove punctuation from, it leaves us with a list of letters
        item_no_punct = [[l for l in item if l not in punct] for item in items]
        # joint the letters back into words
        items_formated = [''.join(item) for item in item_no_punct]
        item_list.append(items_formated)

    # turn a list of lists into one list
    items_list_all = [item for sublist in item_list for item in sublist]
    # turn into a set to chck uniques
    uniques = list(set(items_list_all))
    # count uniques
    number_of_unique_items = len(uniques)
    # frequency dict
    frequency_dict = {i: items_list_all.count(i) for i in items_list_all}
    # convert into df
    frequency_df = pd.DataFrame(frequency_dict.items(), columns=["word", "count"])
    # sort values
    sorted_frequency = frequency_df.sort_values(by='count', ascending=False)

    # get top 10 values
    top_10_df = sorted_frequency.head(10)
    top_10 = list(top_10_df['word'])

    class i_list:
        def __init__(self):
            #             no_uniques, list_uniques, full_list
            self.no_uniques = number_of_unique_items
            self.list_uniques = uniques
            self.full_list = items_list_all
            self.sorted_frequency = sorted_frequency
            self.top_10 = top_10

        def how_many(self):
            return f"This set of tweets has {self.no_uniques} unique {hashtag_or_mention}s."

        def list_top_10(self):
            return f"The top 10 {hashtag_or_mention}s used in this set of tweets are: {self.top_10}."

    item_list = i_list()

    return item_list

hashtag_list = extract_list('#')
print(hashtag_list.how_many())
hashtag_frequency_df = hashtag_list.sorted_frequency
# create a column with all hashtags per tweet
# function to extract all hashtags or mentions

def extractor(row, hashtag_or_mention):
    words = [tag.strip(hashtag_or_mention) for tag in row.split() if tag.startswith(hashtag_or_mention)]
    punct = [".","?","!",":","'","]","[",";"]
    #remove punctuation from hashtags, it leaves us with a list of letters
    no_punct = [[l for l in item if l not in punct] for item in words]
    #join the letters back into words
    words_formated = [''.join(item) for item in no_punct]
    return words_formated

df_new['hashtags_list'] = df_new['tweet'].apply(lambda x: extractor(x, '#'))

#clean column
df_new['hashtags_list'] = df_new['hashtags_list'].astype(str).str.replace(']','').str.replace('[','').str.replace("'","")

#check
df_new['hashtags_list'].head(2)

#check
print(df_new.head())



mention_list = extract_list("@")
mention_list.how_many()
mention_list.list_uniques
mention_list.list_top_10()
mention_list_df = mention_list.sorted_frequency
mention_list_df.head(5)
#use the previous extractor function to create a column with a list of mentions
df_new['mentions_list'] = df_new['tweet'].apply(lambda x: extractor(x, '@'))
#clean column
df_new['mentions_list'] = df_new['mentions_list'].astype(str).str.replace(']','').str.replace('[','').str.replace("'","")

#check
print(mention_list_df)
#mention_list_df.to_csv('most_mentioned.csv')


