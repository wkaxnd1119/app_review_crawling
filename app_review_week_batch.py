 
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

 

# 카드사 구분 코드 
df_hana['app'] = '원큐페이'
df_paybook['app'] = '페이북'
df_toss['app'] = '토스'
df_kakao['app'] = '카카오페이'
df_hyundai['app'] = '현대카드'

 

# 데이터 합쳐서 전송하기 
df_list = [df_hana, df_paybook, df_toss, df_kakao, df_hyundai]
df_total = pd.DataFrame()

for data in df_list:
    print(str(data))
    df_total = pd.concat([df_total, data])


df_total = df_total[['at', 'app','reviewId', 'userName', 'userImage', 'content', 'score',
       'thumbsUpCount', 'reviewCreatedVersion', 'replyContent',
       'repliedAt']]

# 전주 데이터만 갖고오기 (월~ 다음주 일요일까지)
date_ = datetime.datetime.today() - datetime.timedelta(days=7) 
df_total['week_number'] = df_total['at'].apply(lambda x: x.isocalendar()[1])
todays_review = df_total[df_total['week_number'] == date_.isocalendar()[1]][df_total.columns]
todays_review.fillna('_', inplace=True)
todays_review.pop('week_number')


#제목에 쓰일 date
date_string =  date_.isocalendar()[1]

 
#CSV로 저장
todays_review.reset_index(drop=True).to_csv(path + f'/app_review_week{date_string}.csv')

 