import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "llms-txt-generator/1.0"}

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.text
    except:
        return ""

def summarize_page(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.title.string.strip() if soup.title and soup.title.string else "Brak tytułu"
    desc_tag = soup.find("meta", attrs={"name":"description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else "Brak opisu"
    p = ""
    for para in soup.find_all("p"):
        text = para.get_text(strip=True)
        if len(text) > 40:
            p = text
            break
    if not desc and p:
        desc = p[:300].strip()
    return title, desc

st.title("Generator LLMS")
st.write("Wklej URL-e swojej domeny po jednym w linii, a następnie kliknij 'Generuj'.")

urls_text = st.text_area("URL-e", height=200)

if st.button("Generuj LLMS"):
    urls = [line.strip() for line in urls_text.splitlines() if line.strip()]
    if not urls:
        st.warning("Nie podano żadnych URL-i!")
    else:
        content = ["<!-- llms.txt generated automatically -->\n"]
        for url in urls:
            html = fetch(
