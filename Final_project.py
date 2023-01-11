import pandas as pd
import streamlit as st
import altair as alt
import requests
from bs4 import BeautifulSoup


#Если у Вас возникнут проблемы с стримлит проектом, пожалуйста, воспроизведите его через свой компьютер. Спасибо!
#Решение математической задачи - в другом файле: problem.py

st.title('This is a project, completed by an anonymous.')
st.header("Project's main topic is music.")
st.caption('This is a string that explains something above.')


with st.echo():

    @st.cache
    def get_data():
        data_url = "https://github.com/russhams/streamlit/raw/main/top_albums.csv"
        return pd.read_csv(data_url).drop(columns=["Unnamed: 0", "sec_genres"])

    df = get_data()

    #df

    st.subheader("Okay, by choosing an artist below you can see various information about his albums. "
                 "Please, delete the word 'Radiohead' in the selectbox and type "
                 "'Frank Ocean'! "
                 "Something interesting would be below..")

    artist_selection = st.selectbox("Let's find it out! Type the name down there",
                                    options=df["artist"].unique())

    df_of_your_artist = df[lambda x: x['artist'] == artist_selection]

    st.caption("You can find URL links to various streaming services below and copy them to find it in the Internet!")

    df_of_your_artist.iloc[:, 9:-1]

    st.subheader("So, you can observe an easter egg below, if you write 'Frank Ocean' above. "
             "You can click it and listen to this wonderful composition! "
             "Hope, you will enjoy it! I set timings in such way, "
             "that the video starts from the song 'Pink + White', one of his greatest songs imho. "
             "If you can't see no video below, than you should type 'Frank Ocean' above! "
             "It is connected to some part below, see the code. ")

    st.subheader("If an error occurs, please, type 'Frank Ocean' above!")

    url_blonde = df[lambda x: x['artist'] == artist_selection].iloc[:, 9][87]

    st.video(url_blonde, format="video", start_time=562)

    entrypoint = "https://www.amalgama-lab.com/songs/f/frank_ocean/pink_white.html"
    r = requests.get(entrypoint)
    page = BeautifulSoup(r.text, 'html.parser')
    text_translation = page.html.find_all('div')[221].text.split("\n")
    og_text = []
    translation = []


    cleared_text_list = []
    i = 0
    while i < len(text_translation):
        if text_translation[i] != '':
            cleared_text_list.append(text_translation[i])
            del text_translation[i]
        else:
            i += 1

    for i in range(len(cleared_text_list)):
        if i % 2 == 0:
            og_text.append(cleared_text_list[i])
        if i % 2 == 1:
            translation.append(cleared_text_list[i])
    og_text.pop(-1)
    translation.pop(-1)
    og_text.pop(-2)
    translation.pop(-2)

    st.header("So, here we see the lyrics of this song!")
    for i in range(len(og_text)):
        st.text(str(i) + ". "  + og_text[i])

    st.header("Translation of this text!")
    st.subheader("You can check it, if you're interested..")
    for i in range(len(translation)):
        st.text(str(i) + ". "  + translation[i])

    st.caption('One of strings was deleted by me because it contained a bit of obscene language...')

    st.subheader("So, it's a chart below with information about genres and how much they appear.")
    total_numbers = []

    for i in range(len(df.index)):
        total_numbers.append(df["pr_genres"].iloc[i])

    total_numbers = ", ".join(total_numbers)
    total_list = total_numbers.split(", ")


    total_dict = dict((i, total_list.count(i)) for i in set(total_list) if total_list.count(i) >= 1)

    sorted_dict = {}
    sorted_keys = sorted(total_dict, key=total_dict.get)
    for x in sorted_keys:
        sorted_dict[x] = total_dict[x]

    df_genres = pd.DataFrame({'Count': sorted_dict.values(),
                          'Genres': sorted_dict.keys()})

    bars = alt.Chart(df_genres).mark_bar().encode(
        x='Count:Q',
        y="Genres:O"
    )
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3
    ).encode(
        text='Count:Q'
    )

    st.altair_chart((bars + text))

    st.subheader("Okay, let's find out some albums, that connected to Pop genre, if it is a main genre!")
    st.caption("Just because I like it very much...")

    df[df['pr_genres'].str.match(r'\b.[o][p]\s.', case=True)]