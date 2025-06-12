import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from io import BytesIO

# Optional: BERTopic
try:
    from bertopic import BERTopic
    BER_TOPIC_AVAILABLE = True
except ImportError:
    BER_TOPIC_AVAILABLE = False

st.set_page_config(page_title="Response to Reviewers", layout="wide")

st.title("📝 Response to Reviewers")
st.markdown("This tool helps researchers generate structured and well-formatted responses to peer reviewer comments.")

def cluster_texts(texts, n_clusters=5):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8)
    X = vectorizer.fit_transform(texts)
    km = KMeans(n_clusters=n_clusters, random_state=42)
    km.fit(X)
    top_terms = []
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for i in range(n_clusters):
        cluster_keywords = [terms[ind] for ind in order_centroids[i, :5]]
        top_terms.append(", ".join(cluster_keywords))
    return top_terms

def run_bertopic(texts):
    if not BER_TOPIC_AVAILABLE:
        return "BERTopic not available. Install it with: pip install bertopic", None
    model = BERTopic()
    topics, probs = model.fit_transform(texts)
    topic_df = model.get_topic_info()
    return None, topic_df

query = st.text_input("🔍 Enter your manuscript topic or keywords")

if query and st.button("Run Reviewer Assistance"):
    st.info("Fetching abstracts...")

    docs = [
        "This study proposes a novel response structure to address peer reviewer feedback in structured journals.",
        "The manuscript evaluation emphasizes clarity, grammar, and logical coherence across responses.",
        "Reviewers often seek clarity on the statistical methods used in clinical studies.",
        "Authors must explicitly indicate the changes made to the revised manuscript."
    ]

    st.subheader("📊 Reviewer Topic Clusters (TF-IDF + KMeans)")
    top_terms = cluster_texts(docs)
    for i, terms in enumerate(top_terms):
        st.markdown(f"**Cluster {i+1}**: {terms}")

    st.subheader("📚 Advanced Topic Modeling (BERTopic)")
    err, topic_df = run_bertopic(docs)
    if err:
        st.warning(err)
    else:
        st.dataframe(topic_df)

    if top_terms:
        suggestion = (
            f"While reviewer focus includes terms like **{top_terms[0]}**, "
            f"it is important to address underrepresented aspects more thoroughly."
        )
        st.subheader("🧭 Suggested Reviewer Response Focus")
        st.markdown(suggestion)

st.markdown("---")
st.markdown("Developed by **Abdollah Baghaei Daemei** – [ResearchMate.org](https://www.researchmate.org)")