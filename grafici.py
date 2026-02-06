import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from wordcloud import WordCloud

df = pd.read_csv("finalna_analiza.csv")
df = df.groupby(['Restoran', 'Grad']).agg({
    'Recenzija': lambda x: ' '.join(x.astype(str)),
    'Sentiment_Score': 'mean'
}).reset_index()

# sentiment distribucija 
plt.figure()
plt.hist(df['Sentiment_Score'], bins=30)
plt.xlabel("Sentiment score")
plt.ylabel("Broj restorana")
plt.title("Distribucija sentiment skora")
plt.show()

# tf-idf analiza
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Recenzija'].fillna(""))

feature_names = np.array(tfidf.get_feature_names_out())

indeks = 0  
ime_restorana = df.iloc[indeks]['Restoran']
vektor = tfidf_matrix[indeks].toarray().flatten()

top_indices = vektor.argsort()[-15:]
top_values = vektor[top_indices]
top_words = feature_names[top_indices]

plt.figure(figsize=(10, 6))
plt.barh(top_words, top_values, color='skyblue')
plt.xlabel('TF-IDF Težina (Značaj reči)')
plt.title(f'Top 15 najznačajnijih reči za: {ime_restorana}')
plt.grid(axis='x', linestyle='--', alpha=0.7)

for i, v in enumerate(top_values):
    plt.text(v, i, f' {v:.4f}', va='center')

plt.tight_layout()
plt.show()

mean_tfidf = tfidf_matrix.mean(axis=0).A1

top_idx = mean_tfidf.argsort()[-10:][::-1]

plt.figure()
plt.barh(feature_names[top_idx][::-1], mean_tfidf[top_idx][::-1])
plt.xlabel("Prosečna TF-IDF vrednost")
plt.title("Najznačajniji termini u recenzijama")
plt.show()

pca = PCA(n_components=2)
tfidf_2d = pca.fit_transform(tfidf_matrix.toarray())

plt.figure()
plt.scatter(tfidf_2d[:, 0], tfidf_2d[:, 1])
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("PCA projekcija restorana")
plt.show()
