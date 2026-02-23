import pandas as pd
from textblob import TextBlob

print("Učitavam očišćene recenzije...")
df = pd.read_csv('ociscene_recenzije.csv')

def analiziraj_tekst(tekst):
    tekst = str(tekst)
    blob = TextBlob(tekst)

    return blob.sentiment.polarity

df['Sentiment_Score'] = df['Recenzija'].apply(analiziraj_tekst)

def kategorija(skor):
    if skor > 0.1:
        return 'Pozitivna'
    elif skor < -0.1:
        return 'Negativna'
    else:
        return 'Neutralna'

df['Emocija'] = df['Sentiment_Score'].apply(kategorija)

print("\n--- PROSEČAN SENTIMENT PO GRADOVIMA ---")
statistika = df.groupby('Grad')['Sentiment_Score'].mean()
print(statistika)

df.to_csv('finalna_analiza.csv', index=False, encoding='utf-8')