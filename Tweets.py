import twint
#import nest_asyncio
#nest_asyncio.apply()
import pandas as pd
pd.set_option('display.max_colwidth',1000)

c = twint.Config()
c.Username = "ADHOrg"
c.Since = "2020-01-01"
c.Until = "2021-06-30"
c.Pandas= True
#c.Popular_tweets = True
c.Store_csv = True
c.Output = "ok.csv"
#c.Native_retweets = True
twint.run.Search(c)
print(twint.storage.panda.Tweets_df.head())


#àdata.head()
#data.to_csv('df.csv')
