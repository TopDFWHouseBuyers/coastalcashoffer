#!/usr/bin/env python3
"""
Coastal Cash Offer - City Landing Pages Generator
Generates 40+ city-specific SEO pages for Southern California
Run once: python scripts/generate_cities.py
"""

import os
import json
import re
import anthropic
from datetime import datetime
from pathlib import Path

CITIES = [
    # Orange County - Primary focus
    {"name": "Irvine", "county": "Orange", "zip": "92618", "region": "Orange County", "notes": "one of the most affluent planned communities in the US with high home values"},
    {"name": "Anaheim", "county": "Orange", "zip": "92801", "region": "Orange County", "notes": "home of Disneyland, diverse city with a mix of older homes and newer developments"},
    {"name": "Santa Ana", "county": "Orange", "zip": "92701", "region": "Orange County", "notes": "Orange County seat, large Hispanic community, many older homes needing updates"},
    {"name": "Huntington Beach", "county": "Orange", "zip": "92648", "region": "Orange County", "notes": "Surf City USA, beachfront properties, strong demand for coastal homes"},
    {"name": "Newport Beach", "county": "Orange", "zip": "92660", "region": "Orange County", "notes": "ultra-premium coastal city, among California's most expensive real estate markets"},
    {"name": "Mission Viejo", "county": "Orange", "zip": "92691", "region": "Orange County", "notes": "master-planned community, predominantly single-family homes, strong HOA culture"},
    {"name": "Laguna Hills", "county": "Orange", "zip": "92653", "region": "Orange County", "notes": "quiet suburban community in south OC with many 1980s-era homes"},
    {"name": "Laguna Niguel", "county": "Orange", "zip": "92677", "region": "Orange County", "notes": "upscale coastal community near Laguna Beach with premium home values"},
    {"name": "Lake Forest", "county": "Orange", "zip": "92630", "region": "Orange County", "notes": "inland OC community with many 1970s-80s homes and strong family neighborhoods"},
    {"name": "San Clemente", "county": "Orange", "zip": "92672", "region": "Orange County", "notes": "Spanish Village by the Sea, coastal community near Camp Pendleton"},
    {"name": "San Juan Capistrano", "county": "Orange", "zip": "92675", "region": "Orange County", "notes": "historic mission city, equestrian community, older Spanish-style homes"},
    {"name": "Aliso Viejo", "county": "Orange", "zip": "92656", "region": "Orange County", "notes": "newer planned community, one of the newest cities in OC, modern developments"},
    {"name": "Costa Mesa", "county": "Orange", "zip": "92626", "region": "Orange County", "notes": "arts and shopping hub near Newport Beach, mix of older homes and new condos"},
    {"name": "Tustin", "county": "Orange", "zip": "92780", "region": "Orange County", "notes": "mix of historic old town and newer Tustin Ranch developments, great location"},
    {"name": "Fountain Valley", "county": "Orange", "zip": "92708", "region": "Orange County", "notes": "centrally located OC city, many 1960s-70s ranch homes, Korean community"},
    {"name": "Garden Grove", "county": "Orange", "zip": "92840", "region": "Orange County", "notes": "diverse OC city, large Vietnamese community, many older affordable homes"},
    {"name": "Fullerton", "county": "Orange", "zip": "92832", "region": "Orange County", "notes": "college town with Cal State Fullerton, historic downtown, diverse housing stock"},
    {"name": "Orange", "county": "Orange", "zip": "92868", "region": "Orange County", "notes": "historic Old Towne Orange, antique district, mix of Victorian and modern homes"},
    {"name": "Yorba Linda", "county": "Orange", "zip": "92886", "region": "Orange County", "notes": "birthplace of Nixon, affluent east OC community, larger lots and equestrian areas"},
    {"name": "Dana Point", "county": "Orange", "zip": "92629", "region": "Orange County", "notes": "harbor city, whale watching capital, coastal premium properties"},
    {"name": "Laguna Beach", "county": "Orange", "zip": "92651", "region": "Orange County", "notes": "premier arts colony, dramatic coastal bluffs, among most expensive in SoCal"},
    {"name": "Brea", "county": "Orange", "zip": "92821", "region": "Orange County", "notes": "north OC city, award-winning downtown, newer planned neighborhoods"},
    {"name": "Placentia", "county": "Orange", "zip": "92870", "region": "Orange County", "notes": "north OC suburban community, older affordable housing, family-oriented"},
    {"name": "Buena Park", "county": "Orange", "zip": "90620", "region": "Orange County", "notes": "home of Knott's Berry Farm, diverse older community, many mid-century homes"},
    {"name": "Westminster", "county": "Orange", "zip": "92683", "region": "Orange County", "notes": "Little Saigon, large Vietnamese community, affordable older housing"},
    {"name": "Seal Beach", "county": "Orange", "zip": "90740", "region": "Orange County", "notes": "small beach town, Leisure World senior community, charming coastal village"},
    # San Diego
    {"name": "San Diego", "county": "San Diego", "zip": "92101", "region": "San Diego County", "notes": "California's second-largest city, strong military presence, diverse neighborhoods"},
    {"name": "Chula Vista", "county": "San Diego", "zip": "91910", "region": "San Diego County", "notes": "second-largest SD city, diverse community, mix of older south bay and newer eastern developments"},
    {"name": "Oceanside", "county": "San Diego", "zip": "92054", "region": "San Diego County", "notes": "military city near Camp Pendleton, beach access, diverse housing"},
    {"name": "Escondido", "county": "San Diego", "zip": "92025", "region": "San Diego County", "notes": "inland north SD county, wine country, older affordable housing"},
    {"name": "El Cajon", "county": "San Diego", "zip": "92020", "region": "San Diego County", "notes": "east SD county, large Middle Eastern community, affordable older homes"},
    {"name": "Vista", "county": "San Diego", "zip": "92083", "region": "San Diego County", "notes": "north SD county, avocado farming history, affordable suburban community"},
    {"name": "Carlsbad", "county": "San Diego", "zip": "92008", "region": "San Diego County", "notes": "upscale coastal north county, LEGOLAND, premium beachside properties"},
    {"name": "San Marcos", "county": "San Diego", "zip": "92069", "region": "San Diego County", "notes": "inland north county, Cal State San Marcos, growing community"},
    {"name": "Santee", "county": "San Diego", "zip": "92071", "region": "San Diego County", "notes": "east county suburban community, affordable family neighborhoods"},
    {"name": "La Mesa", "county": "San Diego", "zip": "91941", "region": "San Diego County", "notes": "Jewel of the Hills, charming village, close to downtown SD"},
    {"name": "Poway", "county": "San Diego", "zip": "92064", "region": "San Diego County", "notes": "City in the Country, large lots, excellent schools, affluent suburban"},
    # Los Angeles
    {"name": "Long Beach", "county": "Los Angeles", "zip": "90802", "region": "Los Angeles County", "notes": "second-largest LA city, major port, diverse neighborhoods from historic to beachfront"},
    {"name": "Torrance", "county": "Los Angeles", "zip": "90501", "region": "Los Angeles County", "notes": "South Bay community, large Japanese-American community, strong auto industry presence"},
    {"name": "Pasadena", "county": "Los Angeles", "zip": "91101", "region": "Los Angeles County", "notes": "Rose Bowl city, Caltech, beautiful craftsman homes, affluent historic community"},
    {"name": "Burbank", "county": "Los Angeles", "zip": "91502", "region": "Los Angeles County", "notes": "Media capital, Disney and Warner Bros, strong entertainment industry"},
    {"name": "Glendale", "county": "Los Angeles", "zip": "91201", "region": "Los Angeles County", "notes": "large Armenian-American community, diverse city north of LA, hillside properties"},
    {"name": "Whittier", "county": "Los Angeles", "zip": "90601", "region": "Los Angeles County", "notes": "birthplace of Nixon, historic Uptown, affordable southeast LA county"},
    {"name": "Downey", "county": "Los Angeles", "zip": "90241", "region": "Los Angeles County", "notes": "southeast LA county, NASA history, diverse working-class community"},
]


def generate_city_content(city: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are an expert real estate SEO content writer for Coastal Cash Offer, a cash home buying company in Southern California.

COMPANY INFO:
- Name: Coastal Cash Offer
- Phone: 949-280-5139
- Website: https://www.coastalcashoffer.com

ASSIGNMENT: Write city-specific landing page content for {city['name']}, {city['county']} County, CA.

CITY DETAILS:
- City: {city['name']}, {city['county']} County, CA {city['zip']}
- Region: {city['region']}
- Local context: {city['notes']}

TARGET KEYWORD: "sell my house fast {city['name']} CA"

REQUIREMENTS:
1. Write 600-800 words of unique, helpful content
2. Include local {city['name']} context and neighborhoods
3. 3 H2 sections with natural subheadings
4. 2 CTA sections mentioning 949-280-5139
5. Warm, California-casual tone
6. Meta title under 60 chars
7. Meta description under 160 chars
8. Include California-specific considerations (tenant laws, high values, escrow, etc.)

Return ONLY valid JSON (no markdown, no backticks):
{{
  "meta_title": "...",
  "meta_description": "...",
  "h1": "We Buy Houses in {city['name']}, CA - Fast Cash Offers",
  "intro": "...(2-3 sentence intro)...",
  "content_html": "...(HTML using only h2, p, ul, li tags)...",
  "why_sellers_title": "Why {city['name']} Homeowners Choose Us",
  "why_sellers_points": ["...", "...", "...", "..."]
}}"""

    prompt_safe = prompt.encode('ascii', errors='replace').decode('ascii')
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt_safe}]
    )
    raw = message.content[0].text.strip()
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return json.loads(raw)


def build_city_page(content: dict, city: dict) -> str:
    slug = city['name'].lower().replace(' ', '-')
    year = datetime.now().year
    why_points = ''.join([f'<li style="font-size:15px;line-height:1.8;color:#4a3a28;margin:8px 0">{p}</li>' for p in content.get('why_sellers_points', [])])

    # Build city links
    city_links = ''
    for c in CITIES[:20]:
        cs = c['name'].lower().replace(' ', '-')
        active = 'background:#e8823a;color:#fff;border-color:#e8823a;' if c['name'] == city['name'] else ''
        city_links += f'<a href="/{cs}/" style="padding:10px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.8);font-size:11px;font-weight:600;text-decoration:none;text-align:center;border-radius:8px;display:block;transition:all .15s;{active}">{c["name"]}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{content['meta_title']}</title>
<meta name="description" content="{content['meta_description']}">
<link rel="canonical" href="https://www.coastalcashoffer.com/{slug}/">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question","name": "How fast can you buy my house in {city['name']}, CA?","acceptedAnswer": {{"@type": "Answer","text": "We can close in as few as 7 days in {city['name']}. Call us at 949-280-5139 to discuss your timeline."}}}},
    {{"@type": "Question","name": "Do I need to make repairs before selling my {city['name']} home?","acceptedAnswer": {{"@type": "Answer","text": "Never. We buy houses in {city['name']} in any condition - no repairs, no cleaning required."}}}},
    {{"@type": "Question","name": "Are there any fees when selling to Coastal Cash Offer?","acceptedAnswer": {{"@type": "Answer","text": "Zero fees, zero commissions, zero closing costs. What we offer is exactly what you receive."}}}},
    {{"@type": "Question","name": "Do you buy homes with tenants in {city['name']}?","acceptedAnswer": {{"@type": "Answer","text": "Yes. We buy California properties with tenants in place - you don't need to deal with California tenant laws."}}}}
  ]
}}
</script>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Nunito:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--ocean:#0f4a63;--ocean2:#1a6b8a;--sunrise:#e8823a;--sand:#fdfaf5;--gold:#f8d264}}
body{{background:var(--sand);color:#2a2018;font-family:'Nunito',sans-serif;font-weight:300}}
.site-nav{{background:var(--ocean);padding:14px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid var(--sunrise);position:sticky;top:0;z-index:100}}
.nav-logo{{color:var(--gold);font-family:'Cormorant Garamond',serif;font-weight:700;font-size:20px;text-decoration:none}}
.nav-links{{display:flex;align-items:center;gap:20px}}
.nav-links a{{color:rgba(255,255,255,0.7);font-size:12px;font-weight:600;text-decoration:none;text-transform:uppercase;letter-spacing:0.05em}}
.nav-cta{{background:var(--sunrise);color:#fff !important;padding:9px 18px;border-radius:20px}}
.hero{{background:linear-gradient(160deg,var(--ocean) 0%,var(--ocean2) 100%);padding:56px 40px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=60') center/cover;opacity:0.1}}
.hero-inner{{position:relative;z-index:1;max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 400px;gap:48px;align-items:center}}
@media(max-width:900px){{.hero-inner{{grid-template-columns:1fr}}}}
.hero-badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(232,130,58,0.2);border:1px solid rgba(232,130,58,0.4);padding:5px 14px;border-radius:20px;font-size:10px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--gold);margin-bottom:16px}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(30px,4vw,50px);color:#fff;font-weight:700;line-height:1.1;margin-bottom:16px}}
.hero h1 em{{font-style:italic;color:var(--gold);font-weight:300}}
.hero-sub{{font-size:15px;color:rgba(255,255,255,0.75);line-height:1.7;margin-bottom:24px}}
.badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{display:flex;align-items:center;gap:5px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);padding:6px 12px;border-radius:16px;font-size:11px;color:rgba(255,255,255,0.85);font-weight:500}}
.badge::before{{content:'✓';color:var(--gold);font-weight:700}}
.hero-form{{background:rgba(255,255,255,0.97);border-radius:16px;border-top:4px solid var(--sunrise);padding:28px 24px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
.form-headline{{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:700;color:var(--ocean);margin-bottom:4px}}
.form-sub{{font-size:12px;color:#7a6a52;margin-bottom:18px}}
.field{{margin-bottom:12px}}
.field label{{display:block;font-size:10px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#7a6a52;margin-bottom:4px}}
.field input,.field select{{width:100%;padding:10px 14px;border:1.5px solid #ddd5c0;border-radius:10px;font-family:'Nunito',sans-serif;font-size:13px;outline:none;transition:border-color .15s}}
.field input:focus,.field select:focus{{border-color:var(--ocean2)}}
.field-row{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.submit-btn{{width:100%;padding:14px;background:linear-gradient(135deg,var(--sunrise),#f0a060);border:none;color:#fff;font-family:'Nunito',sans-serif;font-weight:700;font-size:13px;cursor:pointer;border-radius:10px;transition:all .2s;margin-top:4px}}
.submit-btn:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(232,130,58,0.4)}}
.guarantee{{text-align:center;font-size:10px;color:#7a6a52;margin-top:10px}}
.form-success{{display:none;text-align:center;padding:24px}}
.form-success .wave{{font-size:40px;margin-bottom:10px}}
.form-success h3{{font-family:'Cormorant Garamond',serif;font-size:20px;color:var(--ocean);margin-bottom:8px}}
.content-wrap{{max-width:1100px;margin:0 auto;padding:48px 24px;display:grid;grid-template-columns:1fr 300px;gap:48px}}
@media(max-width:768px){{.content-wrap{{grid-template-columns:1fr}}}}
.main h2{{font-family:'Cormorant Garamond',serif;font-size:26px;color:var(--ocean);margin:32px 0 12px}}
.main p{{font-size:15px;line-height:1.9;color:#4a3a28;margin-bottom:14px}}
.main ul{{padding-left:20px;margin-bottom:14px}}
.main li{{font-size:15px;line-height:1.8;color:#4a3a28;margin:6px 0}}
.why-box{{background:var(--ocean);padding:28px;margin:28px 0;border-radius:12px}}
.why-box h2{{font-family:'Cormorant Garamond',serif;font-size:20px;color:#fff;margin-bottom:16px}}
.why-box ul{{list-style:none;padding:0}}
.why-box li{{padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.1);color:rgba(255,255,255,0.8);font-size:14px;display:flex;gap:8px}}
.why-box li::before{{content:'✓';color:var(--gold);font-weight:700;flex-shrink:0}}
.cta-box{{background:#f5e6c8;border-left:4px solid var(--sunrise);padding:20px 24px;margin:28px 0;border-radius:0 12px 12px 0}}
.cta-box h3{{font-size:15px;font-weight:700;color:var(--ocean);margin-bottom:6px}}
.cta-box p{{font-size:13px;color:#7a6a52;margin-bottom:14px;line-height:1.6}}
.cta-box a{{display:inline-block;background:var(--ocean);color:#fff;padding:10px 22px;font-weight:700;font-size:12px;text-decoration:none;border-radius:20px}}
.sidebar-card{{background:#fff;border:1px solid #ddd5c0;border-top:3px solid var(--sunrise);padding:20px;margin-bottom:16px;border-radius:0 0 12px 12px}}
.sidebar-card h3{{font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:700;color:var(--ocean);margin-bottom:6px}}
.sidebar-phone{{font-size:20px;font-weight:700;color:var(--sunrise);text-decoration:none;display:block;margin-bottom:10px}}
.s-btn{{display:block;padding:11px;font-weight:700;font-size:11px;text-decoration:none;border-radius:20px;text-align:center;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.06em}}
.s-btn.orange{{background:var(--sunrise);color:#fff}}
.s-btn.dark{{background:var(--ocean);color:#fff}}
.cities-strip{{background:linear-gradient(160deg,var(--ocean),var(--ocean2));padding:40px;position:relative;overflow:hidden}}
.cities-strip h2{{font-family:'Cormorant Garamond',serif;font-size:24px;color:#fff;margin-bottom:20px;text-align:center;position:relative;z-index:1}}
.cities-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;max-width:900px;margin:0 auto;position:relative;z-index:1}}
@media(max-width:640px){{.cities-grid{{grid-template-columns:repeat(3,1fr)}}}}
footer{{background:var(--ocean);color:rgba(255,255,255,0.4);text-align:center;padding:24px;font-size:11px;border-top:3px solid var(--sunrise)}}
footer a{{color:var(--gold);text-decoration:none}}
.sticky{{position:fixed;bottom:0;left:0;right:0;background:var(--ocean);border-top:2px solid var(--sunrise);padding:12px 20px;display:none;align-items:center;justify-content:space-between;z-index:200}}
@media(max-width:640px){{.sticky{{display:flex}}}}
.sticky span{{font-size:12px;color:rgba(255,255,255,0.7)}}
.sticky a{{padding:9px 18px;background:var(--sunrise);color:#fff;font-weight:700;font-size:11px;text-decoration:none;border-radius:20px;white-space:nowrap}}
</style>
</head>
<body>

<nav class="site-nav">
  <a href="/" class="nav-logo">Coastal Cash Offer</a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="tel:9492805139">949-280-5139</a>
    <a href="/#offer" class="nav-cta">Get Cash Offer</a>
  </div>
</nav>

<section class="hero">
  <div class="hero-inner">
    <div>
      <div class="hero-badge">🌊 {city['region']} · {city['county']} County, CA</div>
      <h1>{content['h1'].replace('Fast Cash Offers', '<em>Fast Cash Offers</em>')}</h1>
      <p class="hero-sub">No repairs. No agent fees. No commissions. Get a fair cash offer within 24 hours and close on your timeline — as fast as 7 days.</p>
      <div class="badges">
        <div class="badge">No Repairs Needed</div>
        <div class="badge">No Agent Fees</div>
        <div class="badge">Close in 7 Days</div>
        <div class="badge">Any Condition</div>
      </div>
    </div>
    <div class="hero-form">
      <div class="form-headline">Get Your Cash Offer</div>
      <div class="form-sub">{city['name']} homeowners — takes 60 seconds, no obligation</div>
      <form id="city-form" name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" onsubmit="submitForm(event)">
        <input type="hidden" name="form-name" value="contact">
        <input type="hidden" name="bot-field" style="display:none">
        <input type="hidden" name="city" value="{city['name']}">
        <div class="field">
          <label>Your Name *</label>
          <input type="text" id="fname" name="name" placeholder="John Smith" required>
        </div>
        <div class="field">
          <label>Property Address *</label>
          <input type="text" id="address" name="address" placeholder="{city['name']}, CA {city['zip']}" required>
        </div>
        <div class="field-row">
          <div class="field">
            <label>Phone *</label>
            <input type="tel" id="phone" name="phone" placeholder="(949) 555-0000" required>
          </div>
          <div class="field">
            <label>Email</label>
            <input type="email" name="email" placeholder="john@email.com">
          </div>
        </div>
        <div class="field">
          <label>Situation</label>
          <select name="situation">
            <option value="">Select...</option>
            <option>Behind on mortgage / foreclosure</option>
            <option>Inherited property</option>
            <option>Divorce / separation</option>
            <option>Tired landlord / tenants</option>
            <option>Needs major repairs</option>
            <option>Relocating</option>
            <option>Downsizing</option>
            <option>Vacant property</option>
            <option>Just want to sell fast</option>
            <option>Other</option>
          </select>
        </div>
        <button type="submit" class="submit-btn">Get My Cash Offer 🌊</button>
      </form>
      <div class="form-success" id="form-success">
        <div class="wave">🌊</div>
        <h3>Got It!</h3>
        <p>We'll call you within 30 minutes.<br><strong>949-280-5139</strong></p>
      </div>
      <div class="guarantee">100% confidential · No obligation · No spam</div>
    </div>
  </div>
</section>

<div class="content-wrap">
  <div class="main">
    <p style="font-size:16px;line-height:1.9;color:#3a2a18;font-weight:400;margin-bottom:24px">{content['intro']}</p>
    {content['content_html']}
    <div class="why-box">
      <h2>{content['why_sellers_title']}</h2>
      <ul>{why_points}</ul>
    </div>
    <div class="cta-box">
      <h3>Ready to Sell Your {city['name']} Home?</h3>
      <p>Get a fair cash offer within 24 hours. No fees, no repairs, no commissions. Close in as few as 7 days.</p>
      <a href="tel:9492805139">Call 949-280-5139 Now</a>
    </div>
  </div>
  <div>
    <div class="sidebar-card">
      <h3>Get Your Free Cash Offer</h3>
      <p style="font-size:12px;color:#7a6a52;margin-bottom:12px">No fees, no repairs. Close in 7 days or on your schedule.</p>
      <a href="tel:9492805139" class="sidebar-phone">949-280-5139</a>
      <a href="#" onclick="window.scrollTo({{top:0,behavior:'smooth'}});return false" class="s-btn orange">Get Cash Offer 🌊</a>
      <a href="tel:9492805139" class="s-btn dark">Call Now</a>
    </div>
    <div class="sidebar-card">
      <h3>How It Works</h3>
      <p style="font-size:12px;color:#7a6a52;line-height:1.8;margin:0">
        <strong>1.</strong> Tell us about your property<br>
        <strong>2.</strong> Cash offer in 24 hours<br>
        <strong>3.</strong> Choose your closing date<br>
        <strong>4.</strong> Walk away with cash
      </p>
    </div>
  </div>
</div>

<div class="cities-strip">
  <h2>We Buy Houses Across Southern California</h2>
  <div class="cities-grid">
    {city_links}
  </div>
</div>

<footer>
  {year} Coastal Cash Offer · <a href="/">coastalcashoffer.com</a> · 949-280-5139<br>
  Serving {city['name']} and all of Orange County, San Diego, and Los Angeles
</footer>

<div class="sticky">
  <span>Sell your {city['name']} home — cash offer in 24 hrs</span>
  <a href="tel:9492805139">Call Now →</a>
</div>

<script>
async function submitForm(e) {{
  e.preventDefault();
  const form = document.getElementById('city-form');
  const btn = form.querySelector('.submit-btn');
  btn.textContent = 'Submitting...';
  btn.disabled = true;
  try {{
    const formData = new FormData(form);
    await fetch('/', {{method:'POST',headers:{{'Content-Type':'application/x-www-form-urlencoded'}},body:new URLSearchParams(formData).toString()}});
  }} catch(e) {{}}
  form.style.display = 'none';
  document.getElementById('form-success').style.display = 'block';
}}
</script>
</body>
</html>"""


def main():
    print(f"Generating {len(CITIES)} city landing pages")
    for i, city in enumerate(CITIES):
        slug = city['name'].lower().replace(' ', '-')
        output_dir = Path(slug)
        output_file = output_dir / "index.html"
        print(f"  [{i+1}/{len(CITIES)}] Generating {city['name']}...")
        try:
            content = generate_city_content(city)
            html = build_city_page(content, city)
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"    Saved: {output_file}")
        except Exception as e:
            print(f"    Error: {e}")
    print("Done!")


if __name__ == "__main__":
    main()
