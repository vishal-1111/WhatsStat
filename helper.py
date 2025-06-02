import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
extract=URLExtract()


def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    # find no. of messages
    num_messages = df.shape[0]
    #  find no. of words and links
    words=[]
    links = []
    for message in df['message']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))
    #  find no. of media files
    num_media= df[df['message']=='<Media omitted>\n'].shape[0]
    return num_messages,len(words),num_media,len(links)


# most active users
def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'user':'Name','count':'Percentage %'})
    return x,df


# creating the word cloud
def create_word_cloud(selected_user,df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_sw(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_sw)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# most common words
def most_common_words(selected_user,df):
    with open('stop_hinglish.txt','r') as f:
        stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and not re.search(r'\d', word):
                words.append(word)
    common_words=pd.DataFrame(Counter(words).most_common(20))
    return common_words

#  emoji analysis
def count_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    em_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return em_df

#   montly message timeline
def df_tl(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

# daily message timeline
def daily_tl(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    d_tl=df.groupby('itsDate').count()['message'].reset_index()
    return d_tl


# weekly activity
def weekly_df(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

# month activity map
def month_df(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

# activity heat map

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    ac_hm=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return ac_hm