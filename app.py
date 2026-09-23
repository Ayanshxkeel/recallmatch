"""Search official Canadian recall notices using TF-IDF text similarity."""
from io import BytesIO
import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_URL = "https://recalls-rappels.canada.ca/sites/default/files/opendata-donneesouvertes/HCRSAMOpenData.csv"
REQUIRED = ["Title", "Product", "URL", "Last updated"]

@st.cache_data(ttl=86400, show_spinner="Loading official recall data...")
def load_recalls():
    response = requests.get(DATA_URL, timeout=30)
    response.raise_for_status()
    data = pd.read_csv(BytesIO(response.content), low_memory=False)
    return data.dropna(subset=["Title", "URL"])

def find_matches(data, query, limit=8):
    text = (data["Product"].fillna("") + " " + data["Title"].fillna("")).tolist()
    model = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    matrix = model.fit_transform(text + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = scores.argsort()[::-1][:limit]
    return [(data.iloc[i], float(scores[i])) for i in ranked if scores[i] > 0]

st.set_page_config(page_title="RecallMatch", page_icon="🔎", layout="wide")
st.title("RecallMatch")
st.caption("Find potentially relevant Canadian recall notices. Always check the official notice before acting.")
query = st.text_input("What product are you checking?", placeholder="e.g. portable Bluetooth speaker")
try:
    recalls = load_recalls()
    st.caption(f"Source: Health Canada open data · {len(recalls):,} notices loaded · newest update: {recalls['Last updated'].max()}")
    if query.strip():
        results = find_matches(recalls, query.strip())
        if not results:
            st.info("No strong text matches. Try a brand, product type, or model number. This does not prove a product is safe.")
        for row, score in results:
            with st.container(border=True):
                st.subheader(str(row['Title']))
                st.write(f"Product: {row.get('Product', 'Unknown')} · Updated: {row.get('Last updated', 'Unknown')}")
                st.progress(min(score, 1.0), text=f"Text similarity: {score:.0%}")
                st.link_button("Read official notice", str(row['URL']))
    else:
        st.info("Enter a product name to search the latest downloaded recall file.")
except (requests.RequestException, ValueError) as error:
    st.error(f"Could not load the official data: {error}")
st.markdown("[Official data source](https://open.canada.ca/data/en/dataset/d38de914-c94c-429b-8ab1-8776c31643e3)")
