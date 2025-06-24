
import streamlit as st
import preprocessor
import helper



st.sidebar.title("Whatsapp Chat Analysis")


#to read that file into app
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:  #Agar file upload hui hai, tabhi agla code chalega.
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)
    st.dataframe(df) # showing data in streamlit app


    #Jab user koi file upload karega,
    # to yeh code us file ka data read karega,
    # clean karega, aur Streamlit app ke andar
    # ek table ke format me show karega.

    #fetch unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("show analysis wrt",user_list)


    if st.sidebar.button("Show analysis"):


        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics of Whatsapp Chats")
        col1, col2, col3,col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)





























