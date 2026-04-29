#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime

BASE_URL = "https://www.coastalcashoffer.com"

CITY_SLUGS = [
    "irvine","anaheim","santa-ana","huntington-beach","newport-beach",
    "mission-viejo","laguna-hills","laguna-niguel","lake-forest",
    "san-clemente","san-juan-capistrano","aliso-viejo","costa-mesa",
    "tustin","fountain-valley","garden-grove","fullerton","orange",
    "yorba-linda","dana-point","laguna-beach","brea","placentia",
    "buena-park","westminster","seal-beach",
    "san-diego","chula-vista","oceanside","escondido","el-cajon",
    "vista","carlsbad","san-marcos","santee","la-mesa","poway",
    "long-beach","torrance","pasadena","burbank","glendale","whittier","downey"
]

def generate_sitemap():
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")
    urls.append(f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""")
    urls.append(f"""  <url>
    <loc>{BASE_URL}/blog/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>""")
    for slug in CITY_SLUGS:
        city_file = Path(f"{slug}/index.html")
        if city_file.exists():
            mod_date = datetime.fromtimestamp(city_file.stat().st_mtime).strftime("%Y-%m-%d")
            urls.append(f"""  <url>
    <loc>{BASE_URL}/{slug}/</loc>
    <lastmod>{mod_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>""")
    blog_dir = Path("blog")
    if blog_dir.exists():
        for post_dir in sorted(blog_dir.iterdir()):
            if post_dir.is_dir() and (post_dir / "index.html").exists():
                mod_date = datetime.fromtimestamp((post_dir/"index.html").stat().st_mtime).strftime("%Y-%m-%d")
                urls.append(f"""  <url>
    <loc>{BASE_URL}/blog/{post_dir.name}/</loc>
    <lastmod>{mod_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
    with open("sitemap.xml","w") as f:
        f.write(sitemap)
    print(f"Sitemap: {len(urls)} URLs")

if __name__ == "__main__":
    generate_sitemap()
