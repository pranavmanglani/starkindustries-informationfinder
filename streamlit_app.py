import streamlit as st
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import base64
import re
from io import StringIO

ua = UserAgent()

# === Google Search without API ===
def search_web(query, num_results=5):
    headers = {'User-Agent': ua.random}
    params = {'q': query, 'num': num_results}
    response = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        match = re.search(r'/url\?q=(https?://[^&]+)&', href)
        if match:
            link = match.group(1)
            if "google.com" not in link and "webcache" not in link:
                links.append(link)
        if len(links) >= num_results:
            break

    return links

# === Fetch and parse website content ===
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

# === Audio startup ===
def play_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
    except Exception as e:
        st.warning(f"Audio Error: {e}")

# === Streamlit App ===
def main():
    st.set_page_config(page_title="🧊 STARK WEB INTELLIGENCE", layout="wide")

    # Custom UI theme
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

    # Play startup sound once
    if "played" not in st.session_state:
        play_audio("stark_startup.mp3")
        st.session_state.played = True

    collected_results = StringIO()

    if st.button("🔍 Launch J.A.R.V.I.S. Scan") and query.strip() != "":
        st.info(f"Scanning the web for: **{query}**")
        urls = search_web(query)
        if not urls:
            st.warning("No results found or Google blocked the request.")
        else:
            for i, url in enumerate(urls, 1):
                st.markdown(f"### {i}. [{url}]({url})")
                with st.spinner("Fetching content..."):
                    content = fetch_and_parse(url)
                    st.write(content)
                    st.markdown("---")
                    collected_results.write(f"{i}. {url}\n{content}\n{'='*60}\n\n")

            # Only show download button if there’s content
            if collected_results.tell() > 0:
                st.download_button(
                    label="💾 Download Results as .txt",
                    data=collected_results.getvalue(),
                    file_name="stark_results.txt",
                    mime="text/plain"
                )
    elif query.strip() == "":
        st.warning("Please enter a query to begin the scan.")

if __name__ == "__main__":
    main()
