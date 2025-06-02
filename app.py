import streamlit as st
import helper
import prepro
import matplotlib.pyplot as plt
import seaborn as sns
# print(st.__version__)
st.sidebar.title("WhatsStat")

uploaded_file = st.sidebar.file_uploader("Choose a file to Analyse")
if uploaded_file is not None:
    b_d=uploaded_file.getvalue()
    data = b_d.decode("utf-8")
    df= prepro.preprocess(data)
    # st.dataframe(df)

    # IDENTIFY UNIQUE USERS----------------
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user=st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Stats")
        num_messages, words, num_media, num_links= helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4=st.columns(4)
        # st.title("Top Stats")
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Files")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #  timeline analysis
        st.title('Montly TimeLine Analysis')
        timeline= helper.df_tl(selected_user, df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title('Daily TimeLine Analysis')
        d_tl = helper.daily_tl(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_tl['itsDate'], d_tl['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map
        st.title('Activity Map')
        col1, col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            b_d= helper.weekly_df(selected_user, df)
            fig, ax=plt.subplots()
            ax.bar(b_d.index,b_d.values, color='pink')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            b_m = helper.month_df(selected_user, df)
            fig, ax = plt.subplots()
            ax.pie(b_m.values,labels=b_m.index,autopct="%0.2f")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Activity HeatMap--------------
        st.title('Weekly Activity Map')
        Act_hMap= helper.activity_heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(Act_hMap)
        st.pyplot(fig)



        #  finding the most active user-----------------------
        if selected_user=='Overall':
            st.title('Most Active users')
            x, new_df= helper.most_busy_users(df)
            fig, ax =plt.subplots()

            col1, col2 =st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='brown')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        # creating the wordcloud---------------------------
        st.title("WordCloud")
        df_wc= helper.create_word_cloud(selected_user, df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

#         most common words
        common_words= helper.most_common_words(selected_user, df)
        st.title('Most Common Words')
        fig, ax=plt.subplots(figsize=(10,12))
        col1, col2=st.columns(2)
        with col1:
            ax.barh(common_words[0],common_words[1],color="purple")
            plt.xticks()

            st.pyplot(fig)
        with col2:
            st.dataframe(common_words)


         # analyse emojis--------------------
        em_df= helper.count_emoji(selected_user, df)
        st.title('Emoji Analysis')
        col1, col2=st.columns(2)
        with col1:
            fig, ax= plt.subplots()
            ax.pie(em_df[1].head(), labels=em_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        with col2:
            st.dataframe(em_df)
