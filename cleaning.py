import pandas as pd

df = pd.read_csv('recenzije_restorana.csv')

print(f"Početni broj redova: {len(df)}")

df = df.drop_duplicates()

df['Ocena'] = pd.to_numeric(df['Ocena'], errors='coerce').fillna(0)

zabranjene_fraze = [
    "Rewards Discover", "Sign in", "Tripadvisor is not responsible", 
    "subjective opinion", "trust & safety", "Forums", "Cruises",
    "economic search tools", "Economic", "Books", "Flights", "reviews)",
    "Dear Customer", "Dear Guest", "Kind regards","Best wishes","Thank you for sharing your", "Thank you for your", "looking forward",
    "Sponsored","50% off", "Order online", "Reserve", "See all", "Open now", "Check availability"
]
df['Recenzija'] = df['Recenzija'].str.encode('ascii', 'ignore').str.decode('ascii')
df['Recenzija'] = df['Recenzija'].str.replace('⭐', '', regex=False)
for fraza in zabranjene_fraze:
    df = df[~df['Recenzija'].str.contains(fraza, case=False, na=False,regex=False)]

df = df[df['Recenzija'].str.len() > 50]

df['Recenzija'] = df['Recenzija'].str.replace(r'\n', ' ', regex=True).str.strip()


print(f"Broj redova nakon čišćenja: {len(df)}")

df.to_csv('ociscene_recenzije.csv', index=False, encoding='utf-8')
