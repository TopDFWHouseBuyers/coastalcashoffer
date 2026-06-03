#!/usr/bin/env python3
"""
Golden Coast Cash Offer - Blog Index Generator
Auto-scans all blog post folders and rebuilds the blog index page.
Run: python scripts/generate_blog_index.py
"""

import re
from pathlib import Path
from datetime import datetime


def get_post_meta(post_dir: Path) -> dict | None:
    """Extract title and description from a blog post's index.html."""
    index_file = post_dir / "index.html"
    if not index_file.exists():
        return None

    content = index_file.read_text(encoding="utf-8", errors="ignore")

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).strip() if title_match else post_dir.name.replace("-", " ").title()
    title = re.sub(r'\s*[\|·—]\s*Golden Coast Cash Offer.*$', '', title).strip()
    title = re.sub(r'\s*[\|·—]\s*goldencoast.*$', '', title).strip()

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = desc_match.group(1).strip() if desc_match else "Expert guide for Southern California homeowners."

    # Extract H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else title

    # Detect category from slug
    slug = post_dir.name
    if any(w in slug for w in ['foreclosure', 'mortgage', 'pre-foreclosure']):
        category = "Foreclosure"
        cat_color = "#c0392b"
    elif any(w in slug for w in ['divorce', 'separation']):
        category = "Divorce"
        cat_color = "#8e44ad"
    elif any(w in slug for w in ['inherited', 'probate', 'estate']):
        category = "Inheritance"
        cat_color = "#d35400"
    elif any(w in slug for w in ['market', '2026', '2025']):
        category = "Market"
        cat_color = "#27ae60"
    elif any(w in slug for w in ['tenant', 'landlord', 'rental']):
        category = "Landlords"
        cat_color = "#2980b9"
    elif any(w in slug for w in ['sell-my-house-fast', 'we-buy-houses', 'cash-home-buyers']):
        category = "City Guide"
        cat_color = "#0f6b8a"
    else:
        category = "Education"
        cat_color = "#16a085"

    # Get file modified time as publish date
    mod_time = index_file.stat().st_mtime
    pub_date = datetime.fromtimestamp(mod_time).strftime("%B %d, %Y")

    return {
        "slug": slug,
        "title": title,
        "h1": h1,
        "description": description,
        "category": category,
        "cat_color": cat_color,
        "pub_date": pub_date,
        "mod_time": mod_time,
    }


def build_post_card(post: dict) -> str:
    return f'''    <article class="post-card">
      <div class="post-meta">
        <span class="post-cat" style="background:{post['cat_color']}15;color:{post['cat_color']};border-color:{post['cat_color']}40">{post['category']}</span>
        <span class="post-date">{post['pub_date']}</span>
      </div>
      <h2 class="post-title"><a href="/blog/{post['slug']}/">{post['title']}</a></h2>
      <p class="post-excerpt">{post['description'][:160]}</p>
      <a href="/blog/{post['slug']}/" class="post-read-more">Read Article →</a>
    </article>'''


def build_blog_index(posts: list) -> str:
    year = datetime.now().year
    post_cards = "\n".join([build_post_card(p) for p in posts])
    total = len(posts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog - Golden Coast Cash Offer | Southern California Home Seller Resources</title>
<meta name="description" content="Expert guides for Southern California homeowners - how to sell fast, avoid foreclosure, handle inherited properties, divorce sales, and more.">
<link rel="canonical" href="https://www.goldencoastcashoffer.com/blog/">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QW7L1QHYFR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-QW7L1QHYFR');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "wmyw873b7e");
</script>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Nunito:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#fdfaf5;color:#2a2018;font-family:'Nunito',sans-serif;font-weight:300}}
.site-nav{{background:#0f4a63;padding:14px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid #e8823a;position:sticky;top:0;z-index:100}}
.nav-logo{{color:#f8d264;font-family:'Cormorant Garamond',serif;font-weight:700;font-size:20px;text-decoration:none}}
.nav-links{{display:flex;align-items:center;gap:20px}}
.nav-links a{{color:rgba(255,255,255,0.7);font-size:12px;font-weight:600;text-decoration:none;text-transform:uppercase;letter-spacing:0.05em}}
.nav-cta{{background:#e8823a;color:#fff !important;padding:9px 18px;border-radius:20px}}
.blog-hero{{background:linear-gradient(160deg,#0f4a63,#1a6b8a);padding:56px 40px;text-align:center;position:relative;overflow:hidden}}
.blog-hero::before{{content:'';position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=60') center/cover;opacity:0.1}}
.blog-hero-inner{{position:relative;z-index:1}}
.blog-hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,4vw,48px);color:#fff;font-weight:700;margin-bottom:12px}}
.blog-hero p{{font-size:15px;color:rgba(255,255,255,0.7);max-width:600px;margin:0 auto 20px}}
.blog-hero .count{{font-size:12px;color:#f8d264;font-weight:600;letter-spacing:0.1em;text-transform:uppercase}}
.blog-wrap{{max-width:1100px;margin:0 auto;padding:48px 24px}}
.posts-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
@media(max-width:900px){{.posts-grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:600px){{.posts-grid{{grid-template-columns:1fr}}}}
.post-card{{background:#fff;border:1px solid #ddd5c0;border-radius:8px;padding:24px;transition:transform .15s,box-shadow .15s;display:flex;flex-direction:column}}
.post-card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(15,74,99,0.1)}}
.post-meta{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
.post-cat{{font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;padding:3px 10px;border-radius:20px;border:1px solid}}
.post-date{{font-size:11px;color:#9a8a72}}
.post-title{{font-family:'Cormorant Garamond',serif;font-size:18px;font-weight:700;color:#2a2018;line-height:1.3;margin-bottom:10px}}
.post-title a{{color:inherit;text-decoration:none}}
.post-title a:hover{{color:#e8823a}}
.post-excerpt{{font-size:13px;color:#7a6a52;line-height:1.7;margin-bottom:16px;flex:1}}
.post-read-more{{font-size:12px;font-weight:700;color:#e8823a;text-decoration:none;letter-spacing:0.05em;text-transform:uppercase;margin-top:auto}}
.cta-band{{background:linear-gradient(135deg,#0f4a63,#1a6b8a);padding:48px 24px;text-align:center;margin-top:48px;border-radius:12px}}
.cta-band h2{{font-family:'Cormorant Garamond',serif;font-size:28px;color:#fff;margin-bottom:12px}}
.cta-band p{{color:rgba(255,255,255,0.7);font-size:15px;margin-bottom:24px}}
.cta-band a{{display:inline-block;background:#e8823a;color:#fff;padding:14px 32px;font-weight:700;font-size:13px;text-decoration:none;border-radius:20px}}
footer{{background:#0f4a63;color:rgba(255,255,255,0.4);text-align:center;padding:24px;font-size:11px;border-top:3px solid #e8823a}}
footer a{{color:#f8d264;text-decoration:none}}
</style>
</head>
<body>

<nav class="site-nav">
  <a href="/" class="nav-logo">Golden Coast Cash Offer</a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="tel:9492805139">949-280-5139</a>
    <a href="/#offer" class="nav-cta">Get Cash Offer</a>
  </div>
</nav>

<div class="blog-hero">
  <div class="blog-hero-inner">
    <h1>🌊 SoCal Seller Resources</h1>
    <p>Expert guides for Orange County, San Diego, LA, and Ventura County homeowners navigating every situation.</p>
    <div class="count">{total} Articles · Updated Regularly</div>
  </div>
</div>

<div class="blog-wrap">
  <div class="posts-grid">
{post_cards}
  </div>

  <div class="cta-band">
    <h2>Ready to Sell Your SoCal Home?</h2>
    <p>Get a fair cash offer in 24 hours. No fees, no repairs, no commissions. Close in as few as 7 days.</p>
    <a href="/#offer">Get My Free Cash Offer 🌊</a>
  </div>
</div>

<footer>
  © {year} Golden Coast Cash Offer · <a href="/">goldencoastcashoffer.com</a> · 949-280-5139<br>
  Serving Orange County, San Diego, Los Angeles, Ventura County and all of Southern California
</footer>

</body>
</html>"""


def main():
    blog_dir = Path("blog")
    if not blog_dir.exists():
        print("No blog directory found.")
        return

    # Get all post directories sorted by modified time (newest first)
    post_dirs = sorted(
        [d for d in blog_dir.iterdir() if d.is_dir() and (d / "index.html").exists()],
        key=lambda d: (d / "index.html").stat().st_mtime,
        reverse=True
    )

    posts = []
    for post_dir in post_dirs:
        meta = get_post_meta(post_dir)
        if meta:
            posts.append(meta)

    print(f"Found {len(posts)} blog posts")

    html = build_blog_index(posts)
    output_file = blog_dir / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Blog index rebuilt: {output_file}")
    print(f"Total posts shown: {len(posts)}")


if __name__ == "__main__":
    main()
