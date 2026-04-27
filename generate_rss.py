import pandas as pd
from datetime import datetime
import html
import urllib.parse
import re

def clean_text_strict(text):
    if pd.isna(text): return ""
    # 1. Supprime les caractères spéciaux et emojis (garde lettres, chiffres et ponctuation simple)
    text = re.sub(r'[^\x00-\x7F]+', ' ', str(text))
    # 2. Nettoyage HTML pour le XML
    return html.escape(text.strip())

def get_safe_image_url(row):
    url = str(row['Media URL']).strip()
    # Si l'image est manquante ou invalide
    if not url or url == "" or "nan" in url.lower() or "manquante" in url.lower():
        # Recherche Unsplash : on ajoute "-person" et "nature" pour éviter les humains
        topic = f"{row['Title']} garden vegetable plant no people"
        query = urllib.parse.quote(topic)
        # On utilise un ID de collection nature pour plus de sécurité
        return f"https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&q=80&w=800&sig={urllib.parse.quote(str(row['Title']))}"
    return url

# Charger ton CSV
df = pd.read_csv('pinterest_final_corrigé_complet.csv')

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>GreenTomorrow Feed</title>
  <link>https://greentomorrow2026.blogspot.com</link>
  <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
"""

for _, row in df.iterrows():
    img_url = get_safe_image_url(row)
    
    rss += f"""
  <item>
    <title>{clean_text_strict(row['Title'])}</title>
    <link>{clean_text_strict(row['Link'])}</link>
    <description>{clean_text_strict(row['Description'])}</description>
    <enclosure url="{clean_text_strict(img_url)}" type="image/jpeg" />
    <category>{clean_text_strict(row['Pinterest board'])}</category>
    <guid isPermaLink="false">{clean_text_strict(row['Link'])}-{datetime.now().day}</guid>
  </item>"""

rss += "</channel></rss>"

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(rss)
