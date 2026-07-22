#!/usr/bin/env python3
"""
Golden Coast Cash Offer - Keyword Landing Page Generator
Generates /sell-my-house-fast-{city}-ca/ pages for SoCal cities
Run once to generate all pages, then commit to repo
"""

from pathlib import Path
from datetime import datetime

# City data: name, slug, zip codes, neighborhoods, county, market context
CITIES = [
    {
        "name": "Irvine",
        "slug": "irvine",
        "zips": ["92602", "92603", "92604", "92606", "92612", "92614", "92617", "92618", "92620"],
        "neighborhoods": ["Woodbridge", "Northwood", "Turtle Rock", "University Park", "Quail Hill", "Portola Springs", "Great Park"],
        "county": "Orange County",
        "context": "one of Southern California's most planned and desirable cities, known for top-rated schools, master-planned communities, and strong property values typically ranging from $900K to $2M+",
        "specifics": "With Irvine's strict HOA communities, high-density condos near the Irvine Spectrum, and complex trust sales common in established neighborhoods like Turtle Rock, selling traditionally can involve lengthy timelines and strict HOA transfer requirements."
    },
    {
        "name": "Newport Beach",
        "slug": "newport-beach",
        "zips": ["92657", "92660", "92661", "92662", "92663"],
        "neighborhoods": ["Corona del Mar", "Newport Coast", "Balboa Island", "Lido Isle", "West Newport"],
        "county": "Orange County",
        "context": "one of California's most prestigious coastal communities, with median home prices often exceeding $3M and a market driven by luxury buyers and second-home investors",
        "specifics": "Newport Beach properties often involve trust sales, divorce settlements on high-value assets, or landlords managing vacation rental compliance under new Newport Beach short-term rental ordinances."
    },
    {
        "name": "Huntington Beach",
        "slug": "huntington-beach",
        "zips": ["92646", "92647", "92648", "92649"],
        "neighborhoods": ["Downtown HB", "Seacliff", "Huntington Harbour", "Meadowlark", "South Huntington"],
        "county": "Orange County",
        "context": "Surf City USA — a highly desirable coastal community where home values range from $700K for inland properties to $3M+ for oceanfront homes",
        "specifics": "Huntington Beach homeowners often deal with flood zone considerations, coastal commission requirements, and vacation rental regulations that complicate traditional listings."
    },
    {
        "name": "Mission Viejo",
        "slug": "mission-viejo",
        "zips": ["92691", "92692"],
        "neighborhoods": ["Lake Mission Viejo", "Aegean Hills", "Painted Trails", "Canyon Crest", "Melinda Heights"],
        "county": "Orange County",
        "context": "a master-planned community in South Orange County known for its lake, excellent schools, and stable home values typically ranging from $750K to $1.5M",
        "specifics": "Mission Viejo's lake community HOA, strict architectural guidelines, and large share of long-term homeowners mean many sellers are dealing with estate sales, trust transfers, or major deferred maintenance after decades of ownership."
    },
    {
        "name": "Costa Mesa",
        "slug": "costa-mesa",
        "zips": ["92626", "92627", "92628"],
        "neighborhoods": ["Eastside Costa Mesa", "Westside Costa Mesa", "Mesa Verde", "South Coast Metro", "College Park"],
        "county": "Orange County",
        "context": "a dynamic Orange County city adjacent to Newport Beach, with home values ranging from $800K to $2M+ depending on proximity to the coast",
        "specifics": "Costa Mesa's mix of older mid-century homes needing updates, condo complexes with HOA issues, and landlords navigating California tenant protections makes cash sales a frequent solution."
    },
    {
        "name": "Laguna Niguel",
        "slug": "laguna-niguel",
        "zips": ["92677"],
        "neighborhoods": ["Bear Brand Ranch", "Laguna Sur", "Marina Hills", "Monarch Beach", "Pacific Island"],
        "county": "Orange County",
        "context": "an upscale South OC community bordering the coast, with median home prices around $1.2M and strong demand from buyers seeking Laguna Beach proximity without the price tag",
        "specifics": "Laguna Niguel's hillside communities, gated enclaves, and prevalence of HOA-governed developments mean sellers often face transfer delays, special assessments, and disclosure requirements that slow traditional sales."
    },
    {
        "name": "Aliso Viejo",
        "slug": "aliso-viejo",
        "zips": ["92656"],
        "neighborhoods": ["Glenwood", "Pacific Ridge", "Vantis", "Aliso Ranch", "Canyon Vistas"],
        "county": "Orange County",
        "context": "a planned community in South Orange County with home values typically ranging from $700K to $1.3M, popular with families and young professionals",
        "specifics": "Aliso Viejo's heavily HOA-governed communities and large condo market mean sellers frequently face special assessments, rental restrictions, and mandatory disclosure packets that extend traditional closing timelines."
    },
    {
        "name": "Lake Forest",
        "slug": "lake-forest",
        "zips": ["92630", "92679"],
        "neighborhoods": ["Foothill Ranch", "Baker Ranch", "Serrano", "Sun and Sail", "Portola Hills"],
        "county": "Orange County",
        "context": "a growing South OC community with home values from $750K to $1.5M, known for newer master-planned neighborhoods and easy Toll Road access",
        "specifics": "Lake Forest's mix of resale HOA communities and newer construction means sellers dealing with inherited properties, divorce, or relocation often find cash sales the fastest path to closing."
    },
    {
        "name": "Laguna Hills",
        "slug": "laguna-hills",
        "zips": ["92653", "92654"],
        "neighborhoods": ["Moulton Ranch", "Laguna Hills Estates", "Nellie Gail Ranch", "Creekside", "Village Walk"],
        "county": "Orange County",
        "context": "a quiet South OC city with home values from $700K to $2M+, anchored by established residential neighborhoods and easy freeway access",
        "specifics": "Laguna Hills has a high percentage of long-term homeowners, meaning many properties coming to market involve estate sales, trust administration, or deferred maintenance on older homes."
    },
    {
        "name": "San Clemente",
        "slug": "san-clemente",
        "zips": ["92672", "92673"],
        "neighborhoods": ["Southeast San Clemente", "Talega", "Las Palmas", "Southwest San Clemente", "Northwest San Clemente"],
        "county": "Orange County",
        "context": "a coastal surf town at the southern tip of Orange County with median home prices around $1.1M, popular for its Spanish Colonial architecture and beach lifestyle",
        "specifics": "San Clemente homeowners often deal with hillside properties requiring coastal commission disclosure, older homes with deferred maintenance, or vacation rental compliance issues."
    },
    {
        "name": "Dana Point",
        "slug": "dana-point",
        "zips": ["92624", "92629"],
        "neighborhoods": ["Lantern District", "Monarch Beach", "Capistrano Beach", "Dana Hills", "Strand at Headlands"],
        "county": "Orange County",
        "context": "a charming harbor city at the southern end of Orange County with home values from $800K to $4M+ for oceanfront properties",
        "specifics": "Dana Point's coastal location means sellers frequently navigate California Coastal Commission requirements, short-term rental ordinance compliance, and high property tax carry costs that make cash sales attractive."
    },
    {
        "name": "San Juan Capistrano",
        "slug": "san-juan-capistrano",
        "zips": ["92675"],
        "neighborhoods": ["Mission Hills", "Rancho Madrina", "Ortega Ranch", "Marbella", "Shangri-La"],
        "county": "Orange County",
        "context": "a historic city known for the Mission and equestrian estates, with home values ranging from $700K for standard homes to $5M+ for horse properties",
        "specifics": "San Juan Capistrano's equestrian zoning, historic district regulations, and large share of estate properties create complexities that often make cash sales the most practical option for sellers."
    },
    {
        "name": "Carlsbad",
        "slug": "carlsbad",
        "zips": ["92008", "92009", "92010", "92011"],
        "neighborhoods": ["La Costa", "Aviara", "Bressi Ranch", "Calavera Hills", "Village by the Sea"],
        "county": "San Diego County",
        "context": "one of San Diego County's most desirable coastal cities with median home prices around $1.3M, known for Legoland, world-class golf, and pristine beaches",
        "specifics": "Carlsbad's mix of coastal estates, master-planned inland communities, and vacation-rental properties means sellers often face HOA complexities, coastal permit requirements, or tenant transition issues."
    },
    {
        "name": "Encinitas",
        "slug": "encinitas",
        "zips": ["92024"],
        "neighborhoods": ["Leucadia", "Cardiff-by-the-Sea", "Olivenhain", "New Encinitas", "Old Encinitas"],
        "county": "San Diego County",
        "context": "a beloved North San Diego County beach community with home values typically ranging from $1M to $4M+, known for its surf culture and coastal lifestyle",
        "specifics": "Encinitas sellers frequently encounter coastal bluff setback requirements, short-term rental compliance issues, and high carrying costs that make a quick cash sale attractive over a drawn-out listing process."
    },
    {
        "name": "Temecula",
        "slug": "temecula",
        "zips": ["92590", "92591", "92592"],
        "neighborhoods": ["Wine Country", "Redhawk", "Paloma del Sol", "Harveston", "Old Town Temecula"],
        "county": "Riverside County",
        "context": "the Inland Empire's wine country city with home values from $500K to $1.5M+, popular for its wineries, master-planned communities, and relative affordability compared to coastal OC",
        "specifics": "Temecula's large share of HOA-governed communities, vacation rental properties near the wineries, and a significant retiree population mean estate sales and downsizing are common motivators for a quick cash sale."
    },
    {
        "name": "Murrieta",
        "slug": "murrieta",
        "zips": ["92562", "92563"],
        "neighborhoods": ["Central Murrieta", "West Murrieta", "Greer Ranch", "Spencer's Crossing", "Copper Canyon"],
        "county": "Riverside County",
        "context": "a fast-growing Inland Empire city with home values from $450K to $900K, offering more space and affordability than coastal communities while still accessible to OC and San Diego",
        "specifics": "Murrieta's rapid growth means many homeowners are investors with multiple properties, landlords managing tenant transitions, or families relocating for work who need to close quickly."
    },
    {
        "name": "Riverside",
        "slug": "riverside",
        "zips": ["92501", "92503", "92504", "92505", "92506", "92507", "92508"],
        "neighborhoods": ["Wood Streets", "Alessandro Heights", "Canyon Crest", "Orangecrest", "La Sierra"],
        "county": "Riverside County",
        "context": "the Inland Empire's largest city with home values from $400K to $900K, offering diverse neighborhoods from historic districts to newer suburban developments",
        "specifics": "Riverside's older housing stock, large rental investor market, and significant share of distressed properties mean cash buyers are a common and practical solution for sellers facing repairs, tenant issues, or financial hardship."
    },
    {
        "name": "Corona",
        "slug": "corona",
        "zips": ["92879", "92880", "92881", "92882", "92883"],
        "neighborhoods": ["South Corona", "Sierra del Oro", "Chase Ranch", "Horsethief Canyon", "El Cerrito"],
        "county": "Riverside County",
        "context": "a growing Inland Empire city at the gateway to Orange County with home values from $550K to $950K, popular for its relative affordability and freeway access",
        "specifics": "Corona's position between OC and the IE attracts both investors and primary homeowners. Many sellers are landlords or homeowners facing major repairs on older properties who prefer a fast cash sale over a costly renovation."
    },
    {
        "name": "Oceanside",
        "slug": "oceanside",
        "zips": ["92054", "92056", "92057", "92058"],
        "neighborhoods": ["Downtown Oceanside", "Fire Mountain", "South Oceanside", "Rancho del Oro", "Jeffries Ranch"],
        "county": "San Diego County",
        "context": "North San Diego County's largest city with home values from $600K to $1.5M+, offering coastal living at more accessible prices than neighboring Carlsbad and Encinitas",
        "specifics": "Oceanside's large military community (adjacent to Camp Pendleton) means many sellers are PCS-ing on short notice and need a fast, guaranteed close without the uncertainty of a traditional listing."
    },
    {
        "name": "Escondido",
        "slug": "escondido",
        "zips": ["92025", "92026", "92027", "92029"],
        "neighborhoods": ["Hidden Meadows", "Felicita", "Valley Center adjacent", "Central Escondido", "East Escondido"],
        "county": "San Diego County",
        "context": "an inland San Diego County city with home values from $550K to $900K, offering larger lots and more affordability than coastal communities",
        "specifics": "Escondido's older housing stock, large share of rental properties, and diverse seller situations — from inherited homes to landlords exiting the market — make cash sales a frequent and practical choice."
    },
    {
        "name": "San Diego",
        "slug": "san-diego",
        "zips": ["92101", "92103", "92104", "92105", "92108", "92115", "92116", "92117", "92120", "92123"],
        "neighborhoods": ["North Park", "Hillcrest", "Mission Valley", "San Carlos", "Kensington", "Linda Vista", "Clairemont"],
        "county": "San Diego County",
        "context": "California's second-largest city with home values ranging widely from $650K to $3M+ depending on neighborhood and proximity to the coast",
        "specifics": "San Diego's diverse neighborhoods, large military and biotech employer base, and significant rental market mean sellers come from every situation — relocation, divorce, inherited property, tired landlord — and often need the speed and certainty of a cash sale."
    },
    {
        "name": "Chula Vista",
        "slug": "chula-vista",
        "zips": ["91910", "91911", "91913", "91914", "91915"],
        "neighborhoods": ["Eastlake", "Otay Ranch", "Rancho del Rey", "Bonita adjacent", "Downtown Chula Vista"],
        "county": "San Diego County",
        "context": "San Diego's second-largest city with home values from $600K to $900K, featuring master-planned communities in the east and established neighborhoods in the west",
        "specifics": "Chula Vista's rapid eastern growth has created a large HOA-governed community market. Sellers dealing with special assessments, Mello-Roos tax complications, or tenant-occupied investment properties often find cash sales the simplest path forward."
    },
    {
        "name": "Los Angeles",
        "slug": "los-angeles",
        "zips": ["90001", "90011", "90018", "90019", "90025", "90034", "90043", "90047", "90062", "90068"],
        "neighborhoods": ["Mid-City", "West Adams", "Palms", "Mar Vista", "Highland Park", "Eagle Rock", "Leimert Park"],
        "county": "Los Angeles County",
        "context": "the nation's second-largest city with home values ranging from $600K in outlying areas to $5M+ in prime westside neighborhoods, with an extraordinarily diverse seller market",
        "specifics": "Los Angeles sellers face some of California's most complex tenant protections under the LA Rent Stabilization Ordinance (RSO), strict disclosure requirements, and frequent probate and trust sales. Cash buyers who understand LA-specific regulations provide the fastest, cleanest path to closing."
    },
    {
        "name": "Long Beach",
        "slug": "long-beach",
        "zips": ["90802", "90803", "90804", "90805", "90806", "90807", "90808"],
        "neighborhoods": ["Belmont Shore", "Naples", "Bixby Knolls", "Signal Hill adjacent", "Los Altos", "Wrigley"],
        "county": "Los Angeles County",
        "context": "a diverse coastal city with home values from $550K to $2M+ on the waterfront, offering more affordability than neighboring beach communities while maintaining coastal access",
        "specifics": "Long Beach has its own rent control ordinance and significant multi-unit inventory. Landlords dealing with rent-controlled tenants, sellers managing older craftsman homes, and estate executors frequently choose cash buyers to avoid the complexity of a traditional sale."
    },
    {
        "name": "Torrance",
        "slug": "torrance",
        "zips": ["90501", "90502", "90503", "90504", "90505"],
        "neighborhoods": ["Old Torrance", "Hollywood Riviera", "South Bay Galleria area", "West Torrance", "North Torrance"],
        "county": "Los Angeles County",
        "context": "a well-established South Bay city with home values from $750K to $2M+, known for its excellent schools, walkable downtown, and proximity to the beach",
        "specifics": "Torrance's stable, owner-occupied neighborhoods have a high share of long-term homeowners, meaning many properties coming to market involve estate sales, significant deferred maintenance, or trust transfers that benefit from the speed of a cash sale."
    },
    {
        "name": "Thousand Oaks",
        "slug": "thousand-oaks",
        "zips": ["91320", "91360", "91361", "91362"],
        "neighborhoods": ["Newbury Park", "Lynn Ranch", "Conejo Valley", "Wildwood", "Lang Ranch"],
        "county": "Ventura County",
        "context": "one of Ventura County's most desirable cities with home values from $800K to $2M+, consistently ranked among the safest cities in the nation",
        "specifics": "Thousand Oaks sellers often include long-term homeowners downsizing from large family homes, estate executors managing trust sales, and landlords navigating California tenant protections in a strong rental market."
    },
    {
        "name": "Oxnard",
        "slug": "oxnard",
        "zips": ["93030", "93033", "93035", "93036"],
        "neighborhoods": ["Oxnard Shores", "Silver Strand", "Riverpark", "South Oxnard", "Northbank"],
        "county": "Ventura County",
        "context": "Ventura County's largest city with home values from $550K to $1.5M+ for beachfront properties, offering coastal access at more affordable prices than Orange County",
        "specifics": "Oxnard's diverse housing stock — from beachfront condos to agricultural-adjacent properties — and strong rental market mean sellers frequently deal with tenant situations, deferred maintenance, or inherited properties."
    },
    {
        "name": "Ventura",
        "slug": "ventura",
        "zips": ["93001", "93003", "93004"],
        "neighborhoods": ["Midtown", "Downtown Ventura", "Pierpont", "East Ventura", "Ondulando"],
        "county": "Ventura County",
        "context": "a classic California coastal city with home values from $600K to $1.5M+, known for its surf, farmers market, and relaxed beach town atmosphere",
        "specifics": "Ventura's older housing stock, active vacation rental market, and significant share of inherited coastal properties mean sellers frequently need a buyer who can close without requiring costly repairs or renovations."
    },
    {
        "name": "Rancho Cucamonga",
        "slug": "rancho-cucamonga",
        "zips": ["91701", "91730", "91737", "91739"],
        "neighborhoods": ["Etiwanda", "Alta Loma", "Victoria", "Northtown", "Haven View Estates"],
        "county": "San Bernardino County",
        "context": "one of the Inland Empire's most desirable cities with home values from $550K to $1.2M, known for its planned communities, mountain views, and growing job market",
        "specifics": "Rancho Cucamonga's large HOA community base and strong rental market mean sellers often deal with special assessments, investor exits, or families relocating for work who need a guaranteed fast close."
    },
    {
        "name": "Anaheim",
        "slug": "anaheim",
        "zips": ["92801", "92802", "92804", "92805", "92806", "92807", "92808"],
        "neighborhoods": ["Anaheim Hills", "Platinum Triangle", "Colony Historic District", "West Anaheim", "East Anaheim"],
        "county": "Orange County",
        "context": "Orange County's largest city with home values from $600K to $1.5M+ in Anaheim Hills, known for Disneyland, Angel Stadium, and a diverse mix of residential neighborhoods",
        "specifics": "Anaheim's large vacation rental market near Disneyland, significant older housing inventory in West Anaheim, and diverse seller situations make cash buyers an attractive option for homeowners who want to avoid costly updates before listing."
    },
    {
        "name": "Santa Ana",
        "slug": "santa-ana",
        "zips": ["92701", "92703", "92704", "92705", "92706", "92707"],
        "neighborhoods": ["Floral Park", "Park Santiago", "Downtown Santa Ana", "South Coast Metro adjacent", "Lacy"],
        "county": "Orange County",
        "context": "Orange County's second-largest city with home values from $550K to $1.2M, featuring a mix of historic neighborhoods and urban development near the civic center",
        "specifics": "Santa Ana has a high concentration of older homes, a significant rental market, and many multi-generational family properties. Sellers dealing with inherited homes, deferred maintenance, or tenant situations frequently choose cash buyers."
    },
    {
        "name": "Fullerton",
        "slug": "fullerton",
        "zips": ["92831", "92832", "92833", "92835"],
        "neighborhoods": ["Downtown Fullerton", "Sunny Hills", "Amerige Heights", "Raymond Hills", "Richman"],
        "county": "Orange County",
        "context": "a college town and established Orange County community with home values from $650K to $1.5M, known for its tree-lined streets, historic downtown, and Cal State Fullerton",
        "specifics": "Fullerton's large student rental market, older craftsman homes near downtown, and active investor community mean sellers often deal with tenant situations, significant deferred maintenance, or multi-unit properties that benefit from cash sales."
    },
]

YEAR = datetime.now().year


def build_page(city: dict) -> str:
    name = city["name"]
    slug = city["slug"]
    zips = city["zips"]
    neighborhoods = city["neighborhoods"]
    county = city["county"]
    context = city["context"]
    specifics = city["specifics"]

    zip_str = ", ".join(zips)
    neighborhood_list = "".join(f"<span>{n}</span>" for n in neighborhoods)
    neighborhood_prose = ", ".join(neighborhoods[:-1]) + f", and {neighborhoods[-1]}" if len(neighborhoods) > 1 else neighborhoods[0]

    canonical_url = f"https://www.goldencoastcashoffer.com/sell-my-house-fast-{slug}-ca/"
    city_page_url = f"https://www.goldencoastcashoffer.com/{slug}/"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sell My House Fast {name} CA | Cash Offer in 24 Hours</title>
<meta name="description" content="Sell your {name} house fast for cash. No repairs, no fees, no commissions. Get a fair cash offer in 24 hours. Close in 7 days or on your timeline. Call 949-280-5139.">
<meta property="og:title" content="Sell My House Fast {name} CA | Cash Offer in 24 Hours">
<meta property="og:description" content="We buy houses in {name}, CA fast for cash. No repairs needed. Get a fair cash offer in 24 hours. Call 949-280-5139.">
<link rel="canonical" href="{canonical_url}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Golden Coast Cash Offer",
  "telephone": "949-280-5139",
  "url": "https://www.goldencoastcashoffer.com",
  "areaServed": {{
    "@type": "City",
    "name": "{name}",
    "addressRegion": "CA"
  }},
  "description": "We buy houses fast in {name}, CA for cash. No repairs, no fees, no commissions. Cash offer in 24 hours.",
  "priceRange": "Cash offers"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question","name": "How fast can you buy my {name} house?","acceptedAnswer": {{"@type": "Answer","text": "We can close in as few as 7 days in {name}. Call 949-280-5139 and we can have a cash offer to you within 24 hours."}}}},
    {{"@type": "Question","name": "Do I need to make repairs before selling?","acceptedAnswer": {{"@type": "Answer","text": "Never. We buy {name} houses in any condition — no repairs, no cleaning, no staging required."}}}},
    {{"@type": "Question","name": "Are there any fees or commissions?","acceptedAnswer": {{"@type": "Answer","text": "Zero fees, zero commissions, zero closing costs. What we offer is exactly what you receive at closing."}}}},
    {{"@type": "Question","name": "Do you buy houses with tenants in {name}?","acceptedAnswer": {{"@type": "Answer","text": "Yes. We buy {county} properties with tenants in place. We handle California tenant protection requirements after closing so you don't have to."}}}}
  ]
}}
</script>
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
body{{background:#fdfaf5;color:#2a2018;font-family:'Nunito',sans-serif;font-weight:300;line-height:1.6}}
.site-nav{{background:#0f4a63;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid #e8823a;position:sticky;top:0;z-index:100}}
.nav-logo{{color:#f8d264;font-family:'Cormorant Garamond',serif;font-weight:700;font-size:20px;text-decoration:none}}
.nav-links{{display:flex;align-items:center;gap:20px}}
.nav-links a{{color:rgba(255,255,255,0.7);font-size:12px;font-weight:600;text-decoration:none;letter-spacing:0.05em;text-transform:uppercase}}
.nav-cta{{background:#e8823a;color:#fff !important;padding:9px 18px;border-radius:20px}}
.hero{{background:linear-gradient(160deg,#0f4a63 0%,#1a6b8a 100%);padding:56px 40px 48px;text-align:center;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=60') center/cover;opacity:0.1}}
.hero-inner{{position:relative;z-index:1;max-width:780px;margin:0 auto}}
.hero-badge{{display:inline-block;background:rgba(232,130,58,0.2);border:1px solid rgba(232,130,58,0.4);color:#f8d264;font-size:10px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;padding:5px 14px;border-radius:20px;margin-bottom:14px}}
.hero h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,4.5vw,52px);color:#fff;font-weight:700;line-height:1.1;margin-bottom:14px}}
.hero-sub{{font-size:15px;color:rgba(255,255,255,0.75);margin-bottom:28px;line-height:1.6}}
.hero-pills{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:28px}}
.pill{{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;font-size:11px;font-weight:600;padding:6px 14px;border-radius:20px;letter-spacing:0.04em}}
.hero-form{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:24px;max-width:480px;margin:0 auto}}
.hero-form p{{color:rgba(255,255,255,0.6);font-size:11px;margin-bottom:14px;letter-spacing:0.06em;text-transform:uppercase}}
.form-row{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}}
.form-row input,.hero-form input,.hero-form select{{width:100%;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:11px 14px;color:#fff;font-size:13px;font-family:'Nunito',sans-serif;outline:none}}
.form-row input::placeholder,.hero-form input::placeholder{{color:rgba(255,255,255,0.4)}}
.hero-form select{{color:rgba(255,255,255,0.6)}}
.hero-form select option{{color:#000}}
.btn-primary{{display:block;width:100%;background:#e8823a;color:#fff;border:none;padding:14px;font-weight:700;font-size:14px;border-radius:20px;cursor:pointer;font-family:'Nunito',sans-serif;margin-top:10px;letter-spacing:0.03em}}
.hero-form .fine{{font-size:10px;color:rgba(255,255,255,0.35);margin-top:8px;text-transform:none;letter-spacing:0}}
.layout{{max-width:1080px;margin:0 auto;padding:48px 24px;display:grid;grid-template-columns:1fr 300px;gap:44px;align-items:start}}
@media(max-width:768px){{.layout{{grid-template-columns:1fr}}.form-row{{grid-template-columns:1fr}}}}
.main h2{{font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:700;color:#0f4a63;margin:36px 0 12px;line-height:1.2}}
.main h3{{font-size:17px;font-weight:700;color:#1a6b8a;margin:22px 0 8px}}
.main p{{font-size:15px;line-height:1.9;color:#4a3a28;margin-bottom:14px}}
.main ul{{padding-left:20px;margin-bottom:14px}}
.main li{{font-size:15px;line-height:1.8;color:#4a3a28;margin:5px 0}}
.zip-box{{background:#fff;border:1px solid #ddd5c0;border-left:3px solid #e8823a;padding:16px 20px;margin:24px 0;border-radius:0 8px 8px 0}}
.zip-box h3{{font-size:13px;font-weight:700;color:#0f4a63;margin-bottom:8px;letter-spacing:0.05em;text-transform:uppercase}}
.zip-box .zips{{font-size:13px;color:#7a6a52;line-height:1.8}}
.neighborhood-box{{background:#fff;border:1px solid #ddd5c0;border-left:3px solid #0f4a63;padding:16px 20px;margin:24px 0;border-radius:0 8px 8px 0}}
.neighborhood-box h3{{font-size:13px;font-weight:700;color:#0f4a63;margin-bottom:10px;letter-spacing:0.05em;text-transform:uppercase}}
.neighborhood-box span{{display:inline-block;background:#f0ece4;color:#4a3a28;font-size:12px;font-weight:600;padding:4px 10px;border-radius:12px;margin:3px 3px 3px 0}}
.cta-block{{background:linear-gradient(135deg,#0f4a63,#1a6b8a);border-left:4px solid #e8823a;padding:24px 28px;margin:32px 0;border-radius:0 12px 12px 0}}
.cta-block h3{{color:#f8d264;font-size:16px;font-weight:700;margin-bottom:8px;font-family:'Cormorant Garamond',serif}}
.cta-block p{{color:rgba(255,255,255,0.8);font-size:14px;margin-bottom:16px;line-height:1.7}}
.cta-block a{{display:inline-block;background:#e8823a;color:#fff;padding:12px 24px;font-weight:700;font-size:13px;text-decoration:none;border-radius:20px}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}}
@media(max-width:600px){{.steps{{grid-template-columns:1fr}}}}
.step{{background:#fff;border:1px solid #ddd5c0;border-top:3px solid #e8823a;padding:20px;border-radius:0 0 10px 10px;text-align:center}}
.step-num{{font-family:'Cormorant Garamond',serif;font-size:32px;font-weight:700;color:#e8823a;line-height:1}}
.step h4{{font-size:13px;font-weight:700;color:#0f4a63;margin:8px 0 4px}}
.step p{{font-size:12px;color:#7a6a52;line-height:1.6;margin:0}}
.sidebar{{position:sticky;top:80px}}
.s-card{{background:#fff;border:1px solid #ddd5c0;border-top:3px solid #e8823a;padding:22px;margin-bottom:18px;border-radius:0 0 10px 10px}}
.s-card h3{{font-size:14px;font-weight:700;color:#0f4a63;margin-bottom:6px;font-family:'Cormorant Garamond',serif}}
.s-card p{{font-size:12px;color:#7a6a52;line-height:1.6;margin-bottom:14px}}
.s-phone{{font-size:22px;font-weight:700;color:#e8823a;text-decoration:none;display:block;margin-bottom:12px}}
.s-btn{{display:block;padding:11px;font-weight:700;font-size:11px;text-decoration:none;border-radius:20px;letter-spacing:0.06em;text-transform:uppercase;text-align:center;margin-bottom:8px}}
.s-btn.orange{{background:#e8823a;color:#fff}}
.s-btn.navy{{background:#0f4a63;color:#fff}}
.trust-items{{list-style:none;padding:0;margin:0}}
.trust-items li{{font-size:12px;color:#4a3a28;padding:6px 0;border-bottom:1px solid #f0ece4;display:flex;align-items:center;gap:8px}}
.trust-items li:last-child{{border:none}}
.trust-items li::before{{content:'✓';color:#e8823a;font-weight:700;flex-shrink:0}}
footer{{background:#0f4a63;color:rgba(255,255,255,0.5);text-align:center;padding:28px;font-size:12px;border-top:3px solid #e8823a}}
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

<div class="hero">
  <div class="hero-inner">
    <div class="hero-badge">{county} · Southern California</div>
    <h1>Sell My House Fast in {name}, CA</h1>
    <p class="hero-sub">Get a fair cash offer in 24 hours. No repairs, no fees, no commissions. Close in as few as 7 days — or on your timeline.</p>
    <div class="hero-pills">
      <span class="pill">No Repairs Needed</span>
      <span class="pill">No Agent Fees</span>
      <span class="pill">Close in 7 Days</span>
      <span class="pill">Tenants OK</span>
      <span class="pill">Any Condition</span>
    </div>
    <div class="hero-form">
      <p>Get your free cash offer — takes 60 seconds</p>
      <div class="form-row">
        <input type="text" placeholder="Your Name">
        <input type="tel" placeholder="Phone Number">
      </div>
      <input type="text" placeholder="Property Address in {name}" style="margin-bottom:10px">
      <select>
        <option value="" disabled selected>Your Situation (optional)</option>
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
      <button class="btn-primary" onclick="window.location.href='/#offer'">Get My Free Cash Offer →</button>
      <p class="fine">100% confidential · No obligation · No spam ever</p>
    </div>
  </div>
</div>

<div class="layout">
  <div class="main">

    <h2>We Buy Houses in {name}, CA — Any Condition, Any Situation</h2>
    <p>Golden Coast Cash Offer purchases homes throughout {name}, {county}. Whether you're dealing with an inherited property, facing foreclosure, going through a divorce, or simply need to sell quickly without the hassle of repairs and showings, we provide a straightforward alternative to the traditional listing process.</p>
    <p>{name} is {context}. {specifics}</p>

    <div class="zip-box">
      <h3>ZIP Codes We Serve in {name}</h3>
      <div class="zips">{zip_str}</div>
    </div>

    <div class="neighborhood-box">
      <h3>Neighborhoods We Buy Houses In</h3>
      {neighborhood_list}
    </div>

    <h2>How Our {name} Home Buying Process Works</h2>
    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <h4>Contact Us</h4>
        <p>Call 949-280-5139 or fill out our form. Tell us about your {name} property — takes 60 seconds.</p>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <h4>Get Your Offer</h4>
        <p>We research your neighborhood and present a fair, no-obligation cash offer within 24 hours.</p>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <h4>Close &amp; Get Paid</h4>
        <p>Choose your closing date — as fast as 7 days. We handle all paperwork through a reputable {county} escrow company.</p>
      </div>
    </div>

    <div class="cta-block">
      <h3>Ready to Sell Your {name} Home Fast?</h3>
      <p>Call us at 949-280-5139 or fill out our form to get a no-obligation cash offer within 24 hours. No repairs, no fees, no surprises.</p>
      <a href="/#offer">Get My Free Cash Offer</a>
    </div>

    <h2>Why {name} Homeowners Choose a Cash Sale</h2>
    <p>A traditional listing in {name} involves repairs, showings, open houses, buyer financing contingencies, and an average of 30–60+ days to close — even after you find a buyer. For many homeowners, that timeline and uncertainty simply doesn't work.</p>
    <p>When you sell to Golden Coast Cash Offer, you skip all of it. No repairs. No cleaning. No agents taking 5–6% commission. No buyer asking for credits at the inspection. You get a guaranteed cash offer, and you choose the closing date.</p>

    <h3>Situations We Commonly Help With in {name}</h3>
    <ul>
      <li><strong>Inherited properties and trust sales</strong> — We work directly with executors, trustees, and probate attorneys throughout {county} to facilitate clean, efficient transactions</li>
      <li><strong>Divorce and community property splits</strong> — California is a community property state. We close quickly so both parties can move forward</li>
      <li><strong>Homes needing major repairs</strong> — Foundation issues, roof damage, outdated systems, water damage — we buy as-is and handle everything after closing</li>
      <li><strong>Landlords with tenant situations</strong> — We purchase tenant-occupied properties in {name} and navigate California's complex tenant protection laws ourselves</li>
      <li><strong>Foreclosure prevention</strong> — If you're behind on payments, a fast cash sale can stop foreclosure and protect your credit</li>
      <li><strong>Relocation and job transfers</strong> — Close in 7 days or coordinate timing with your move — your schedule, not ours</li>
      <li><strong>Vacant and abandoned properties</strong> — We buy vacant homes throughout {name} without requiring you to maintain or secure the property during the process</li>
    </ul>

    <h2>California-Specific Considerations for {name} Sellers</h2>
    <p>Selling a home in California involves specific legal and financial considerations that differ from other states. As experienced {county} home buyers, we handle all of these routinely:</p>
    <ul>
      <li><strong>California disclosure requirements</strong> — California sellers must complete extensive disclosure packages. We handle all required disclosures and don't ask you to dig up records you don't have</li>
      <li><strong>California Tenant Protection Act</strong> — If your {name} property has tenants, California AB 1482 and local ordinances govern how and when they can be asked to vacate. We take on that responsibility at closing</li>
      <li><strong>Capital gains considerations</strong> — Long-term {name} homeowners often have significant appreciation. We can refer you to a 1031 exchange specialist or tax advisor if needed before closing</li>
      <li><strong>Escrow process</strong> — California uses escrow companies rather than attorneys to close transactions. We work with reputable {county} escrow firms and cover standard closing costs on our end</li>
      <li><strong>HOA transfer requirements</strong> — Many {name} communities have HOA transfer fees, required documentation, and approval processes. We navigate these so you don't have to</li>
    </ul>

    <div class="cta-block">
      <h3>Questions About Selling Your {name} Home?</h3>
      <p>Call us at 949-280-5139 — we're happy to answer questions about the process, what your home might be worth, or anything else. No pressure, no obligation.</p>
      <a href="tel:9492805139">Call 949-280-5139</a>
    </div>

    <h2>What We Offer {name} Sellers</h2>
    <ul>
      <li>Fair cash offer based on current {name} market conditions and your property's specific location and condition</li>
      <li>Close in as few as 7 days, or on a longer timeline that works for your situation</li>
      <li>No repairs, cleaning, or staging required — we buy houses in any condition throughout {neighborhood_prose}</li>
      <li>Zero commissions, zero agent fees, zero closing costs on your side</li>
      <li>Experienced with complex situations including trust sales, probate, tenants, liens, and code violations</li>
      <li>Local {county} buyer — not a national call center or wholesale operation</li>
    </ul>

    <p>To learn more about selling your {name} home or to explore all your options, visit our <a href="{city_page_url}" style="color:#0f4a63;font-weight:600">{name} home buyers page</a>.</p>

  </div>

  <div class="sidebar">
    <div class="s-card">
      <h3>Get Your Free Cash Offer</h3>
      <p>No fees, no repairs. Close in 7 days or on your schedule.</p>
      <a href="tel:9492805139" class="s-phone">949-280-5139</a>
      <a href="/#offer" class="s-btn orange">Get Cash Offer</a>
      <a href="tel:9492805139" class="s-btn navy">Call Us Now</a>
    </div>
    <div class="s-card">
      <h3>ZIP Codes Served</h3>
      <p style="font-size:12px;color:#7a6a52;line-height:1.9;margin:0">{zip_str}</p>
    </div>
    <div class="s-card">
      <h3>Why Sell to Us?</h3>
      <ul class="trust-items">
        <li>Cash offer in 24 hours</li>
        <li>Close in as few as 7 days</li>
        <li>No repairs or cleaning</li>
        <li>Zero fees or commissions</li>
        <li>Tenants OK</li>
        <li>Any condition accepted</li>
        <li>{county} local buyer</li>
      </ul>
    </div>
    <div class="s-card">
      <h3>California Sellers</h3>
      <p style="font-size:12px;color:#7a6a52;line-height:1.7;margin:0">We handle tenant situations, probate, trust sales, HOA transfers, and all California-specific complexities so you don't have to.</p>
    </div>
  </div>
</div>

<footer>
  &copy; {YEAR} Golden Coast Cash Offer &middot; <a href="/">goldencoastcashoffer.com</a> &middot; 949-280-5139<br>
  Serving {name} and all of {county}, Southern California
</footer>

</body>
</html>"""


def main():
    output_base = Path("sell-my-house-fast")
    output_base.mkdir(exist_ok=True)

    generated = []
    for city in CITIES:
        folder = output_base / f"{city['slug']}-ca"
        folder.mkdir(exist_ok=True)
        html = build_page(city)
        out_file = folder / "index.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        generated.append(f"/sell-my-house-fast/{city['slug']}-ca/index.html")
        print(f"✓ {city['name']} → sell-my-house-fast/{city['slug']}-ca/index.html")

    print(f"\nGenerated {len(generated)} keyword landing pages")
    print("Upload the sell-my-house-fast/ folder to your repo root")
    print("\nSearch Console indexing priority order:")
    for city in CITIES[:10]:
        print(f"  https://www.goldencoastcashoffer.com/sell-my-house-fast-{city['slug']}-ca/")


if __name__ == "__main__":
    main()
