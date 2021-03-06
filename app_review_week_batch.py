 
import json
import pandas as pd
import numpy as np
import datetime

from google_play_scraper import Sort, reviews_all, reviews
 
path = r'C:\Users\user\Desktop\python\daily_app_review_batch'

###############################################################

#Daily Batch

###############################################################

 
## hanacard 

dict_hana, _  = reviews(
    'com.hanaskcard.paycla',
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    count=1000 # defaults to None(means all score)
)


dict_paybook, _ = reviews(
    'kvp.jjy.MispAndroid320',
    #sleep_milliseconds=0, # defaults to 0
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    count=1000 # defaults to None(means all score)
)

 
dict_toss, _ = reviews(
    'viva.republica.toss',
    #sleep_milliseconds=0, # defaults to 0
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    count=1000 # defaults to None(means all score)
)


dict_kakao, _  = reviews(
    'com.kakaopay.app',
    #sleep_milliseconds=0, # defaults to 0
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    count=1000 # defaults to None(means all score)

)

dict_hyundai, _  = reviews(
    'com.hyundaicard.appcard',
    #sleep_milliseconds=0, # defaults to 0
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    count=1000 # defaults to None(means all score)

)


# json to dataframe 
df_hana = pd.DataFrame.from_dict(dict_hana, orient='columns')
df_paybook = pd.DataFrame.from_dict(dict_paybook, orient='columns')
df_toss = pd.DataFrame.from_dict(dict_toss, orient='columns')
df_kakao = pd.DataFrame.from_dict(dict_kakao, orient='columns')
df_hyundai = pd.DataFrame.from_dict(dict_hyundai, orient='columns')

 

# ????????? ?????? ?????? 
df_hana['app'] = '????????????'
df_paybook['app'] = '?????????'
df_toss['app'] = '??????'
df_kakao['app'] = '???????????????'
df_hyundai['app'] = '????????????'

 

# ????????? ????????? ???????????? 
df_list = [df_hana, df_paybook, df_toss, df_kakao, df_hyundai]
df_total = pd.DataFrame()

for data in df_list:
    print(str(data))
    df_total = pd.concat([df_total, data])


df_total = df_total[['at', 'app','reviewId', 'userName', 'userImage', 'content', 'score',
       'thumbsUpCount', 'reviewCreatedVersion', 'replyContent',
       'repliedAt']]

# ?????? ???????????? ???????????? (???~ ????????? ???????????????)
date_ = datetime.datetime.today() - datetime.timedelta(days=7) 
df_total['week_number'] = df_total['at'].apply(lambda x: x.isocalendar()[1])
todays_review = df_total[df_total['week_number'] == date_.isocalendar()[1]][df_total.columns]
todays_review.fillna('_', inplace=True)
todays_review.pop('week_number')


#????????? ?????? date
date_string =  date_.isocalendar()[1]

 
#CSV??? ??????
todays_review.reset_index(drop=True).to_csv(path + f'/app_review_week{date_string}.csv')

 