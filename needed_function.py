from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()


def fetch_data(selected_user, df):
    if selected_user == 'Overall Group':
        num_message = df.shape[0]

        word = []
        for msg in df['message']:
            word.extend(msg.split())

        num_media_share = df[df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for msg in df['message']:
            links.extend(extract.find_urls(msg))

        return num_message, len(word), num_media_share, len(links)
    else:
        temp_df = df[df['users'] == selected_user]
        num_message = temp_df.shape[0]

        word = []
        for msg in temp_df['message']:
            word.extend(msg.split())

        num_media_share = temp_df[temp_df['message'] == '<Media omitted>\n'].shape[0]

        links = []
        for msg in temp_df['message']:
            links.extend(extract.find_urls(msg))

        return num_message, len(word), num_media_share, len(links)

        # Find busy users in the group


def fetch_top_chatter(df):
    top_chatter = df['users'].value_counts().head(13).sort_values(ascending=False)
    df = round((df['users'].value_counts()/df['users'].shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percentage'})
    return top_chatter, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    stopwords = {'<Media omitted>\n', 'This message was deleted'}

    def preprocess_text(text, stopwords):
        # Replace specific words with an empty string to remove them
        for word in stopwords:
            text = text.replace(word, '')

        return text

    # Convert 'message' column to strings
    df['message'] = df['message'].astype(str)

    # Preprocess text and remove empty messages
    df['message'] = df['message'].apply(lambda text: preprocess_text(text, stopwords))
    df = df[df['message'].str.len() > 1]

    # Check if there are non-empty messages to generate the Word Cloud
    if df['message'].str.strip().str.len().any():  # This checks if there are any non-empty messages
        wc = WordCloud(width=500, height=250, min_font_size=14, background_color='black', stopwords=stopwords)
        df_wc = wc.generate(df['message'].str.cat(sep=" "))
        return df_wc
    else:
        return None

def most_common_words(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    temp_df = df[df['users'] != 'group notification']
    temp = temp_df[temp_df['message'] != '<Media omitted>\n']

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    f.close()

    words = []

    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    x = pd.DataFrame(Counter(words).most_common(30))
    return x


def find_emoji(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    Emoji = []
    for msg in df['message']:
        if isinstance(msg, str):
            Emoji.extend([em for em in msg if em in emoji.EMOJI_DATA])

    if len(Emoji) == 0:
        return pd.DataFrame(columns=['emoji', 'count'])
    else:
        em_df = pd.DataFrame(Counter(Emoji).most_common(len(Counter(Emoji))))
        return em_df


def daily_month(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_day(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    temp = df['day_name'].value_counts().reset_index(name='messageCount')
    return temp


def daily_month_bar(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    temp = df['month'].value_counts().reset_index(name='messageCount')
    return temp


def heatmap_hour(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]

    temp_df = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return temp_df


def top_10(selected_user, df):
    if selected_user != 'Overall Group':
        df = df[df['users'] == selected_user]
    return df










