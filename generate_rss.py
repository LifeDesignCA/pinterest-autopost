import pandas as pd
from datetime import datetime

# Charger le CSV corrigé
df = pd.read_csv('pinterest_final_corrigé_complet.csv')

# Début du fichier RSS
rss_content = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>GreenTomorrow Pinterest Feed</title>
  <link>https://greentomorrow2026.blogspot.com</link>
  <description>Automatisation de jardinage bio</description>
  <lastBuildDate>{}</lastBuildDate>
""".format(datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))

# Ajouter chaque ligne du CSV comme un item RSS
for _, row in df.iterrows():
    rss_content += f"""
  <item>
    <title>{row['Title']}</title>
    <link>{row['Link']}</link>
    <description>{row['Description']}</description>
    <enclosure url="{row['Media URL']}" type="image/jpeg" />
    <category>{row['Pinterest board']}</category>
    <guid isPermaLink="false">{row['Link']}</guid>
  </item>"""

# Fin du fichier
rss_content += """
</channel>
</rss>"""

# Sauvegarder le fichier feed.xml
with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write(rss_content)
