import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

# Charger le CSV
df = pd.read_csv('pinterest_final_corrigé_complet.csv')

def escape_xml(text):
    """Nettoie le texte pour éviter les erreurs XML (comme le &)"""
    if pd.isna(text):
        return ""
    text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

# Début du fichier RSS
rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>GreenTomorrow Pinterest Feed</title>
  <link>https://greentomorrow2026.blogspot.com</link>
  <description>Automatisation de jardinage bio</description>
  <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
"""

# Ajouter chaque ligne
for _, row in df.iterrows():
    title = escape_xml(row['Title'])
    link = escape_xml(row['Link'])
    description = escape_xml(row['Description'])
    media_url = escape_xml(row['Media URL'])
    board = escape_xml(row['Pinterest board'])

    rss_content += f"""
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <enclosure url="{media_url}" type="image/jpeg" />
    <category>{board}</category>
    <guid isPermaLink="false">{link}</guid>
  </item>"""

rss_content += """
</channel>
</rss>"""

# Sauvegarder
with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(rss_content)
