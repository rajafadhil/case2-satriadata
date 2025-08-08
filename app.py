import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.title("📊 Dashboard Analisis Tweet Pilpres 2024")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("case2_dataclean (2).csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["hour"] = df["created_at"].dt.hour
    return df

df = load_data()

# Sidebar filter
st.sidebar.header("🔎 Filter")
selected_hour = st.sidebar.slider("Filter jam tweet:", 0, 23, 12)

# Bersihkan teks
def clean_text(text):
    text = text.lower()
    text = re.sub(r'rt\s+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["cleaned_text"] = df["content"].apply(clean_text)

# Filter berdasarkan jam
filtered_df = df[df["hour"] == selected_hour]

st.subheader(f"📁 Data pada jam {selected_hour}")
st.write(filtered_df.head())

# Grafik jumlah tweet per jam
tweet_counts = filtered_df["hour"].value_counts().sort_index()
st.subheader("⏰ Distribusi Tweet per Jam")
fig1, ax1 = plt.subplots()
bars1 = tweet_counts.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Jam")
ax1.set_ylabel("Jumlah Tweet")

# Tambahkan angka di atas bar
for p in bars1.patches:
    ax1.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()),
                 ha='center', va='bottom', fontsize=9)

st.pyplot(fig1)

# Penyebutan kandidat
candidates = ["Anies", "Ganjar", "Prabowo", "Muhaimin", "Mahfud", "Gibran"]
mention_counts = {c: df["cleaned_text"].str.contains(c.lower()).sum() for c in candidates}
mention_series = pd.Series(mention_counts).sort_values(ascending=False)

st.subheader("🗳️ Penyebutan Kandidat")
fig2, ax2 = plt.subplots()
bars2 = mention_series.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Jumlah Penyebutan")

# Tambahkan angka di atas bar
for p in bars2.patches:
    ax2.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2, p.get_height()),
                 ha='center', va='bottom', fontsize=9)

st.pyplot(fig2)

# Distribusi label
st.subheader("🏷️ Distribusi Label (type)")
st.write(df["type"].value_counts())

st.subheader("📌 Distribusi Kategori (tcode)")
st.write(df["tcode"].value_counts())
