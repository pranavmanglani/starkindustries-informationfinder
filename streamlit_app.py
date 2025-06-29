import streamlit as st
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import base64

ua = UserAgent()

# === Utility Functions ===
def search_web(query, num_results=5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=num_results)
        return [res["href"] for res in results]

def fetch_and_parse(url):
    try:
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text() for p in paragraphs)
        return content[:1500] + "..." if len(content) > 1500 else content
    except Exception as e:
        return f"[ERROR fetching {url}] {e}"

def play_audio(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")

# === Streamlit App ===
def main():
    st.set_page_config(page_title="🧊 STARK WEB INTELLIGENCE", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-color: #0e0e0e;
            color: #00ffff;
        }
        .stTextInput>div>div>input {
            background-color: #1e1e1e;
            color: #00ffff;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.title("🧊 STARK WEB INTELLIGENCE ENGINE")
    st.subheader("STARK INDUSTRIES - WEB INTELLIGENCE SYSTEM")

    query = st.text_input("Enter your query:", "")

    if st.button("🔍 Launch J.A.R.V.I.S. Scan"):
        st.info(f"Scanning the web for: **{query}**")
        urls = search_web(query)
        for i, url in enumerate(urls, 1):
            st.markdown(f"### {i}. [{url}]({url})")
            with st.spinner("Fetching content..."):
                content = fetch_and_parse(url)
                st.write(content)
                st.markdown("---")

    # Optionally play sound on load
    if "played" not in st.session_state:
        try:
            play_audio("stark_startup.mp3")
        except Exception as e:
            st.warning(f"Audio Error: {e}")
        st.session_state.played = True

if __name__ == "__main__":
    main()
