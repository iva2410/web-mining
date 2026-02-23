import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.set_page_config(page_title="Sistem za preporuku restorana", layout="wide")

@st.cache_data 
def load_data():
    df = pd.read_csv('finalna_analiza.csv')
    df = df.groupby(['Restoran', 'Grad']).agg({
        'Recenzija': lambda x: ' '.join(x.astype(str)),
        'Sentiment_Score': 'mean',
        'Ocena': 'mean'
    }).reset_index()
    df['opis_za_algoritam'] = df['Grad'] + " " + df['Recenzija'].fillna('')
    return df

df = load_data()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['opis_za_algoritam'])

st.title("🍴 Gastro-Navigator")
st.markdown("Na osnovu mesta koja volite, pronalazimo slične restorane sa najpozitivnijim utiscima širom Evrope.")

st.sidebar.header("Tvoji omiljeni restorani")
omiljeni_nazivi = st.sidebar.multiselect("Pretraži i dodaj:", options=df['Restoran'].unique())
st.sidebar.write("Trenutno u listi:", len(omiljeni_nazivi))


st.sidebar.markdown("---")
izabrani_grad = st.sidebar.selectbox("Gde tražimo slične restorane?", options=["Svi gradovi"] + list(df['Grad'].unique()))


st.sidebar.markdown("---")
st.sidebar.header("🍕 Šta ti se jede?")
kuhinja = st.sidebar.multiselect(
    "Izaberi hranu:",
    options=["Italijanska kuhinja", "Pizza", "Pasta", "Sushi", "Azijska kuhinja", "Meso", "Burger", "Domaća kuhinja", "Riba", "Poslastice"]
)

if omiljeni_nazivi or kuhinja:
    
    if omiljeni_nazivi:
        indeksi_omiljenih = df[df['Restoran'].isin(omiljeni_nazivi)].index
        vektor_restorana = tfidf_matrix[indeksi_omiljenih].mean(axis=0)
    else:
        vektor_restorana = np.zeros((1, tfidf_matrix.shape[1]))

    if kuhinja:
        tekst_kuhinje = " ".join(kuhinja)
        vektor_kuhinje = tfidf.transform([tekst_kuhinje]).toarray()
    else:
        vektor_kuhinje = np.zeros((1, tfidf_matrix.shape[1]))
    
    korisnicki_profil = (np.asarray(vektor_restorana) + np.asarray(vektor_kuhinje) * 1.5)
    
    slicnost_skorovi = cosine_similarity(korisnicki_profil, tfidf_matrix).flatten()
    
    df['Slicnost'] = slicnost_skorovi
    preporuke = df[~df['Restoran'].isin(omiljeni_nazivi)]
    
    if izabrani_grad != "Svi gradovi":
        preporuke = preporuke[preporuke['Grad'] == izabrani_grad]
    
    sve_preporuke = preporuke.sort_values(by=['Slicnost', 'Sentiment_Score'], ascending=False)
    finalne_preporuke = sve_preporuke.head(10)

    st.subheader(f"✨ Najbolji predlozi za lokaciju: {izabrani_grad}")    
    za_prikaz = [finalne_preporuke[i:i+5] for i in range(0, len(finalne_preporuke), 5)]
    
    for grupa in za_prikaz:
        cols = st.columns(len(grupa))
        for i, (index, row) in enumerate(grupa.iterrows()):
            with cols[i]:
                st.success(f"**{row['Restoran']}**")
                st.caption(f"📍 {row['Grad']}")
                st.write(f"Ocena: {round(row['Ocena'])}⭐")
               # st.write(f"Sličnost: {round(row['Slicnost']*100, 1)}%")
                search_query = f"{row['Restoran']} {row['Grad']}".replace(" ", "+")
                google_link = f"https://www.google.com/search?q={search_query}"
                st.markdown(f"🔗 [DETALJNIJE]({google_link})")

else:
    st.info("Dodaj restorane u listu omiljenih sa leve strane da dobiješ preporuke.")
    st.image("https://www.byblos.com/wp-content/uploads/Restaurant-IL-Giardino_Hotel-Byblos_Saint-Tropez-%C2%A9Stephan-Julliard-7-1600x1000.jpg") # Ukrasna slika