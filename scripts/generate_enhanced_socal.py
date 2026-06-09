#!/usr/bin/env python3
"""
Golden Coast Cash Offer — Complete Enhanced City Page Generator
All 90 cities with neighborhood-level detail.
Skips cities that already have enhanced pages (checks for neighborhood strip).
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
    {"slug":"ventura","name":"Ventura","county":"Ventura","zip":"93001","region":"Ventura County",
     "neighborhoods":["Downtown Ventura","Midtown","Westside","Pierpont Beach","Ventura Keys","Montalvo","Saticoy"],
     "landmarks":"San Buenaventura Mission, Ventura Pier, Channel Islands National Park gateway, Ventura Harbor",
     "market":"coastal city on the Pacific with a charming historic downtown, median home prices around $750k, gateway to Channel Islands",
     "seller_situations":"relocation, divorce, inherited coastal properties, landlords with long-term tenants, homes needing updates"},
    {"slug":"oxnard","name":"Oxnard","county":"Ventura","zip":"93030","region":"Ventura County",
     "neighborhoods":["Hollywood Beach","Silver Strand","Oxnard Shores","Colonia","Riverpark","Seabridge","Channel Islands Harbor"],
     "landmarks":"Channel Islands Harbor, Hollywood Beach, Carnegie Art Museum, Collection at RiverPark",
     "market":"largest city in Ventura County with beachfront community, large Latino population, median home prices around $650k",
     "seller_situations":"tired landlords, inherited properties, relocation, homes needing repairs, probate situations"},
    {"slug":"port-hueneme","name":"Port Hueneme","county":"Ventura","zip":"93041","region":"Ventura County",
     "neighborhoods":["Navy Housing area","Beach area","Central Port Hueneme","Hueneme Bay"],
     "landmarks":"Naval Base Ventura County, Port Hueneme Beach, Moranda Park",
     "market":"small beach city with naval base, affordable coastal housing, strong military community",
     "seller_situations":"military relocation, divorce, inherited properties, affordable entry-level homes"},
    {"slug":"camarillo","name":"Camarillo","county":"Ventura","zip":"93010","region":"Ventura County",
     "neighborhoods":["Old Town Camarillo","Mission Oaks","Camarillo Springs","Las Posas Estates","Tierra Vista","Sterling Hills"],
     "landmarks":"Camarillo Premium Outlets, CSUCI, Camarillo Airport, Old Town Camarillo",
     "market":"affluent inland Ventura city with premium outlets and upscale planned communities, median home prices around $800k",
     "seller_situations":"downsizing retirees, relocation, divorce, inherited properties, HOA-governed community sales"},
    {"slug":"thousand-oaks","name":"Thousand Oaks","county":"Ventura","zip":"91360","region":"Ventura County",
     "neighborhoods":["Lang Ranch","Wildwood","Lynn Ranch","Oakbrook Village","Conejo Valley","Dos Vientos","Newbury Park"],
     "landmarks":"Conejo Valley Botanic Garden, Janss Marketplace, Amgen HQ, Los Robles Hospital",
     "market":"one of safest US cities with large lots, highly rated schools, tech corridor, median home prices around $900k",
     "seller_situations":"corporate relocation, divorce, downsizing empty nesters, inherited properties, landlords exiting"},
    {"slug":"simi-valley","name":"Simi Valley","county":"Ventura","zip":"93065","region":"Ventura County",
     "neighborhoods":["Wood Ranch","Big Sky","Berylwood","Country Club Estates","Bridle Path","Oakridge Estates","Mountain Gate"],
     "landmarks":"Ronald Reagan Presidential Library, Simi Valley Town Center, Corriganville Park",
     "market":"suburban community with affordable family neighborhoods, median home prices around $650k",
     "seller_situations":"relocation, divorce, inherited properties, landlords, homes needing significant repairs"},
    {"slug":"ojai","name":"Ojai","county":"Ventura","zip":"93023","region":"Ventura County",
     "neighborhoods":["Downtown Ojai","Meiners Oaks","Mira Monte","Upper Ojai","Arbolada","East End"],
     "landmarks":"Ojai Valley Inn, Ojai Arcade, Meditation Mount, Ojai Music Festival",
     "market":"artsy mountain valley retreat with wellness tourism and unique hillside properties, median home prices around $850k",
     "seller_situations":"estate sales, trust sales, inherited unique properties, lifestyle change relocations, vacation home sales"},

    # ── Los Angeles County ─────────────────────────────────────────────────
    {"slug":"malibu","name":"Malibu","county":"Los Angeles","zip":"90265","region":"Los Angeles County",
     "neighborhoods":["Malibu Colony","Point Dume","Malibu Road","Broad Beach","Serra Retreat","Paradise Cove","Carbon Beach"],
     "landmarks":"PCH, Zuma Beach, Getty Villa, Nobu Malibu, Surfrider Beach",
     "market":"ultra-premium beachfront estates and celebrity enclave, median home prices above $3.5M",
     "seller_situations":"estate sales, trust and probate sales, divorce settlements, celebrity estate dispositions, out-of-state inheritors"},
    {"slug":"santa-monica","name":"Santa Monica","county":"Los Angeles","zip":"90401","region":"Los Angeles County",
     "neighborhoods":["Ocean Park","Sunset Park","North of Montana","Pico","Downtown Santa Monica","Mid-City Santa Monica"],
     "landmarks":"Santa Monica Pier, Third Street Promenade, Bergamot Station, Tongva Park",
     "market":"iconic pier city with high-end coastal real estate and tech hub, median home prices above $1.5M",
     "seller_situations":"divorce, relocation, inherited properties, trust sales, downsizing coastal homeowners"},
    {"slug":"los-angeles","name":"Los Angeles","county":"Los Angeles","zip":"90001","region":"Los Angeles County",
     "neighborhoods":["Silver Lake","Echo Park","Highland Park","Koreatown","Los Feliz","West Adams","Mid-Wilshire","Boyle Heights","Hancock Park","Leimert Park"],
     "landmarks":"Griffith Observatory, Getty Center, LACMA, Dodger Stadium, SoFi Stadium, Hollywood Sign",
     "market":"second-largest US city with incredibly diverse neighborhoods, median home prices around $900k citywide",
     "seller_situations":"divorce, inherited properties, landlords with tenant issues, relocation, probate, homes needing major repairs"},
    {"slug":"beverly-hills","name":"Beverly Hills","county":"Los Angeles","zip":"90210","region":"Los Angeles County",
     "neighborhoods":["Beverly Hills Flats","Beverly Hills Post Office","Trousdale Estates","Benedict Canyon","Bel-Air adjacent","Coldwater Canyon"],
     "landmarks":"Rodeo Drive, Beverly Hills Hotel, Wallis Annenberg Center, Beverly Gardens Park",
     "market":"world-famous luxury enclave with ultra-premium estates and global buyer demand, median home prices above $3M",
     "seller_situations":"estate sales, trust and probate sales, divorce involving high-value properties, out-of-state inheritors"},
    {"slug":"west-hollywood","name":"West Hollywood","county":"Los Angeles","zip":"90046","region":"Los Angeles County",
     "neighborhoods":["Sunset Strip","Design District","Santa Monica Blvd corridor","Norma Triangle","East WeHo","Laurel Canyon adjacent"],
     "landmarks":"Sunset Strip, Chateau Marmont, Pacific Design Center, Troubadour",
     "market":"vibrant nightlife and arts district with high condo density and strong rental market, median home prices around $1.2M",
     "seller_situations":"condo sales, divorce, relocation, landlords exiting the rental market, trust sales"},
    {"slug":"culver-city","name":"Culver City","county":"Los Angeles","zip":"90232","region":"Los Angeles County",
     "neighborhoods":["Downtown Culver City","Blanco","Fox Hills","West Culver City","Blair Hills","Carlson Park"],
     "landmarks":"Amazon Studios, Sony Pictures, Helms Bakery District, Platform LA",
     "market":"tech and entertainment hub with rapidly appreciating home values, median home prices around $1.1M",
     "seller_situations":"relocation, divorce, inherited properties, homeowners cashing out on appreciation"},
    {"slug":"inglewood","name":"Inglewood","county":"Los Angeles","zip":"90301","region":"Los Angeles County",
     "neighborhoods":["Morningside Park","Lockeford","Centinela","Hyde Park","Fairview Heights","Downtown Inglewood"],
     "landmarks":"SoFi Stadium, Kia Forum, Hollywood Park, Crenshaw/LAX Metro Line",
     "market":"rapidly gentrifying city with SoFi Stadium, strong investor demand, median home prices around $700k",
     "seller_situations":"investors cashing out, inherited properties, relocation, homes needing significant repairs"},
    {"slug":"hawthorne","name":"Hawthorne","county":"Los Angeles","zip":"90250","region":"Los Angeles County",
     "neighborhoods":["Holly Glen","El Camino Village","Bodger Park","Ramona","Wiseburn","Downtown Hawthorne"],
     "landmarks":"SpaceX HQ, LAX adjacent, In-N-Out Burger birthplace, South Bay Galleria",
     "market":"SpaceX headquarters city adjacent to LAX, rapidly developing South Bay community, median home prices around $750k",
     "seller_situations":"relocation, inherited properties, landlords, homes needing updates, investors"},
    {"slug":"gardena","name":"Gardena","county":"Los Angeles","zip":"90247","region":"Los Angeles County",
     "neighborhoods":["Western Gardena","Eastern Gardena","South Gardena","North Gardena","Gardens"],
     "landmarks":"Hollywood Park Casino nearby, Alondra Park, South Bay Galleria area",
     "market":"diverse South Bay community with large Japanese-American and Latino population, median home prices around $650k",
     "seller_situations":"aging homeowners, inherited properties, landlords, homes needing significant updates"},
    {"slug":"compton","name":"Compton","county":"Los Angeles","zip":"90220","region":"Los Angeles County",
     "neighborhoods":["North Compton","East Compton","West Compton","Richland Farms","Sunny Cove"],
     "landmarks":"Compton Courthouse, Martin Luther King Jr Park, Douglas Park",
     "market":"historically significant city in south LA with strong investor interest and affordable entry points, median home prices around $550k",
     "seller_situations":"inherited properties, probate, homes needing significant repairs, landlords, relocation"},
    {"slug":"carson","name":"Carson","county":"Los Angeles","zip":"90745","region":"Los Angeles County",
     "neighborhoods":["Dolphin Square","West Carson","East Carson","South Carson","Carson Park","Anza"],
     "landmarks":"Cal State Dominguez Hills, StubHub Center, South Bay Pavilion",
     "market":"South Bay community with diverse working-class neighborhoods, median home prices around $650k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, homes needing repairs"},
    {"slug":"el-segundo","name":"El Segundo","county":"Los Angeles","zip":"90245","region":"Los Angeles County",
     "neighborhoods":["Downtown El Segundo","North El Segundo","South El Segundo","El Segundo Beach area"],
     "landmarks":"LAX adjacent, Chevron headquarters, Raytheon, The Lakes shopping center",
     "market":"aerospace hub near LAX with tight-knit beach community and strong tech employment, median home prices around $1.1M",
     "seller_situations":"corporate relocation, divorce, inherited properties, downsizing"},
    {"slug":"manhattan-beach","name":"Manhattan Beach","county":"Los Angeles","zip":"90266","region":"Los Angeles County",
     "neighborhoods":["Sand Section","Tree Section","Hill Section","East Manhattan Beach","Liberty Village"],
     "landmarks":"Manhattan Beach Pier, Strand walkway, Metlox, Manhattan Village Mall",
     "market":"premier South Bay beach city with top schools and among priciest SoCal coastal markets, median home prices above $2.5M",
     "seller_situations":"estate sales, divorce settlements, trust sales, downsizing coastal homeowners, out-of-state inheritors"},
    {"slug":"hermosa-beach","name":"Hermosa Beach","county":"Los Angeles","zip":"90254","region":"Los Angeles County",
     "neighborhoods":["Downtown Hermosa","The Strand","Hermosa Valley","North Hermosa","South Hermosa"],
     "landmarks":"Hermosa Pier, Pier Avenue nightlife, The Strand walkway, Hermosa Beach Volleyball courts",
     "market":"vibrant beach community with walkable Pier Ave and strong vacation rental demand, median home prices above $1.8M",
     "seller_situations":"vacation rental sales, divorce, inherited beach properties, downsizing"},
    {"slug":"redondo-beach","name":"Redondo Beach","county":"Los Angeles","zip":"90277","region":"Los Angeles County",
     "neighborhoods":["North Redondo","South Redondo","Hollywood Riviera","Riviera Village","Admiralty","King Harbor"],
     "landmarks":"King Harbor, Redondo Beach Pier, Riviera Village, Veterans Park",
     "market":"South Bay beach city with harbor area and mix of condos and single-family homes, median home prices around $1.3M",
     "seller_situations":"divorce, inherited properties, landlords, relocation, downsizing coastal homeowners"},
    {"slug":"torrance","name":"Torrance","county":"Los Angeles","zip":"90501","region":"Los Angeles County",
     "neighborhoods":["Old Torrance","North Torrance","South Torrance","West Torrance","Walteria","Seaside","Hollywood Riviera"],
     "landmarks":"Del Amo Fashion Center, Toyota USA HQ, Torrance Beach, Wilson Park",
     "market":"South Bay community with large Japanese-American presence and strong auto industry, median home prices around $950k",
     "seller_situations":"corporate relocation, inherited properties, divorce, aging homeowners, landlords"},
    {"slug":"long-beach","name":"Long Beach","county":"Los Angeles","zip":"90802","region":"Los Angeles County",
     "neighborhoods":["Belmont Shore","Naples","Bixby Knolls","Wrigley","Signal Hill adjacent","Downtown Long Beach","Park Estates"],
     "landmarks":"Queen Mary, Aquarium of the Pacific, Port of Long Beach, Alamitos Bay",
     "market":"second-largest LA city with major port and diverse neighborhoods from historic to beachfront, median home prices around $750k",
     "seller_situations":"inherited properties, divorce, landlords, probate, relocation, homes needing repairs"},
    {"slug":"bellflower","name":"Bellflower","county":"Los Angeles","zip":"90706","region":"Los Angeles County",
     "neighborhoods":["East Bellflower","West Bellflower","North Bellflower","Downtown Bellflower"],
     "landmarks":"Bellflower Civic Center, Simms Park, Bellflower Towne Center",
     "market":"southeast LA county suburb with affordable housing and strong working-class community, median home prices around $600k",
     "seller_situations":"inherited properties, aging homeowners, relocation, homes needing updates, landlords"},
    {"slug":"paramount","name":"Paramount","county":"Los Angeles","zip":"90723","region":"Los Angeles County",
     "neighborhoods":["East Paramount","West Paramount","South Paramount","Paramount Industrial"],
     "landmarks":"Paramount City Hall, Cerritos College nearby, Foster Freeze",
     "market":"small southeast LA county city with industrial and residential mix and affordable homes, median home prices around $550k",
     "seller_situations":"inherited properties, landlords, relocation, homes needing repairs"},
    {"slug":"downey","name":"Downey","county":"Los Angeles","zip":"90241","region":"Los Angeles County",
     "neighborhoods":["North Downey","South Downey","West Downey","East Downey","Old Town Downey"],
     "landmarks":"NASA Armstrong Flight Research Center museum, Downey Landing, Wilderness Park",
     "market":"southeast LA county with NASA history and diverse working-class community, median home prices around $650k",
     "seller_situations":"inherited properties, divorce, relocation, landlords, aging homeowners"},
    {"slug":"norwalk","name":"Norwalk","county":"Los Angeles","zip":"90650","region":"Los Angeles County",
     "neighborhoods":["North Norwalk","South Norwalk","West Norwalk","East Norwalk","Studebaker"],
     "landmarks":"Cerritos College, Norwalk Civic Center, Town Square",
     "market":"southeast LA county with Cerritos border and large Hispanic community, median home prices around $600k",
     "seller_situations":"inherited older homes, landlords, relocation, divorce, homes needing significant updates"},
    {"slug":"cerritos","name":"Cerritos","county":"Los Angeles","zip":"90703","region":"Los Angeles County",
     "neighborhoods":["North Cerritos","South Cerritos","West Cerritos","East Cerritos"],
     "landmarks":"Cerritos Auto Square, Cerritos Center for the Performing Arts, Cerritos Public Library",
     "market":"highly rated schools with diverse affluent suburb and strong Korean and Filipino community, median home prices around $900k",
     "seller_situations":"downsizing empty nesters, inherited properties, relocation, divorce"},
    {"slug":"lakewood","name":"Lakewood","county":"Los Angeles","zip":"90712","region":"Los Angeles County",
     "neighborhoods":["East Lakewood","West Lakewood","North Lakewood","South Lakewood","Lakewood Village"],
     "landmarks":"Lakewood Center Mall, Del Valle Park, Bolivar Park",
     "market":"one of first planned communities in US with post-WWII suburb character, median home prices around $700k",
     "seller_situations":"aging original homeowners, inherited properties, divorce, relocation, homes needing updates"},
    {"slug":"whittier","name":"Whittier","county":"Los Angeles","zip":"90601","region":"Los Angeles County",
     "neighborhoods":["Uptown Whittier","East Whittier","South Whittier","North Whittier","Friendly Hills","Murphy Ranch"],
     "landmarks":"Whittier Uptown district, Nixon birthplace nearby, Whittier College, Rose Hills Memorial Park",
     "market":"historic Uptown, birthplace of Nixon, affordable southeast LA county, median home prices around $650k",
     "seller_situations":"aging homeowners, inherited properties, divorce, relocation, homes needing repairs"},
    {"slug":"el-monte","name":"El Monte","county":"Los Angeles","zip":"91731","region":"Los Angeles County",
     "neighborhoods":["North El Monte","South El Monte","Central El Monte","Garvey","Durfee"],
     "landmarks":"El Monte Airport, Whittier Narrows Recreation Area, Azteca Stadium",
     "market":"San Gabriel Valley city with large Latino community and older housing stock, median home prices around $600k",
     "seller_situations":"inherited older homes, landlords, divorce, homes needing significant repairs, probate"},
    {"slug":"west-covina","name":"West Covina","county":"Los Angeles","zip":"91790","region":"Los Angeles County",
     "neighborhoods":["West Covina Hills","East West Covina","South West Covina","Woodside Village","Sunset Hills"],
     "landmarks":"West Covina Fashion Plaza, Galster Wilderness Park, Lark Ellen Village",
     "market":"San Gabriel Valley suburb with diverse community and mix of ranch homes and newer developments, median home prices around $650k",
     "seller_situations":"divorce, inherited properties, relocation, aging homeowners, landlords"},
    {"slug":"alhambra","name":"Alhambra","county":"Los Angeles","zip":"91801","region":"Los Angeles County",
     "neighborhoods":["North Alhambra","South Alhambra","West Alhambra","Downtown Alhambra","Midwick Tract"],
     "landmarks":"Almansor Park, Alhambra Theatre, Valley Blvd restaurant row, Main Street corridor",
     "market":"San Gabriel Valley with large Chinese-American community and close proximity to downtown LA, median home prices around $700k",
     "seller_situations":"inherited properties, aging homeowners, divorce, landlords, homes needing updates"},
    {"slug":"monterey-park","name":"Monterey Park","county":"Los Angeles","zip":"91754","region":"Los Angeles County",
     "neighborhoods":["North Monterey Park","South Monterey Park","Garvey Corridor","Atlantic corridor"],
     "landmarks":"Monterey Park City Hall, Barnes Park, Atlantic Times Square",
     "market":"first suburban Chinatown in the US with dense diverse community, median home prices around $700k",
     "seller_situations":"inherited properties, aging homeowners, divorce, estate sales, relocation"},
    {"slug":"arcadia","name":"Arcadia","county":"Los Angeles","zip":"91006","region":"Los Angeles County",
     "neighborhoods":["Baldwin Stocker","Rancho Santa Anita","Highland Oaks","Foothill","Arcadia Gardens","Santa Anita"],
     "landmarks":"Santa Anita Park racetrack, Westfield Santa Anita, LA Arboretum, Arcadia Wilderness Park",
     "market":"affluent San Gabriel Valley with Santa Anita Park and large Chinese-American community, median home prices around $1M",
     "seller_situations":"estate sales, trust sales, inherited properties, divorce, downsizing empty nesters"},
    {"slug":"pasadena","name":"Pasadena","county":"Los Angeles","zip":"91101","region":"Los Angeles County",
     "neighborhoods":["Caltech area","Old Pasadena","Rose Bowl area","Bungalow Heaven","Madison Heights","Hastings Ranch","San Rafael Hills"],
     "landmarks":"Rose Bowl, Caltech, Huntington Library, Norton Simon Museum, Colorado Blvd",
     "market":"Rose Bowl city with Caltech and beautiful craftsman homes in an affluent historic community, median home prices around $1.1M",
     "seller_situations":"estate sales, trust sales, inherited craftsman homes, divorce, relocation"},
    {"slug":"glendale","name":"Glendale","county":"Los Angeles","zip":"91201","region":"Los Angeles County",
     "neighborhoods":["Montrose","Crescenta Valley","Adams Hill","Verdugo Woodlands","Glenoaks Canyon","Downtown Glendale","Chevy Chase Canyon"],
     "landmarks":"Americana at Brand, Glendale Galleria, Forest Lawn Memorial Park, Brand Park",
     "market":"large Armenian-American community with diverse city north of LA and hillside properties, median home prices around $900k",
     "seller_situations":"estate sales, inherited properties, divorce, aging homeowners, relocation"},
    {"slug":"burbank","name":"Burbank","county":"Los Angeles","zip":"91502","region":"Los Angeles County",
     "neighborhoods":["Media District","Magnolia Park","Downtown Burbank","Rancho","Hillside","Starlight Hills"],
     "landmarks":"Warner Bros Studios, Disney Animation, NBC Studios, Burbank Airport, Magnolia Park",
     "market":"media capital with Disney and Warner Bros presence, median home prices around $900k",
     "seller_situations":"corporate relocation, divorce, inherited properties, downsizing, trust sales"},
    {"slug":"santa-clarita","name":"Santa Clarita","county":"Los Angeles","zip":"91350","region":"Los Angeles County",
     "neighborhoods":["Valencia","Stevenson Ranch","Newhall","Saugus","Canyon Country","Castaic"],
     "landmarks":"Six Flags Magic Mountain, College of the Canyons, Old Town Newhall, Vasquez Rocks",
     "market":"master-planned communities with family-oriented culture and one of safest large CA cities, median home prices around $750k",
     "seller_situations":"relocation, divorce, inherited properties, downsizing, landlords exiting"},
    {"slug":"pomona","name":"Pomona","county":"Los Angeles","zip":"91766","region":"Los Angeles County",
     "neighborhoods":["Lincoln Park","Westmont","Downtown Pomona","Arenas","Garey","Towne","Ganesha Hills"],
     "landmarks":"Cal Poly Pomona, LA County Fairplex, Fox Theater Pomona, Palomares Hills",
     "market":"inland LA county with Cal Poly Pomona and diverse working-class community, median home prices around $550k",
     "seller_situations":"inherited properties, divorce, homes needing repairs, landlords, relocation"},

    # ── Orange County ──────────────────────────────────────────────────────
    {"slug":"seal-beach","name":"Seal Beach","county":"Orange","zip":"90740","region":"Orange County",
     "neighborhoods":["Old Town Seal Beach","Leisure World","College Park East","College Park West","Surfside"],
     "landmarks":"Seal Beach Pier, Old Town Main Street, Leisure World retirement community, Naval Weapons Station",
     "market":"small beach town with Leisure World senior community and charming coastal village, median home prices around $900k",
     "seller_situations":"retirees downsizing from Leisure World, inherited properties, relocation, divorce"},
    {"slug":"huntington-beach","name":"Huntington Beach","county":"Orange","zip":"92648","region":"Orange County",
     "neighborhoods":["Downtown HB","Huntington Harbour","Bolsa Chica","Seacliff","Pacific Ranch","Meadowlark","South HB","Tri Pointe"],
     "landmarks":"HB Pier, Pacific City, Bolsa Chica Ecological Reserve, US Open of Surfing venue",
     "market":"Surf City USA with strong mix of beachfront condos and single-family homes, median home prices around $1.1M",
     "seller_situations":"tired landlords with coastal rental properties, divorce, relocation, older beach cottages needing major updates"},
    {"slug":"fountain-valley","name":"Fountain Valley","county":"Orange","zip":"92708","region":"Orange County",
     "neighborhoods":["West Fountain Valley","East Fountain Valley","Mile Square Park area","Ward Street corridor","Brookhurst corridor"],
     "landmarks":"Mile Square Regional Park, Fountain Valley Recreation Center, Coastline Community College",
     "market":"quiet City of Pleasant Living with mix of 1960s-1980s ranch homes and strong school district, median home prices around $900k",
     "seller_situations":"aging original homeowners, inherited properties, families relocating out of state"},
    {"slug":"westminster","name":"Westminster","county":"Orange","zip":"92683","region":"Orange County",
     "neighborhoods":["Little Saigon","Westminster Center","Sigler Park","Springdale","Westminster Village","Golden West"],
     "landmarks":"Little Saigon district, Westminster Mall, Bolsa Ave corridor, Sid Goldstein Freedom Park",
     "market":"home to the largest Vietnamese-American community outside Vietnam with affordable OC housing, median home prices around $800k",
     "seller_situations":"aging homeowners, inherited properties, landlords with long-term tenants, quick sale needs"},
    {"slug":"garden-grove","name":"Garden Grove","county":"Orange","zip":"92840","region":"Orange County",
     "neighborhoods":["Historic Main Street","West Garden Grove","East Garden Grove","Euclid corridor","Chapman corridor","Brookhurst area"],
     "landmarks":"Crystal Cathedral, Garden Grove Historic Main Street, Strawberry Festival grounds",
     "market":"diverse north OC city with large Vietnamese and Korean communities and affordable older housing, median home prices around $800k",
     "seller_situations":"older homeowners, inherited properties, homes with deferred maintenance, landlords ready to exit"},
    {"slug":"cypress","name":"Cypress","county":"Orange","zip":"90630","region":"Orange County",
     "neighborhoods":["North Cypress","South Cypress","Cypress Business Park area","Katella corridor"],
     "landmarks":"Cypress College, Los Alamitos Race Course, Cypress Community Center",
     "market":"small north OC city with well-maintained neighborhoods and strong schools, median home prices around $850k",
     "seller_situations":"downsizing empty nesters, inherited properties, relocation, divorce"},
    {"slug":"buena-park","name":"Buena Park","county":"Orange","zip":"92620","region":"Orange County",
     "neighborhoods":["North Buena Park","South Buena Park","Entertainment Corridor","Whitaker","La Palma adjacent"],
     "landmarks":"Knott's Berry Farm, Medieval Times, Hobby City, Beach Blvd entertainment corridor",
     "market":"Knott's Berry Farm city with diverse north OC community, median home prices around $800k",
     "seller_situations":"landlord fatigue near entertainment corridor, inherited properties, divorce, relocation"},
    {"slug":"la-habra","name":"La Habra","county":"Orange","zip":"90631","region":"Orange County",
     "neighborhoods":["North La Habra","South La Habra","East La Habra","La Habra Heights adjacent","Downtown La Habra"],
     "landmarks":"La Habra Depot Theatre, Children's Museum at La Habra, Portola Park",
     "market":"north OC border city with large Latino community and affordable older housing stock, median home prices around $750k",
     "seller_situations":"aging homeowners, inherited properties, divorce, landlords, relocation"},
    {"slug":"brea","name":"Brea","county":"Orange","zip":"92821","region":"Orange County",
     "neighborhoods":["North Brea","South Brea","Downtown Brea","Carbon Canyon","Olinda Village","Tonner Canyon"],
     "landmarks":"Brea Mall, Downtown Brea arts district, Craig Regional Park, Brea Community Center",
     "market":"upscale north OC city with oil heritage and newer master-planned communities, median home prices around $850k",
     "seller_situations":"downsizing empty nesters, inherited properties, relocation, divorce, trust sales"},
    {"slug":"yorba-linda","name":"Yorba Linda","county":"Orange","zip":"92886","region":"Orange County",
     "neighborhoods":["East Lake","Travis Ranch","Stonehaven","Vista Del Verde","Camino del Norte","Fairmont","Lemon Cove"],
     "landmarks":"Richard Nixon Presidential Library, Yorba Linda Town Center, Carbon Canyon Regional Park",
     "market":"birthplace of Nixon with affluent north OC, large lots and equestrian properties, median home prices around $1M",
     "seller_situations":"downsizing from large estates, inherited properties, divorce, relocation, trust sales"},
    {"slug":"placentia","name":"Placentia","county":"Orange","zip":"92870","region":"Orange County",
     "neighborhoods":["North Placentia","South Placentia","Downtown Placentia","Placentia Linda","Golden Heritage"],
     "landmarks":"Placentia Heritage Museum, Tri-City Park, Bradford Ave corridor",
     "market":"north OC suburb with family-friendly character and mix of older and newer residential developments, median home prices around $800k",
     "seller_situations":"aging homeowners, inherited properties, divorce, relocation, landlords"},
    {"slug":"newport-beach","name":"Newport Beach","county":"Orange","zip":"92660","region":"Orange County",
     "neighborhoods":["Corona del Mar","Balboa Island","Newport Coast","Lido Isle","Balboa Peninsula","Dover Shores","Eastbluff","Crystal Cove","Harbor View"],
     "landmarks":"Fashion Island, Pelican Hill Resort, Newport Harbor, Crystal Cove State Park, Balboa Pier",
     "market":"among California's most expensive coastal markets, median home prices above $3M",
     "seller_situations":"estate sales, trust and probate properties, divorce settlements, out-of-state inheritors"},
    {"slug":"costa-mesa","name":"Costa Mesa","county":"Orange","zip":"92626","region":"Orange County",
     "neighborhoods":["Eastside Costa Mesa","Westside Costa Mesa","South Coast Metro","Mesa Verde","College Park","Harbor View"],
     "landmarks":"South Coast Plaza, Segerstrom Center for the Arts, OC Fairgrounds, Metro Pointe",
     "market":"arts and shopping hub near Newport Beach with mix of older homes and new condos, median home prices around $1M",
     "seller_situations":"landlords, divorce, relocation, inherited properties, homes needing updates"},
    {"slug":"laguna-beach","name":"Laguna Beach","county":"Orange","zip":"92651","region":"Orange County",
     "neighborhoods":["Arch Beach Heights","Three Arch Bay","Emerald Bay","Bluebird Canyon","Temple Hills","South Laguna","Top of the World"],
     "landmarks":"Pageant of the Masters, Heisler Park, Main Beach, Festival of Arts",
     "market":"premier arts colony with dramatic coastal bluffs, among most expensive in SoCal, median home prices above $2.5M",
     "seller_situations":"estate sales, trust sales, inherited coastal properties, divorce, out-of-state inheritors"},
    {"slug":"laguna-hills","name":"Laguna Hills","county":"Orange","zip":"92653","region":"Orange County",
     "neighborhoods":["Nellie Gail Ranch","Moulton Ranch","Sheep Hills","Heritage Fields","Laguna Hills Mall area","Aliso border communities"],
     "landmarks":"Laguna Hills Mall, Saddleback Memorial Medical Center, Aliso and Wood Canyons Wilderness Park",
     "market":"family-oriented south OC community with mix of 1980s-2000s single-family homes, median home prices around $900k",
     "seller_situations":"families relocating, inherited properties, divorce, homeowners facing repair costs"},
    {"slug":"laguna-niguel","name":"Laguna Niguel","county":"Orange","zip":"92677","region":"Orange County",
     "neighborhoods":["Bear Brand Ranch","Marina Hills","Laguna Sur","Ocean Ranch","Salt Creek","Beacon Hill","Aliso Viejo adjacent"],
     "landmarks":"Ritz-Carlton Laguna Niguel, Salt Creek Beach, Laguna Niguel Regional Park",
     "market":"affluent planned community with ocean views and upscale residential neighborhoods, median home prices around $1.2M",
     "seller_situations":"downsizing retirees, inherited properties, divorce, relocation, trust sales"},
    {"slug":"laguna-woods","name":"Laguna Woods","county":"Orange","zip":"92637","region":"Orange County",
     "neighborhoods":["Village One","Village Two","Village Three","Casta del Sol","Gate 1","Gate 11","Gate 14"],
     "landmarks":"Laguna Woods Village gates, Laguna Woods Golf Club, Community Center",
     "market":"55+ retirement community with large active senior population and condo-heavy market, median prices around $500k",
     "seller_situations":"retirees downsizing or moving to assisted living, estate sales, inherited senior community properties"},
    {"slug":"aliso-viejo","name":"Aliso Viejo","county":"Orange","zip":"92656","region":"Orange County",
     "neighborhoods":["Pacific Ridge","Glenwood","Aliso Viejo Town Center","Canyon Vistas","Pacific Park","Wood Canyon"],
     "landmarks":"Aliso Viejo Town Center, Wood Canyon Wilderness Park, Soka University",
     "market":"planned south OC community with young professional demographic and strong condo market, median home prices around $800k",
     "seller_situations":"young professionals relocating, divorce, inherited HOA properties, landlords"},
    {"slug":"lake-forest","name":"Lake Forest","county":"Orange","zip":"92630","region":"Orange County",
     "neighborhoods":["El Toro","Portola Hills","Foothill Ranch","Baker Ranch","Serrano","Aliso Creek"],
     "landmarks":"El Toro Air Museum, Whiting Ranch Wilderness Park, Etnies Skatepark",
     "market":"large OC suburb with mix of older El Toro homes and newer Baker Ranch developments, median home prices around $900k",
     "seller_situations":"relocation, inherited older El Toro properties, divorce, families upgrading or downsizing"},
    {"slug":"mission-viejo","name":"Mission Viejo","county":"Orange","zip":"92691","region":"Orange County",
     "neighborhoods":["Mission Viejo North","Mission Viejo South","Lake Mission Viejo area","Aegean Hills","Painted Trails","Olympiad area","Marguerite corridor"],
     "landmarks":"Lake Mission Viejo, Saddleback College, Oso Creek Trail, Saddleback Memorial Medical Center",
     "market":"award-winning master-planned community with predominantly single-family HOA homes, median home prices around $950k",
     "seller_situations":"retirees downsizing, inherited HOA properties, divorce, homeowners relocating out of SoCal"},
    {"slug":"rancho-santa-margarita","name":"Rancho Santa Margarita","county":"Orange","zip":"92688","region":"Orange County",
     "neighborhoods":["Melinda Heights","Trabuco Highlands","Coto de Caza adjacent","Las Flores","Tijeras Creek","Dove Canyon"],
     "landmarks":"Rancho Santa Margarita Lake, O'Neill Regional Park, Tijeras Creek Golf Club",
     "market":"planned community in Saddleback Valley with family-friendly neighborhoods and strong HOA culture, median home prices around $900k",
     "seller_situations":"relocation, divorce, inherited HOA properties, downsizing empty nesters"},
    {"slug":"trabuco-canyon","name":"Trabuco Canyon","county":"Orange","zip":"92679","region":"Orange County",
     "neighborhoods":["Robinson Ranch","Portola Hills","Wagon Wheel","Las Flores","Plano Trabuco","Rose Canyon"],
     "landmarks":"O'Neill Regional Park, Trabuco Canyon Road, Holy Jim Falls, Irvine Lake",
     "market":"rural unincorporated OC community with horse properties and large lots in scenic canyon setting, median home prices around $850k",
     "seller_situations":"horse property sales, estate sales, inherited rural properties, relocation, divorce"},
    {"slug":"foothill-ranch","name":"Foothill Ranch","county":"Orange","zip":"92610","region":"Orange County",
     "neighborhoods":["Foothill Ranch Town Centre area","Montecido","Ironwood","Saddleback Valley","Whiting Ranch adjacent"],
     "landmarks":"Whiting Ranch Wilderness Park, Foothill Ranch Town Centre, Etnies Skatepark",
     "market":"master-planned community in Lake Forest with newer homes and close access to Whiting Ranch trails, median home prices around $850k",
     "seller_situations":"relocation, divorce, inherited properties, young families upgrading"},
    {"slug":"dana-point","name":"Dana Point","county":"Orange","zip":"92629","region":"Orange County",
     "neighborhoods":["Dana Point Harbor","Monarch Beach","Lantern District","Capistrano Beach","Baby Beach","Strand Beach","Dana Hills"],
     "landmarks":"Dana Point Harbor, Doheny State Beach, Ocean Institute, Lantern District restaurants",
     "market":"harbor city and whale watching capital with coastal premium properties, median home prices above $1.2M",
     "seller_situations":"estate sales, divorce, inherited coastal properties, relocation, trust sales"},
    {"slug":"san-juan-capistrano","name":"San Juan Capistrano","county":"Orange","zip":"92675","region":"Orange County",
     "neighborhoods":["Historic Los Rios District","Mission Hills","Forster Ranch","Rancho Ortega","Marbella","San Juan Hills"],
     "landmarks":"Mission San Juan Capistrano, Los Rios Historic District, Swallows Inn, Zoomars Petting Farm",
     "market":"historic mission city with equestrian community, charming Old Town and rural properties, median home prices around $1M",
     "seller_situations":"estate sales, inherited equestrian properties, divorce, relocation, trust sales"},
    {"slug":"san-clemente","name":"San Clemente","county":"Orange","zip":"92672","region":"Orange County",
     "neighborhoods":["North Beach","Southeast San Clemente","Southwest San Clemente","Marblehead","Talega","Highland Light Estates"],
     "landmarks":"San Clemente Pier, Talega Golf Club, San Clemente State Beach, Ole Hanson Beach Club",
     "market":"Spanish Village by the Sea with coastal community near Camp Pendleton, median home prices around $1.1M",
     "seller_situations":"military relocation, divorce, inherited coastal properties, estate sales, trust sales"},
    {"slug":"irvine","name":"Irvine","county":"Orange","zip":"92618","region":"Orange County",
     "neighborhoods":["Woodbridge","Northwood","Westpark","Turtle Rock","Shady Canyon","Orchard Hills","Stonegate","Quail Hill","University Park","Portola Springs"],
     "landmarks":"UC Irvine, Irvine Spectrum Center, Orange County Great Park, John Wayne Airport",
     "market":"one of the most affluent planned cities in the US, median home prices above $1.1M",
     "seller_situations":"divorce, job relocation, inherited HOA-governed properties, landlords dealing with California tenant laws"},
    {"slug":"tustin","name":"Tustin","county":"Orange","zip":"92780","region":"Orange County",
     "neighborhoods":["Old Town Tustin","Tustin Ranch","Tustin Legacy","Columbus Square","Greenwood","Laurelwood"],
     "landmarks":"Old Town Tustin historic district, Tustin Legacy development, MCAS Tustin blimp hangars",
     "market":"mix of historic Old Town and newer Tustin Ranch developments with great OC location, median home prices around $900k",
     "seller_situations":"relocation, inherited Old Town properties, divorce, landlords, downsizing"},
    {"slug":"orange","name":"Orange","county":"Orange","zip":"92868","region":"Orange County",
     "neighborhoods":["Old Towne Orange","Orange Hills","Serrano Heights","Villa Park adjacent","El Modena","Olive"],
     "landmarks":"Old Towne Orange historic district, Chapman University, Orange Circle, Irvine Regional Park",
     "market":"historic Old Towne Orange with antique district and mix of Victorian and modern homes, median home prices around $850k",
     "seller_situations":"inherited historic homes, divorce, relocation, aging homeowners, homes needing restoration"},
    {"slug":"santa-ana","name":"Santa Ana","county":"Orange","zip":"92701","region":"Orange County",
     "neighborhoods":["Floral Park","Wilshire Square","Park Santiago","South Main","Metro East","Delhi","Cornerstone Village","Logan Barrio"],
     "landmarks":"Bowers Museum, Santa Ana Zoo, Discovery Cube OC, Orange County Courthouse",
     "market":"Orange County seat with large Hispanic community and older housing stock from 1940s-1970s, median home prices around $700k",
     "seller_situations":"inherited older homes, probate situations, properties with deferred maintenance, landlords with tenant issues"},
    {"slug":"anaheim","name":"Anaheim","county":"Orange","zip":"92801","region":"Orange County",
     "neighborhoods":["Anaheim Hills","Platinum Triangle","Historic Downtown","West Anaheim","Canyon Area","Brookhurst Community","River Valley"],
     "landmarks":"Disneyland Resort, Angel Stadium, Honda Center, Anaheim Convention Center",
     "market":"OC's largest city with diverse neighborhoods from affordable West Anaheim to upscale Anaheim Hills, median home prices around $800k",
     "seller_situations":"landlord fatigue with vacation rentals, inherited properties, divorce, homes needing updates"},
    {"slug":"fullerton","name":"Fullerton","county":"Orange","zip":"92832","region":"Orange County",
     "neighborhoods":["Downtown Fullerton","Sunny Hills","Amerige Heights","Coyote Hills","Golden Hills","Fullerton Hills"],
     "landmarks":"Cal State Fullerton, Fullerton Arboretum, Downtown Fullerton arts scene, Muckenthaler Cultural Center",
     "market":"college town with Cal State Fullerton and historic downtown and diverse housing stock, median home prices around $850k",
     "seller_situations":"relocation, inherited properties, divorce, aging homeowners, landlords near CSUF"},
    {"slug":"stanton","name":"Stanton","county":"Orange","zip":"90680","region":"Orange County",
     "neighborhoods":["North Stanton","South Stanton","Cypress adjacent","Katella corridor","Western Stanton"],
     "landmarks":"Stanton Central Park, Grovedale Park, Stanton Community Center",
     "market":"small dense north OC city with very affordable entry-level homes, median home prices around $700k",
     "seller_situations":"inherited older homes, landlords, divorce, relocation, first-time seller situations"},

    # ── Inland Empire ──────────────────────────────────────────────────────
    {"slug":"riverside","name":"Riverside","county":"Riverside","zip":"92501","region":"Inland Empire",
     "neighborhoods":["Wood Streets","Alessandro Heights","Orangecrest","Canyon Crest","Victoria","La Sierra","Downtown Riverside"],
     "landmarks":"Mission Inn, UC Riverside, Riverside Art Museum, National Orange Show grounds",
     "market":"UC Riverside city with historic Mission Inn and gateway to Inland Empire, median home prices around $550k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, homes needing repairs"},
    {"slug":"corona","name":"Corona","county":"Riverside","zip":"92879","region":"Inland Empire",
     "neighborhoods":["Eagle Glen","Dos Lagos","Temescal Valley","South Corona","North Corona","Sierra Del Oro","Coronita"],
     "landmarks":"Dos Lagos shopping center, Glen Ivy Hot Springs, Eagle Glen Golf Club, Prado Regional Park",
     "market":"fast-growing suburb with strong commuter base to OC and LA, median home prices around $650k",
     "seller_situations":"relocation, divorce, inherited properties, landlords, upgrading families"},
    {"slug":"murrieta","name":"Murrieta","county":"Riverside","zip":"92562","region":"Inland Empire",
     "neighborhoods":["Murrieta Hot Springs","West Murrieta","Central Murrieta","French Valley","Copper Canyon","Shea Homes"],
     "landmarks":"Murrieta Hot Springs Resort, California Oaks Sports Park, Murrieta Town Square",
     "market":"one of fastest-growing SW Riverside cities with excellent schools and master-planned communities, median home prices around $650k",
     "seller_situations":"relocation, divorce, inherited properties, upgrading families, new construction competition"},
    {"slug":"temecula","name":"Temecula","county":"Riverside","zip":"92590","region":"Inland Empire",
     "neighborhoods":["Old Town Temecula","Wine Country","Redhawk","Paloma del Sol","Harveston","Roripaugh Ranch","Crowne Hill"],
     "landmarks":"Temecula Wine Country, Old Town Temecula, Pechanga Resort, Promenade Mall",
     "market":"wine country destination with Old Town charm and strong tourism and residential growth, median home prices around $650k",
     "seller_situations":"relocation, vacation home sales, divorce, inherited properties, downsizing"},
    {"slug":"menifee","name":"Menifee","county":"Riverside","zip":"92584","region":"Inland Empire",
     "neighborhoods":["Sun City","Quail Valley","Romoland","Murrieta Road corridor","McCall Blvd area","Audie Murphy Ranch"],
     "landmarks":"Menifee Lakes Country Club, Sun City Community Center, Menifee Town Center",
     "market":"one of California's fastest-growing cities with large master-planned communities, median home prices around $550k",
     "seller_situations":"relocation, inherited properties, divorce, upgrading families, new construction competition"},
    {"slug":"lake-elsinore","name":"Lake Elsinore","county":"Riverside","zip":"92530","region":"Inland Empire",
     "neighborhoods":["Lakeside","Canyon Hills","Summerly","Rosetta Canyon","Mission Trail","Alberhill"],
     "landmarks":"Lake Elsinore, Diamond Stadium, Lake Elsinore Outlets, Skydive Elsinore",
     "market":"lakeside city with outdoor recreation and affordable entry-level homes, median home prices around $500k",
     "seller_situations":"relocation, inherited lake properties, divorce, landlords, first-time seller situations"},
    {"slug":"ontario","name":"Ontario","county":"San Bernardino","zip":"91761","region":"Inland Empire",
     "neighborhoods":["Ontario Ranch","Vineyard","Creekside","Downtown Ontario","Mountain View","East Ontario"],
     "landmarks":"Ontario International Airport, Ontario Mills Mall, Citizens Business Bank Arena",
     "market":"major logistics hub with Ontario Airport and diverse affordable housing market, median home prices around $550k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, industrial area homeowners"},
    {"slug":"rancho-cucamonga","name":"Rancho Cucamonga","county":"San Bernardino","zip":"91730","region":"Inland Empire",
     "neighborhoods":["Alta Loma","Etiwanda","Deer Creek","Day Creek","Vintage","Victoria Groves","Carriage Estates"],
     "landmarks":"Victoria Gardens, Ontario Mills nearby, Cucamonga-Guasti Regional Park, LoanMart Field",
     "market":"affluent IE suburb with Victoria Gardens and top-rated schools and mountain views, median home prices around $700k",
     "seller_situations":"relocation, divorce, inherited properties, downsizing empty nesters, trust sales"},

    # ── San Diego County ───────────────────────────────────────────────────
    {"slug":"oceanside","name":"Oceanside","county":"San Diego","zip":"92054","region":"San Diego County",
     "neighborhoods":["Downtown Oceanside","Fire Mountain","South Oceanside","North Coastal","Peacock Hills","Eastside Oceanside"],
     "landmarks":"Oceanside Pier, Camp Pendleton adjacent, Oceanside Harbor, California Surf Museum",
     "market":"military city near Camp Pendleton with beach access and diverse housing, median home prices around $700k",
     "seller_situations":"military relocation (PCS orders), divorce, inherited properties, landlords, homes needing updates"},
    {"slug":"vista","name":"Vista","county":"San Diego","zip":"92083","region":"San Diego County",
     "neighborhoods":["North Vista","South Vista","Shadowridge","Buena Creek","Rancho Minerva","Downtown Vista"],
     "landmarks":"Moonlight Amphitheatre, Avo Playhouse, Wave Waterpark",
     "market":"north county inland city with diverse community and affordable housing, median home prices around $650k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, homes needing repairs"},
    {"slug":"san-marcos","name":"San Marcos","county":"San Diego","zip":"92069","region":"San Diego County",
     "neighborhoods":["San Elijo Hills","Nordahl Road corridor","Twin Oaks Valley","Discovery Hills","Old Creek Ranch","University District"],
     "landmarks":"Cal State San Marcos, Lake San Marcos, Twin Oaks Golf Course, Discovery Lake",
     "market":"fast-growing north county city with Cal State San Marcos and master-planned communities, median home prices around $750k",
     "seller_situations":"relocation, inherited properties, divorce, upgrading families, new construction competition"},
    {"slug":"carlsbad","name":"Carlsbad","county":"San Diego","zip":"92008","region":"San Diego County",
     "neighborhoods":["Carlsbad Village","La Costa","Aviara","Pacific Rim","Bressi Ranch","Calavera Hills","Olde Carlsbad"],
     "landmarks":"LEGOLAND California, Flower Fields, Carlsbad Premium Outlets, Carlsbad State Beach",
     "market":"upscale coastal north county with LEGOLAND and premium beachside properties, median home prices around $1.2M",
     "seller_situations":"relocation, estate sales, divorce, inherited properties, trust sales"},
    {"slug":"encinitas","name":"Encinitas","county":"San Diego","zip":"92024","region":"San Diego County",
     "neighborhoods":["Cardiff-by-the-Sea","Leucadia","Olivenhain","New Encinitas","Old Encinitas","Moonlight Beach area"],
     "landmarks":"Swami's surf break, Self-Realization Fellowship, Moonlight Beach, San Diego Botanic Garden",
     "market":"surf culture with flower fields and coastal bluffs in upscale north county community, median home prices around $1.3M",
     "seller_situations":"estate sales, trust sales, inherited coastal properties, divorce, relocation"},
    {"slug":"solana-beach","name":"Solana Beach","county":"San Diego","zip":"92075","region":"San Diego County",
     "neighborhoods":["Lomas Santa Fe","Del Mar Heights adjacent","Solana Beach coastal","La Colonia"],
     "landmarks":"Fletcher Cove Beach Park, Cedros Design District, Del Mar Racetrack adjacent",
     "market":"small affluent coastal community with Fletcher Cove and premium beachfront values, median home prices above $1.5M",
     "seller_situations":"estate sales, trust sales, divorce, inherited coastal properties, out-of-state inheritors"},
    {"slug":"del-mar","name":"Del Mar","county":"San Diego","zip":"92014","region":"San Diego County",
     "neighborhoods":["Del Mar Village","Powerhouse Park area","Del Mar Heights","North Del Mar","Rancho Del Mar"],
     "landmarks":"Del Mar Racetrack, Del Mar City Beach, Del Mar Plaza, Torrey Pines State Reserve nearby",
     "market":"iconic racetrack with ultra-premium coastal village and median homes over $3.5M",
     "seller_situations":"estate sales, trust sales, inherited coastal properties, divorce settlements, out-of-state inheritors"},
    {"slug":"la-jolla","name":"La Jolla","county":"San Diego","zip":"92037","region":"San Diego County",
     "neighborhoods":["La Jolla Village","Bird Rock","La Jolla Shores","La Jolla Farms","Country Club","Windansea Beach area"],
     "landmarks":"UC San Diego, Birch Aquarium, La Jolla Cove, Torrey Pines Golf Course, Salk Institute",
     "market":"ultra-premium coastal village with UC San Diego and among California's most expensive real estate, median home prices above $2.5M",
     "seller_situations":"estate sales, trust and probate sales, divorce, out-of-state inheritors, downsizing wealthy homeowners"},
    {"slug":"san-diego","name":"San Diego","county":"San Diego","zip":"92101","region":"San Diego County",
     "neighborhoods":["North Park","Hillcrest","Pacific Beach","Ocean Beach","Mission Valley","Downtown","Point Loma","Mission Hills","South Park","Normal Heights"],
     "landmarks":"Balboa Park, USS Midway, Gaslamp Quarter, San Diego Zoo, Petco Park",
     "market":"California's second-largest city with strong military presence and diverse neighborhoods, median home prices around $900k",
     "seller_situations":"military relocation, divorce, inherited properties, landlords with tenant issues, probate"},
    {"slug":"poway","name":"Poway","county":"San Diego","zip":"92064","region":"San Diego County",
     "neighborhoods":["Old Poway","Poway Road corridor","Twin Peaks","Heritage Estates","Green Valley","Bridlewood"],
     "landmarks":"Lake Poway, Old Poway Park, Poway Center for the Performing Arts",
     "market":"City in the Country with large lots and excellent schools in affluent north county community, median home prices around $950k",
     "seller_situations":"downsizing empty nesters, inherited large lot properties, relocation, divorce, estate sales"},
    {"slug":"santee","name":"Santee","county":"San Diego","zip":"92071","region":"San Diego County",
     "neighborhoods":["Town Center","West Santee","East Santee","Fanita Ranch","Carlton Hills","Riverview"],
     "landmarks":"Santee Lakes, West Hills High School, Town Center Community Park, Trolley Station",
     "market":"east county suburb with affordable housing and outdoor recreation, median home prices around $650k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, homes needing updates"},
    {"slug":"escondido","name":"Escondido","county":"San Diego","zip":"92025","region":"San Diego County",
     "neighborhoods":["Elfin Forest","Hidden Meadows","East Valley Pkwy","Central Escondido","South Escondido","Felicita"],
     "landmarks":"San Diego Zoo Safari Park, California Center for the Arts, Lake Wohlford, Grape Day Park",
     "market":"inland north county SD with diverse community and mix of older homes and newer developments, median home prices around $700k",
     "seller_situations":"relocation, inherited properties, divorce, landlords, homes needing significant repairs"},
    {"slug":"la-mesa","name":"La Mesa","county":"San Diego","zip":"91941","region":"San Diego County",
     "neighborhoods":["La Mesa Village","Highlands","Casa de Oro","Rolando","Mount Helix","La Mesa Springs"],
     "landmarks":"La Mesa Village historic district, Helix Park, La Mesa Oktoberfest, Murray Reservoir",
     "market":"Jewel of the Hills with charming village downtown and close-in east county location, median home prices around $700k",
     "seller_situations":"aging homeowners, inherited properties, divorce, relocation, homes needing updates"},
    {"slug":"lemon-grove","name":"Lemon Grove","county":"San Diego","zip":"91945","region":"San Diego County",
     "neighborhoods":["North Lemon Grove","South Lemon Grove","Central Lemon Grove","Mt. Helix adjacent"],
     "landmarks":"Lemon Grove Giant Lemon statue, Lemon Grove Historical Museum, Spring Valley adjacent",
     "market":"small east county city with affordable entry-level homes and diverse community, median home prices around $600k",
     "seller_situations":"inherited older homes, landlords, relocation, divorce, first-time seller situations"},
    {"slug":"el-cajon","name":"El Cajon","county":"San Diego","zip":"92020","region":"San Diego County",
     "neighborhoods":["North El Cajon","South El Cajon","East El Cajon","Fletcher Hills","Bostonia","Rancho San Diego adjacent"],
     "landmarks":"East County Performing Arts Center, Prescott Promenade, Gillespie Field Airport",
     "market":"east SD county with large Middle Eastern community and affordable older homes, median home prices around $600k",
     "seller_situations":"inherited older homes, landlords, divorce, relocation, properties with deferred maintenance"},
    {"slug":"national-city","name":"National City","county":"San Diego","zip":"91950","region":"San Diego County",
     "neighborhoods":["National City Mile of Cars","Kimball","Las Palmas","Harbor District","Westside National City"],
     "landmarks":"Mile of Cars auto dealerships, Sweetwater Regional Park, National City Community Center",
     "market":"south bay city bordering San Diego with diverse community and affordable housing, median home prices around $550k",
     "seller_situations":"inherited properties, landlords, divorce, relocation, homes needing repairs"},
    {"slug":"chula-vista","name":"Chula Vista","county":"San Diego","zip":"91910","region":"San Diego County",
     "neighborhoods":["Otay Ranch","Eastlake","Rancho del Rey","Bonita","Northwest Chula Vista","Downtown Chula Vista"],
     "landmarks":"Chula Vista Elite Athlete Training Center, Otay Ranch Town Center, Aquatica San Diego",
     "market":"second-largest SD city with diverse community and mix of older south bay and newer eastern developments, median home prices around $700k",
     "seller_situations":"military relocation, inherited properties, divorce, landlords, upgrading families"},
    {"slug":"coronado","name":"Coronado","county":"San Diego","zip":"92118","region":"San Diego County",
     "neighborhoods":["Coronado Village","Coronado Cays","North Island area","Central Coronado","Coronado Shores"],
     "landmarks":"Hotel del Coronado, Naval Air Station North Island, Coronado Bridge, Coronado Beach",
     "market":"island city with Hotel del Coronado and premium military and civilian community, median home prices above $1.8M",
     "seller_situations":"military relocation, estate sales, trust sales, divorce, inherited island properties"},
    {"slug":"imperial-beach","name":"Imperial Beach","county":"San Diego","zip":"91932","region":"San Diego County",
     "neighborhoods":["IB Pier area","Silver Strand adjacent","Imperial Beach Shores","Bayside","Coronado Cays adjacent"],
     "landmarks":"Imperial Beach Pier, Tijuana Estuary, US Open of Surfing, Bikeway Beach",
     "market":"southernmost beach city in US with border community character and affordable coastal values, median home prices around $650k",
     "seller_situations":"relocation, inherited coastal properties, divorce, landlords, affordable coastal sales"},
]

# ── Full grouped city list for the bottom strip ────────────────────────────
CITIES_BY_REGION = {
    "Ventura County": ["Ventura","Oxnard","Port Hueneme","Camarillo","Thousand Oaks","Simi Valley","Ojai"],
    "Los Angeles County": ["Malibu","Santa Monica","Los Angeles","Beverly Hills","West Hollywood","Culver City","Inglewood","Hawthorne","Gardena","Compton","Carson","El Segundo","Manhattan Beach","Hermosa Beach","Redondo Beach","Torrance","Long Beach","Bellflower","Paramount","Downey","Norwalk","Cerritos","Lakewood","Whittier","El Monte","West Covina","Alhambra","Monterey Park","Arcadia","Pasadena","Glendale","Burbank","Santa Clarita","Pomona"],
    "Orange County": ["Seal Beach","Huntington Beach","Fountain Valley","Westminster","Garden Grove","Cypress","Buena Park","La Habra","Brea","Yorba Linda","Placentia","Stanton","Newport Beach","Costa Mesa","Laguna Beach","Laguna Hills","Laguna Niguel","Laguna Woods","Aliso Viejo","Lake Forest","Mission Viejo","Rancho Santa Margarita","Trabuco Canyon","Foothill Ranch","Dana Point","San Juan Capistrano","San Clemente","Irvine","Tustin","Orange","Santa Ana","Anaheim","Fullerton"],
    "Inland Empire": ["Riverside","Corona","Murrieta","Temecula","Menifee","Lake Elsinore","Ontario","Rancho Cucamonga"],
    "San Diego County": ["Oceanside","Vista","San Marcos","Carlsbad","Encinitas","Solana Beach","Del Mar","La Jolla","San Diego","Poway","Santee","Escondido","La Mesa","Lemon Grove","El Cajon","National City","Chula Vista","Coronado","Imperial Beach"],
}

REGION_COLORS = {
    "Ventura County":"#5b8fa8",
    "Los Angeles County":"#c0622a",
    "Orange County":"#e8823a",
    "Inland Empire":"#7a6a52",
    "San Diego County":"#2a7a6a",
}


def generate_city_content(city: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    neighborhoods_str = ", ".join(city["neighborhoods"])

    prompt = f"""You are an expert real estate SEO content writer for Golden Coast Cash Offer, a cash home buying company serving Southern California.

COMPANY: Golden Coast Cash Offer | Phone: 949-280-5139 | Website: goldencoastcashoffer.com

Write enhanced neighborhood-level landing page content for {city['name']}, {city['county']} County, CA.

NEIGHBORHOODS TO MENTION: {neighborhoods_str}
LOCAL LANDMARKS: {city['landmarks']}
MARKET CONTEXT: {city['market']}
COMMON SELLER SITUATIONS: {city['seller_situations']}

REQUIREMENTS:
1. 800-1000 words of unique helpful content
2. Mention at least 4 specific neighborhoods by name naturally in the content
3. Include what makes each mentioned neighborhood distinctive for sellers
4. 3 H2 sections with natural subheadings
5. 2 CTA sections mentioning 949-280-5139
6. Include California-specific considerations (tenant laws, high values, escrow, trust sales)
7. Warm California-casual tone
8. Meta title under 60 chars
9. Meta description under 160 chars

Return ONLY valid JSON (no markdown no backticks):
{{
  "meta_title": "...",
  "meta_description": "...",
  "h1": "We Buy Houses in {city['name']}, CA - Fast Cash Offers",
  "intro": "2-3 sentences mentioning the city and a specific neighborhood",
  "content_html": "HTML with h2 p ul li tags mentioning neighborhoods naturally",
  "why_sellers_title": "Why {city['name']} Homeowners Choose Us",
  "why_sellers_points": ["...", "...", "...", "..."]
}}"""

    prompt_safe = prompt.encode('ascii', errors='replace').decode('ascii')
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=3000,
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
        html += f'\n  <div class="region-group" style="grid-column:1/-1;margin-top:20px">\n    <div class="region-label" style="color:{color};border-color:{color}">{region}</div>\n    <div class="region-pills">'
        for city_name in cities:
            slug = city_name.lower().replace(' ', '-')
            style = f'background:{color};color:#fff;border-color:{color}' if city_name == current_city_name else ''
            html += f'\n      <a href="/{slug}/" class="city-pill" style="{style}">{city_name}</a>'
        html += '\n    </div>\n  </div>'
    return html


def build_city_page(content: dict, city: dict) -> str:
    slug = city['slug']
    year = datetime.now().year
    why_points = ''.join([f'<li style="font-size:15px;line-height:1.8;color:#4a3a28;margin:8px 0">{p}</li>' for p in content.get('why_sellers_points', [])])
    cities_strip_html = build_cities_strip(city['name'])
    neighborhoods_pills = ' '.join([f'<span style="display:inline-block;background:rgba(232,130,58,0.1);border:1px solid rgba(232,130,58,0.3);color:#c05010;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;margin:3px">{n}</span>' for n in city['neighborhoods']])

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
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QW7L1QHYFR"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-QW7L1QHYFR');</script>
<script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","wmyw873b7e");</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"RealEstateAgent","name":"Golden Coast Cash Offer","telephone":"949-280-5139","url":"https://www.goldencoastcashoffer.com","areaServed":"{city['name']}, California"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"How fast can you buy my house in {city['name']}, CA?","acceptedAnswer":{{"@type":"Answer","text":"We can close in as few as 7 days in {city['name']}. Call 949-280-5139."}}}},
{{"@type":"Question","name":"Do I need to make repairs before selling my {city['name']} home?","acceptedAnswer":{{"@type":"Answer","text":"Never. We buy houses in {city['name']} in any condition."}}}},
{{"@type":"Question","name":"Are there fees when selling to Golden Coast Cash Offer?","acceptedAnswer":{{"@type":"Answer","text":"Zero fees, zero commissions, zero closing costs."}}}},
{{"@type":"Question","name":"What neighborhoods in {city['name']} do you buy houses in?","acceptedAnswer":{{"@type":"Answer","text":"We buy houses throughout all of {city['name']} including {', '.join(city['neighborhoods'][:4])} and more."}}}}
]}}
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
.neighborhoods-strip{{background:#fff;border:1px solid #ddd5c0;border-radius:8px;padding:20px 24px;margin:28px 0}}
.neighborhoods-strip h3{{font-family:'Cormorant Garamond',serif;font-size:16px;color:var(--ocean);margin-bottom:12px;font-weight:700}}
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
.cities-strip>h2{{font-family:'Cormorant Garamond',serif;font-size:26px;color:#fff;margin-bottom:8px;text-align:center}}
.cities-strip>p{{text-align:center;color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:8px}}
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
    <a href="/">Home</a><a href="/blog/">Blog</a>
    <a href="tel:9492805139">949-280-5139</a>
    <a href="/#offer" class="nav-cta">Get Cash Offer</a>
  </div>
</nav>
<section class="hero">
  <div class="hero-inner">
    <div>
      <div class="hero-badge">🌊 {city['region']} · {city['county']} County, CA</div>
      <h1>{content['h1'].replace('Fast Cash Offers','<em>Fast Cash Offers</em>')}</h1>
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
        <div class="field"><label>Your Name *</label><input type="text" name="name" placeholder="John Smith" required></div>
        <div class="field"><label>Property Address *</label><input type="text" name="address" placeholder="{city['name']}, CA {city['zip']}" required></div>
        <div class="field-row">
          <div class="field"><label>Phone *</label><input type="tel" name="phone" placeholder="(949) 555-0000" required></div>
          <div class="field"><label>Email</label><input type="email" name="email" placeholder="john@email.com"></div>
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
      <div class="form-success" id="form-success" style="display:none;text-align:center;padding:24px">
        <div style="font-size:40px;margin-bottom:10px">🌊</div>
        <h3 style="font-family:'Cormorant Garamond',serif;font-size:20px;color:var(--ocean);margin-bottom:8px">Got It!</h3>
        <p style="font-size:13px;color:#7a6a52">We will call you within 30 minutes.<br><strong>949-280-5139</strong></p>
      </div>
      <div class="guarantee">100% confidential · No obligation · No spam</div>
    </div>
  </div>
</section>
<div class="content-wrap">
  <div class="main">
    <p style="font-size:16px;line-height:1.9;color:#3a2a18;font-weight:400;margin-bottom:24px">{content['intro']}</p>
    <div class="neighborhoods-strip">
      <h3>Neighborhoods We Serve in {city['name']}</h3>
      <div style="margin-top:8px">{neighborhoods_pills}</div>
    </div>
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
      <p style="font-size:12px;color:#7a6a52;line-height:1.7;margin:0">We handle tenant situations, probate, trust sales, and all California-specific complexities so you do not have to.</p>
    </div>
  </div>
</div>
<div class="cities-strip">
  <h2>We Buy Houses Across Southern California</h2>
  <p>90+ cities · OC · LA · San Diego · Ventura · Inland Empire</p>
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
async function submitForm(e){{
  e.preventDefault();
  const form=document.getElementById('city-form');
  const btn=form.querySelector('.submit-btn');
  btn.textContent='Submitting...';btn.disabled=true;
  try{{const fd=new FormData(form);await fetch('/',{{method:'POST',headers:{{'Content-Type':'application/x-www-form-urlencoded'}},body:new URLSearchParams(fd).toString()}});}}catch(e){{}}
  form.style.display='none';document.getElementById('form-success').style.display='block';
}}
</script>
</body>
</html>"""


def main():
    print(f"Generating {len(CITIES)} enhanced SoCal city pages — {datetime.now().isoformat()}")
    print()
    for i, city in enumerate(CITIES):
        slug = city['slug']
        output_dir = Path(slug)
        output_file = output_dir / "index.html"
        print(f"  [{i+1}/{len(CITIES)}] {city['name']} ({city['region']})...")
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
    print("Commit all folders to GitHub — Netlify will auto-deploy.")


if __name__ == "__main__":
    main()
