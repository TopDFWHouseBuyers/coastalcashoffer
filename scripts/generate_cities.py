#!/usr/bin/env python3
"""
Golden Coast Cash Offer — City Landing Page Generator (COMPLETE)
Full 90-city list: Ventura · LA · OC · Inland Empire · San Diego
Run: python scripts/generate_cities.py
"""

import os
import json
import re
import anthropic
from datetime import datetime
from pathlib import Path

CITIES = [
    # ── Ventura County ─────────────────────────────────────────────────────
    {"name": "Ventura",               "county": "Ventura",        "zip": "93001", "region": "Ventura County",    "notes": "coastal city on the Pacific, historic downtown, gateway to Channel Islands"},
    {"name": "Oxnard",                "county": "Ventura",        "zip": "93030", "region": "Ventura County",    "notes": "largest city in Ventura County, beachfront community, large Latino population"},
    {"name": "Port Hueneme",          "county": "Ventura",        "zip": "93041", "region": "Ventura County",    "notes": "small beach city, naval base, affordable coastal housing"},
    {"name": "Camarillo",             "county": "Ventura",        "zip": "93010", "region": "Ventura County",    "notes": "affluent inland Ventura city, premium outlets, upscale planned communities"},
    {"name": "Thousand Oaks",         "county": "Ventura",        "zip": "91360", "region": "Ventura County",    "notes": "one of safest US cities, large lots, highly rated schools, tech corridor"},
    {"name": "Simi Valley",           "county": "Ventura",        "zip": "93065", "region": "Ventura County",    "notes": "suburban community, Reagan Presidential Library, affordable family neighborhoods"},
    {"name": "Ojai",                  "county": "Ventura",        "zip": "93023", "region": "Ventura County",    "notes": "artsy mountain valley retreat, wellness tourism, unique hillside properties"},

    # ── Los Angeles County ─────────────────────────────────────────────────
    {"name": "Malibu",                "county": "Los Angeles",    "zip": "90265", "region": "Los Angeles County", "notes": "ultra-premium beachfront estates, celebrity enclave, dramatic coastal bluffs"},
    {"name": "Santa Monica",          "county": "Los Angeles",    "zip": "90401", "region": "Los Angeles County", "notes": "iconic pier city, high-end coastal real estate, tech and entertainment hub"},
    {"name": "Los Angeles",           "county": "Los Angeles",    "zip": "90001", "region": "Los Angeles County", "notes": "second-largest US city, incredibly diverse neighborhoods, strong investor demand"},
    {"name": "Beverly Hills",         "county": "Los Angeles",    "zip": "90210", "region": "Los Angeles County", "notes": "world-famous luxury enclave, ultra-premium estates, global buyer demand"},
    {"name": "West Hollywood",        "county": "Los Angeles",    "zip": "90046", "region": "Los Angeles County", "notes": "vibrant nightlife and arts district, high condo density, strong rental market"},
    {"name": "Culver City",           "county": "Los Angeles",    "zip": "90232", "region": "Los Angeles County", "notes": "tech and entertainment hub, Amazon Studios, rapidly appreciating home values"},
    {"name": "Inglewood",             "county": "Los Angeles",    "zip": "90301", "region": "Los Angeles County", "notes": "SoFi Stadium city, rapidly gentrifying, strong investor demand"},
    {"name": "El Segundo",            "county": "Los Angeles",    "zip": "90245", "region": "Los Angeles County", "notes": "aerospace hub near LAX, tight-knit beach community, strong tech employment"},
    {"name": "Hawthorne",             "county": "Los Angeles",    "zip": "90250", "region": "Los Angeles County", "notes": "SpaceX headquarters, LAX adjacent, rapidly developing South Bay city"},
    {"name": "Gardena",               "county": "Los Angeles",    "zip": "90247", "region": "Los Angeles County", "notes": "diverse South Bay community, large Japanese-American and Latino population"},
    {"name": "Compton",               "county": "Los Angeles",    "zip": "90220", "region": "Los Angeles County", "notes": "historically significant city in south LA, strong investor interest, affordable entry points"},
    {"name": "Carson",                "county": "Los Angeles",    "zip": "90745", "region": "Los Angeles County", "notes": "South Bay community, Cal State Dominguez Hills, diverse working-class neighborhoods"},
    {"name": "Manhattan Beach",       "county": "Los Angeles",    "zip": "90266", "region": "Los Angeles County", "notes": "premier South Bay beach city, top schools, among priciest SoCal coastal markets"},
    {"name": "Hermosa Beach",         "county": "Los Angeles",    "zip": "90254", "region": "Los Angeles County", "notes": "vibrant beach community, walkable Pier Ave, strong vacation rental demand"},
    {"name": "Redondo Beach",         "county": "Los Angeles",    "zip": "90277", "region": "Los Angeles County", "notes": "South Bay beach city, harbor area, mix of condos and single-family homes"},
    {"name": "Torrance",              "county": "Los Angeles",    "zip": "90501", "region": "Los Angeles County", "notes": "South Bay community, large Japanese-American community, strong auto industry presence"},
    {"name": "Long Beach",            "county": "Los Angeles",    "zip": "90802", "region": "Los Angeles County", "notes": "second-largest LA city, major port, diverse neighborhoods from historic to beachfront"},
    {"name": "Bellflower",            "county": "Los Angeles",    "zip": "90706", "region": "Los Angeles County", "notes": "southeast LA county suburb, affordable housing, strong working-class community"},
    {"name": "Paramount",             "county": "Los Angeles",    "zip": "90723", "region": "Los Angeles County", "notes": "small southeast LA county city, industrial and residential mix, affordable homes"},
    {"name": "Downey",                "county": "Los Angeles",    "zip": "90241", "region": "Los Angeles County", "notes": "southeast LA county, NASA history, diverse working-class community"},
    {"name": "Norwalk",               "county": "Los Angeles",    "zip": "90650", "region": "Los Angeles County", "notes": "southeast LA county, Cerritos border, large Hispanic community, older homes"},
    {"name": "Cerritos",              "county": "Los Angeles",    "zip": "90703", "region": "Los Angeles County", "notes": "highly rated schools, diverse affluent suburb, strong Korean and Filipino community"},
    {"name": "Lakewood",              "county": "Los Angeles",    "zip": "90712", "region": "Los Angeles County", "notes": "one of first planned communities in US, post-WWII suburb, strong civic identity"},
    {"name": "Whittier",              "county": "Los Angeles",    "zip": "90601", "region": "Los Angeles County", "notes": "historic Uptown, birthplace of Nixon, affordable southeast LA county"},
    {"name": "El Monte",              "county": "Los Angeles",    "zip": "91731", "region": "Los Angeles County", "notes": "San Gabriel Valley city, large Latino community, older housing stock with strong demand"},
    {"name": "West Covina",           "county": "Los Angeles",    "zip": "91790", "region": "Los Angeles County", "notes": "San Gabriel Valley suburb, diverse community, mix of ranch homes and newer developments"},
    {"name": "Alhambra",              "county": "Los Angeles",    "zip": "91801", "region": "Los Angeles County", "notes": "San Gabriel Valley, large Chinese-American community, close to downtown LA"},
    {"name": "Monterey Park",         "county": "Los Angeles",    "zip": "91754", "region": "Los Angeles County", "notes": "first suburban Chinatown in the US, dense diverse community, strong Asian-American population"},
    {"name": "Arcadia",               "county": "Los Angeles",    "zip": "91006", "region": "Los Angeles County", "notes": "affluent San Gabriel Valley city, Santa Anita Park, large Chinese-American community"},
    {"name": "Pasadena",              "county": "Los Angeles",    "zip": "91101", "region": "Los Angeles County", "notes": "Rose Bowl city, Caltech, beautiful craftsman homes, affluent historic community"},
    {"name": "Glendale",              "county": "Los Angeles",    "zip": "91201", "region": "Los Angeles County", "notes": "large Armenian-American community, diverse city north of LA, hillside properties"},
    {"name": "Burbank",               "county": "Los Angeles",    "zip": "91502", "region": "Los Angeles County", "notes": "media capital, Disney and Warner Bros, strong entertainment industry presence"},
    {"name": "Santa Clarita",         "county": "Los Angeles",    "zip": "91350", "region": "Los Angeles County", "notes": "master-planned communities, family-oriented, one of safest large CA cities"},
    {"name": "Pomona",                "county": "Los Angeles",    "zip": "91766", "region": "Los Angeles County", "notes": "inland LA county, Cal Poly Pomona, diverse working-class community"},

    # ── Orange County ──────────────────────────────────────────────────────
    {"name": "Seal Beach",            "county": "Orange",         "zip": "90740", "region": "Orange County",     "notes": "small beach town, Leisure World senior community, charming coastal village"},
    {"name": "Huntington Beach",      "county": "Orange",         "zip": "92648", "region": "Orange County",     "notes": "Surf City USA, beachfront properties, strong demand for coastal homes"},
    {"name": "Fountain Valley",       "county": "Orange",         "zip": "92708", "region": "Orange County",     "notes": "quiet OC suburb, mile square park, mix of older ranch homes and updated properties"},
    {"name": "Westminster",           "county": "Orange",         "zip": "92683", "region": "Orange County",     "notes": "Little Saigon, large Vietnamese-American community, affordable OC housing"},
    {"name": "Garden Grove",          "county": "Orange",         "zip": "92840", "region": "Orange County",     "notes": "diverse north OC city, large Vietnamese and Korean communities, affordable older homes"},
    {"name": "Cypress",               "county": "Orange",         "zip": "90630", "region": "Orange County",     "notes": "small north OC city, well-maintained neighborhoods, strong schools, affordable entry"},
    {"name": "Buena Park",            "county": "Orange",         "zip": "90620", "region": "Orange County",     "notes": "Knott's Berry Farm city, diverse north OC community, mix of commercial and residential"},
    {"name": "La Habra",              "county": "Orange",         "zip": "90631", "region": "Orange County",     "notes": "north OC border city, large Latino community, affordable older housing stock"},
    {"name": "Brea",                  "county": "Orange",         "zip": "92821", "region": "Orange County",     "notes": "upscale north OC city, Brea Mall, oil heritage, newer master-planned communities"},
    {"name": "Yorba Linda",           "county": "Orange",         "zip": "92886", "region": "Orange County",     "notes": "birthplace of Nixon, affluent north OC, large lots, equestrian properties"},
    {"name": "Placentia",             "county": "Orange",         "zip": "92870", "region": "Orange County",     "notes": "north OC suburb, family-friendly, mix of older and newer residential developments"},
    {"name": "Newport Beach",         "county": "Orange",         "zip": "92660", "region": "Orange County",     "notes": "ultra-premium coastal city, among California's most expensive real estate markets"},
    {"name": "Costa Mesa",            "county": "Orange",         "zip": "92626", "region": "Orange County",     "notes": "arts and shopping hub near Newport Beach, mix of older homes and new condos"},
    {"name": "Laguna Beach",          "county": "Orange",         "zip": "92651", "region": "Orange County",     "notes": "premier arts colony, dramatic coastal bluffs, among most expensive in SoCal"},
    {"name": "Laguna Hills",          "county": "Orange",         "zip": "92653", "region": "Orange County",     "notes": "master-planned community in south OC, family-oriented, close to Laguna Beach"},
    {"name": "Laguna Niguel",         "county": "Orange",         "zip": "92677", "region": "Orange County",     "notes": "affluent planned community, ocean views, upscale residential neighborhoods"},
    {"name": "Laguna Woods",          "county": "Orange",         "zip": "92637", "region": "Orange County",     "notes": "55+ retirement community, large active senior population, condo-heavy market"},
    {"name": "Aliso Viejo",           "county": "Orange",         "zip": "92656", "region": "Orange County",     "notes": "planned south OC community, young professional demographic, strong condo market"},
    {"name": "Lake Forest",           "county": "Orange",         "zip": "92630", "region": "Orange County",     "notes": "large OC suburb, mix of older El Toro homes and newer Portola Hills developments"},
    {"name": "Mission Viejo",         "county": "Orange",         "zip": "92691", "region": "Orange County",     "notes": "master-planned community, predominantly single-family homes, strong HOA culture"},
    {"name": "Rancho Santa Margarita", "county": "Orange",        "zip": "92688", "region": "Orange County",     "notes": "planned community in the Saddleback Valley, family-friendly, strong HOA culture"},
    {"name": "Trabuco Canyon",        "county": "Orange",         "zip": "92679", "region": "Orange County",     "notes": "rural unincorporated OC community, horse properties, large lots, scenic canyon setting"},
    {"name": "Foothill Ranch",        "county": "Orange",         "zip": "92610", "region": "Orange County",     "notes": "master-planned community in Lake Forest, newer homes, close to Whiting Ranch trails"},
    {"name": "Dana Point",            "county": "Orange",         "zip": "92629", "region": "Orange County",     "notes": "harbor city, whale watching capital, coastal premium properties"},
    {"name": "San Juan Capistrano",   "county": "Orange",         "zip": "92675", "region": "Orange County",     "notes": "historic mission city, equestrian community, charming Old Town and rural properties"},
    {"name": "San Clemente",          "county": "Orange",         "zip": "92672", "region": "Orange County",     "notes": "Spanish Village by the Sea, coastal community near Camp Pendleton"},
    {"name": "Irvine",                "county": "Orange",         "zip": "92618", "region": "Orange County",     "notes": "one of the most affluent planned communities in the US with high home values"},
    {"name": "Tustin",                "county": "Orange",         "zip": "92780", "region": "Orange County",     "notes": "mix of historic old town and newer Tustin Ranch developments, great location"},
    {"name": "Orange",                "county": "Orange",         "zip": "92868", "region": "Orange County",     "notes": "historic Old Towne Orange, antique district, mix of Victorian and modern homes"},
    {"name": "Santa Ana",             "county": "Orange",         "zip": "92701", "region": "Orange County",     "notes": "Orange County seat, large Hispanic community, many older homes needing updates"},
    {"name": "Anaheim",               "county": "Orange",         "zip": "92801", "region": "Orange County",     "notes": "home of Disneyland, diverse city with a mix of older homes and newer developments"},
    {"name": "Fullerton",             "county": "Orange",         "zip": "92832", "region": "Orange County",     "notes": "college town with Cal State Fullerton, historic downtown, diverse housing stock"},
    {"name": "Stanton",               "county": "Orange",         "zip": "90680", "region": "Orange County",     "notes": "small dense north OC city, very affordable, older housing stock with investment potential"},

    # ── Inland Empire ──────────────────────────────────────────────────────
    {"name": "Riverside",             "county": "Riverside",      "zip": "92501", "region": "Inland Empire",     "notes": "UC Riverside city, historic Mission Inn, gateway to Inland Empire"},
    {"name": "Corona",                "county": "Riverside",      "zip": "92879", "region": "Inland Empire",     "notes": "Circle City, fast-growing suburb, strong commuter base to OC and LA"},
    {"name": "Murrieta",              "county": "Riverside",      "zip": "92562", "region": "Inland Empire",     "notes": "one of fastest-growing SW Riverside cities, excellent schools, master-planned communities"},
    {"name": "Temecula",              "county": "Riverside",      "zip": "92590", "region": "Inland Empire",     "notes": "wine country destination, Old Town charm, strong tourism and residential growth"},
    {"name": "Menifee",               "county": "Riverside",      "zip": "92584", "region": "Inland Empire",     "notes": "one of California's fastest-growing cities, large master-planned communities, family-oriented"},
    {"name": "Lake Elsinore",         "county": "Riverside",      "zip": "92530", "region": "Inland Empire",     "notes": "lakeside city, outdoor recreation, affordable entry-level homes, rapidly growing"},
    {"name": "Ontario",               "county": "San Bernardino", "zip": "91761", "region": "Inland Empire",     "notes": "major logistics hub, Ontario Airport, diverse affordable housing market"},
    {"name": "Rancho Cucamonga",      "county": "San Bernardino", "zip": "91730", "region": "Inland Empire",     "notes": "affluent IE suburb, Victoria Gardens, top-rated schools, mountain views"},

    # ── San Diego County ───────────────────────────────────────────────────
    {"name": "Oceanside",             "county": "San Diego",      "zip": "92054", "region": "San Diego County",  "notes": "military city near Camp Pendleton, beach access, diverse housing"},
    {"name": "Vista",                 "county": "San Diego",      "zip": "92083", "region": "San Diego County",  "notes": "north county inland city, diverse community, affordable housing, strong growth"},
    {"name": "San Marcos",            "county": "San Diego",      "zip": "92069", "region": "San Diego County",  "notes": "fast-growing north county city, Cal State San Marcos, master-planned communities"},
    {"name": "Carlsbad",              "county": "San Diego",      "zip": "92008", "region": "San Diego County",  "notes": "upscale coastal north county, LEGOLAND, premium beachside properties"},
    {"name": "Encinitas",             "county": "San Diego",      "zip": "92024", "region": "San Diego County",  "notes": "surf culture, flower fields, coastal bluffs, upscale north county community"},
    {"name": "Solana Beach",          "county": "San Diego",      "zip": "92075", "region": "San Diego County",  "notes": "small affluent coastal community, Fletcher Cove, premium beachfront values"},
    {"name": "Del Mar",               "county": "San Diego",      "zip": "92014", "region": "San Diego County",  "notes": "iconic racetrack, ultra-premium coastal village, median homes over $3.5M"},
    {"name": "La Jolla",              "county": "San Diego",      "zip": "92037", "region": "San Diego County",  "notes": "ultra-premium coastal village, UC San Diego, among California's most expensive real estate"},
    {"name": "San Diego",             "county": "San Diego",      "zip": "92101", "region": "San Diego County",  "notes": "California's second-largest city, strong military presence, diverse neighborhoods"},
    {"name": "Poway",                 "county": "San Diego",      "zip": "92064", "region": "San Diego County",  "notes": "City in the Country, large lots, excellent schools, affluent north county community"},
    {"name": "Santee",                "county": "San Diego",      "zip": "92071", "region": "San Diego County",  "notes": "east county suburb, affordable housing, outdoor recreation, family-oriented community"},
    {"name": "Escondido",             "county": "San Diego",      "zip": "92025", "region": "San Diego County",  "notes": "inland north county SD, diverse community, mix of older homes and newer developments"},
    {"name": "La Mesa",               "county": "San Diego",      "zip": "91941", "region": "San Diego County",  "notes": "Jewel of the Hills, charming village downtown, close-in east county location"},
    {"name": "Lemon Grove",           "county": "San Diego",      "zip": "91945", "region": "San Diego County",  "notes": "small east county city, affordable entry-level homes, diverse community"},
    {"name": "El Cajon",              "county": "San Diego",      "zip": "92020", "region": "San Diego County",  "notes": "east SD county, large Middle Eastern community, affordable older homes"},
    {"name": "National City",         "county": "San Diego",      "zip": "91950", "region": "San Diego County",  "notes": "south bay city bordering San Diego, diverse community, affordable housing"},
    {"name": "Chula Vista",           "county": "San Diego",      "zip": "91910", "region": "San Diego County",  "notes": "second-largest SD city, diverse community, mix of older south bay and newer eastern developments"},
    {"name": "Coronado",              "county": "San Diego",      "zip": "92118", "region": "San Diego County",  "notes": "island city connected by bridge, Hotel del Coronado, premium military and civilian community"},
    {"name": "Imperial Beach",        "county": "San Diego",      "zip": "91932", "region": "San Diego County",  "notes": "southernmost beach city in US, border community, affordable coastal values"},
]

# ── Grouped city list for the bottom strip ─────────────────────────────────
CITIES_BY_REGION = {
    "Ventura County": [
        "Ventura", "Oxnard", "Port Hueneme", "Camarillo",
        "Thousand Oaks", "Simi Valley", "Ojai",
    ],
    "Los Angeles County": [
        "Malibu", "Santa Monica", "Los Angeles", "Beverly Hills", "West Hollywood",
        "Culver City", "Inglewood", "Hawthorne", "Gardena", "Compton", "Carson",
        "El Segundo", "Manhattan Beach", "Hermosa Beach", "Redondo Beach", "Torrance",
        "Long Beach", "Bellflower", "Paramount", "Downey", "Norwalk", "Cerritos",
        "Lakewood", "Whittier", "El Monte", "West Covina", "Alhambra",
        "Monterey Park", "Arcadia", "Pasadena", "Glendale", "Burbank",
        "Santa Clarita", "Pomona",
    ],
    "Orange County": [
        "Seal Beach", "Huntington Beach", "Fountain Valley", "Westminster",
        "Garden Grove", "Cypress", "Buena Park", "La Habra", "Brea",
        "Yorba Linda", "Placentia", "Stanton", "Newport Beach", "Costa Mesa",
        "Laguna Beach", "Laguna Hills", "Laguna Niguel", "Laguna Woods",
        "Aliso Viejo", "Lake Forest", "Mission Viejo", "Rancho Santa Margarita",
        "Trabuco Canyon", "Foothill Ranch", "Dana Point", "San Juan Capistrano",
        "San Clemente", "Irvine", "Tustin", "Orange", "Santa Ana",
        "Anaheim", "Fullerton",
    ],
    "Inland Empire": [
        "Riverside", "Corona", "Murrieta", "Temecula", "Menifee",
        "Lake Elsinore", "Ontario", "Rancho Cucamonga",
    ],
    "San Diego County": [
        "Oceanside", "Vista", "San Marcos", "Carlsbad", "Encinitas",
        "Solana Beach", "Del Mar", "La Jolla", "San Diego", "Poway",
        "Santee", "Escondido", "La Mesa", "Lemon Grove", "El Cajon",
        "National City", "Chula Vista", "Coronado", "Imperial Beach",
    ],
}

REGION_COLORS = {
    "Ventura County":     "#5b8fa8",
    "Los Angeles County": "#c0622a",
    "Orange County":      "#e8823a",
    "Inland Empire":      "#7a6a52",
    "San Diego County":   "#2a7a6a",
}


def generate_city_content(city: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are an expert real estate SEO content writer for Golden Coast Cash Offer, a cash home buying company serving Southern California.

COMPANY INFO:
- Name: Golden Coast Cash Offer
- Phone: 949-280-5139
- Website: https://www.goldencoastcashoffer.com

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


def build_cities_strip(current_city_name: str) -> str:
    html = ''
    for region, cities in CITIES_BY_REGION.items():
        color = REGION_COLORS.get(region, "#e8823a")
        html += f'''
  <div class="region-group" style="grid-column:1/-1;margin-top:20px">
    <div class="region-label" style="color:{color};border-color:{color}">{region}</div>
    <div class="region-pills">'''
        for city_name in cities:
            slug = city_name.lower().replace(' ', '-')
            if city_name == current_city_name:
                style = f'background:{color};color:#fff;border-color:{color}'
            else:
                style = ''
            html += f'\n      <a href="/{slug}/" class="city-pill" style="{style}">{city_name}</a>'
        html += '\n    </div>\n  </div>'
    return html


def build_city_page(content: dict, city: dict) -> str:
    slug = city['name'].lower().replace(' ', '-')
    year = datetime.now().year
    why_points = ''.join([
        f'<li style="font-size:15px;line-height:1.8;color:#4a3a28;margin:8px 0">{p}</li>'
        for p in content.get('why_sellers_points', [])
    ])
    cities_strip_html = build_cities_strip(city['name'])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{content['meta_title']}</title>
<meta name="description" content="{content['meta_description']}">
<meta property="og:title" content="{content['meta_title']}">
<meta property="og:description" content="{content['meta_description']}">
<link rel="canonical" href="https://www.goldencoastcashoffer.com/{slug}/">
<!-- Google Analytics -->
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
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Golden Coast Cash Offer",
  "telephone": "949-280-5139",
  "url": "https://www.goldencoastcashoffer.com",
  "areaServed": "{city['name']}, California"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type":"Question","name":"How fast can you buy my house in {city['name']}, CA?","acceptedAnswer":{{"@type":"Answer","text":"We can close in as few as 7 days in {city['name']}. Call us at 949-280-5139 to discuss your timeline."}}}},
    {{"@type":"Question","name":"Do I need to make repairs before selling my {city['name']} home?","acceptedAnswer":{{"@type":"Answer","text":"Never. We buy houses in {city['name']} in any condition — no repairs, no cleaning required."}}}},
    {{"@type":"Question","name":"Are there any fees when selling to Golden Coast Cash Offer?","acceptedAnswer":{{"@type":"Answer","text":"Zero fees, zero commissions, zero closing costs. What we offer is exactly what you receive."}}}},
    {{"@type":"Question","name":"Do you buy homes with tenants in {city['name']}?","acceptedAnswer":{{"@type":"Answer","text":"Yes. We buy California properties with tenants in place — you don't need to deal with California tenant laws."}}}}
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
.cities-strip{{background:linear-gradient(160deg,var(--ocean),var(--ocean2));padding:48px 40px}}
.cities-strip > h2{{font-family:'Cormorant Garamond',serif;font-size:26px;color:#fff;margin-bottom:8px;text-align:center}}
.cities-strip > p{{text-align:center;color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:8px}}
.region-group{{margin-top:24px}}
.region-label{{font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;padding:4px 12px;border:1px solid;border-radius:20px;display:inline-block;margin-bottom:10px}}
.region-pills{{display:flex;flex-wrap:wrap;gap:7px}}
.city-pill{{padding:7px 14px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.75);font-size:11px;font-weight:600;text-decoration:none;border-radius:20px;transition:all .15s;white-space:nowrap}}
.city-pill:hover{{background:rgba(255,255,255,0.2);color:#fff}}
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
  <a href="/" class="nav-logo">Golden Coast Cash Offer</a>
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
        <div class="badge">Tenants OK</div>
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
          <input type="text" name="name" placeholder="John Smith" required>
        </div>
        <div class="field">
          <label>Property Address *</label>
          <input type="text" name="address" placeholder="{city['name']}, CA {city['zip']}" required>
        </div>
        <div class="field-row">
          <div class="field">
            <label>Phone *</label>
            <input type="tel" name="phone" placeholder="(949) 555-0000" required>
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
    <div class="sidebar-card">
      <h3>California Sellers</h3>
      <p style="font-size:12px;color:#7a6a52;line-height:1.7;margin:0">We handle tenant situations, probate, trust sales, and all California-specific complexities — so you don't have to.</p>
    </div>
  </div>
</div>
<div class="cities-strip">
  <h2>We Buy Houses Across Southern California</h2>
  <p>{len(CITIES)} cities · OC · LA · San Diego · Ventura · Inland Empire</p>
  {cities_strip_html}
</div>
<footer>
  © {year} Golden Coast Cash Offer · <a href="/">goldencoastcashoffer.com</a> · 949-280-5139<br>
  Serving {city['name']} and all of Southern California
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
    print(f"Generating {len(CITIES)} SoCal city landing pages — {datetime.now().isoformat()}")
    print()

    for i, city in enumerate(CITIES):
        slug = city['name'].lower().replace(' ', '-')
        output_dir = Path(slug)
        output_file = output_dir / "index.html"

        # Skip if already exists
        if output_file.exists():
            print(f"  [{i+1}/{len(CITIES)}] Skipping {city['name']} — already exists")
            continue

        print(f"  [{i+1}/{len(CITIES)}] Generating {city['name']} ({city['region']})...")
        try:
            content = generate_city_content(city)
            html = build_city_page(content, city)
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"    ✓ {output_file}")
        except Exception as e:
            print(f"    ✗ Error on {city['name']}: {e}")

    print()
    print(f"Done! {len(CITIES)} cities processed.")
    print("Commit all new folders to GitHub — Netlify will auto-deploy.")


if __name__ == "__main__":
    main()
