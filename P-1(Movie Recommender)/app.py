# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# # ------------------ Load Data ------------------ #

# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open('similarity.pkl', 'rb'))

# API_KEY = "9f71ae8ac3b37d6ca17bc17a458ab85d"


# # ------------------ Fetch Poster ------------------ #

# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

#         response = requests.get(url, timeout=10)
#         response.raise_for_status()

#         data = response.json()

#         if data.get("poster_path"):
#             return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Poster"

#     except Exception:
#         return "https://via.placeholder.com/500x750?text=No+Poster"


# # ------------------ Recommend ------------------ #

# def recommend(movie):

#     movie_index = movies[movies['title'] == movie].index[0]

#     distances = similarity[movie_index]

#     movies_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]

#     recommended_movies = []
#     recommended_posters = []

#     for i in movies_list:

#         recommended_movies.append(movies.iloc[i[0]].title)

#         # movie_id ya id dono handle karega
#         if "movie_id" in movies.columns:
#             movie_id = movies.iloc[i[0]].movie_id
#         else:
#             movie_id = movies.iloc[i[0]].id

#         poster = fetch_poster(movie_id)

#         recommended_posters.append(poster)

#     return recommended_movies, recommended_posters


# # ------------------ Streamlit ------------------ #

# st.title("🎬 Movie Recommender System")

# selected_movie_name = st.selectbox(
#     "Select Movie",
#     movies['title'].values
# )

# if st.button("Recommend"):

#     names, posters = recommend(selected_movie_name)

#     col1, col2, col3, col4, col5 = st.columns(5)

#     with col1:
#         st.text(names[0])
#         st.image(posters[0])

#     with col2:
#         st.text(names[1])
#         st.image(posters[1])

#     with col3:
#         st.text(names[2])
#         st.image(posters[2])

#     with col4:
#         st.text(names[3])
#         st.image(posters[3])

#     with col5:
#         st.text(names[4])
#         st.image(posters[4])





import streamlit as st
import pickle
import pandas as pd
import requests

# ================== TMDB API KEY ==================
API_KEY = "9f71ae8ac3b37d6ca17bc17a458ab85d"


# ================== LOAD DATA ==================
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ================== FETCH POSTER ==================
def fetch_poster(movie_id, movie_name):

    # Try fetching by movie ID
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("poster_path"):
                return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except:
        pass

    # Fallback: Search by movie title
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

        response = requests.get(search_url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if len(data["results"]) > 0:
                poster = data["results"][0].get("poster_path")

                if poster:
                    return "https://image.tmdb.org/t/p/w500" + poster

    except:
        pass

    # Placeholder
    return "https://via.placeholder.com/300x450?text=No+Poster"


# ================== RECOMMEND ==================
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]]['movie_id']
        movie_name = movies.iloc[i[0]]['title']

        recommended_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_id, movie_name))

    return recommended_movies, recommended_posters


# ================== UI ==================
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select Movie",
    movies['title'].values
)

if st.button("Recommend"):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])