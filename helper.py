from urlextract import URLExtract
extractor = URLExtract()
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df["message"]:
        words.extend(message.split())

    num_media_messages= df[df["message"] == "<Media omitted>\n"].shape[0]


    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"user":"name", "count":"percent"})
    return x,df


def most_common_words(selected_user,df):
    f = open("stop_hinglish.txt","r")
    stop_word = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

        #st.title('Most Busy Users')


    temp = df[df["user"] != "group notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df




def emoji_helper(selected_user,df):
     if selected_user != "Overall":
         df = df[df["user"] == selected_user]

     emojis = []
     for message in df["message"]:
         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

     return emoji_df




def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    daily_timeline = df.groupby("only_date").count()["message"].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df["month"].value_counts() # to count months activity


def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    user_heatmap = (df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0))

    return  user_heatmap















