# -*- coding: utf-8 -*-
"""
Portable Cloud & Local Blog Engine for PB Ideas Virtuales (pbideasvirtuales.github.io).

Runs identically on Ubuntu Linux (GitHub Actions) and Windows without absolute paths.
Features:
- Dynamic sidebar carousel with uncropped app screenshots (zero 'PB IDEAS' clutter).
- Strict Google/Android trademark & brand policy guardrail before writing any HTML.
- Differentiated privacy policy routing (utilities vs. media).
- Interactive per-niche JS calculators and widgets + Schema.org JSON-LD.
"""

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent.parent
EDITORIAL_DIR = Path(__file__).resolve().parent
SITE_URL = "https://pbideasvirtuales.github.io"

ARG_TZ = timezone(timedelta(hours=-3))


def today_arg_str() -> str:
    """Return current YYYY-MM-DD date in Argentina local time (UTC-3)."""
    return datetime.now(ARG_TZ).strftime("%Y-%m-%d")


def slugify(text: str) -> str:
    """Convert article title to clean URL-safe ASCII slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


TERMINOS_PROHIBIDOS_POLITICA = [
    "official android",
    "android official",
    "google official",
    "official google",
    "google certified",
    "android certified",
    "endorsed by google",
    "endorsed by android",
    "oficial android",
    "android oficial",
    "google oficial",
    "oficial google",
    "certified by google",
    "certified by android",
    "certificado por google",
    "google play certified",
    "official app by google",
]


def auditar_politicas_estrictas(html_content: str, fuente: str) -> None:
    """Abort generation immediately if any banned trademark or endorsement phrase is found."""
    lower_c = html_content.lower()
    for term in TERMINOS_PROHIBIDOS_POLITICA:
        if term in lower_c:
            raise SystemExit(
                f"\n[POLICY SECURITY BLOCK]: Forbidden term '{term}' detected in '{fuente}'. "
                f"Violates Google Brand Permissions. Build aborted.\n"
            )


BLOG_CONFIGS = {
    "electric_blog": {
        "slug": "electric_blog",
        "lang": "en",
        "title": "Electrical Engineering & Solar Wiring Lab",
        "subtitle": "NEC (AWG) & Metric (IEC mm²) Cable Sizing, Voltage Drop, Breaker Protection (Ib ≤ In ≤ Iz) & 40% Conduit Fill",
        "accent": "#00E676",
        "accent_secondary": "#00F2FE",
        "header_bg": "linear-gradient(135deg, #0F172A 0%, #020617 100%)",
        "badge_bg": "rgba(0, 230, 118, 0.15)",
        "card_bg": "#161b22",
        "app_id": "com.pbideasvirtuales.voltagedropwiresizecalc",
        "app_name": "Wire Size & Voltage Drop Calc",
        "brand_badge": "PRO ENGINEERING SUITE • FOR ANDROID",
        "app_badge": "⚡ Dual Standard NEC AWG + IEC mm² • Auto Breaker (Ib ≤ In ≤ Iz)",
        "privacy_policy": "../privacidad-utilidades.html",
        "launch_fomo": "🔥 LAUNCH EDITION (v1.0) — EARLY ADOPTER ACCESS: Download free on Android right now and lock in full access to all core calculators & 40 offline guides before our upcoming Pro subscription update!",
        "app_desc": "Stop testing wire gauges one by one! Automatically calculates commercial AWG & metric mm² sizes, breaker trip ratings (Ib ≤ In ≤ Iz), 8 conductor metals (Copper, Aluminum, Pure Nickel, Nichrome), AC Mains, 12V/24V/48V Solar, 40% Conduit Fill, and 40 Offline Guides.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.voltagedropwiresizecalc&hl=en_US&gl=US&referrer=utm_source%3Dgithub_electric_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Download Free on Google Play (v1.0)",
        "widget_type": "wire_calc",
        "carousel_slides": [
            {
                "tag": "⚡ DUAL CODE ENGINE",
                "title": "Whole mm² & NEC AWG Sizes",
                "desc": "Simultaneous thermal & voltage drop calculation without manual guessing.",
                "img": "assets/wire_en_1.jpg",
            },
            {
                "tag": "🛡️ OVERCURRENT PROTECTION",
                "title": "Breakers & Fuses (Ib ≤ In ≤ Iz)",
                "desc": "Prevents wire melting inside conduits before the circuit breaker trips.",
                "img": "assets/wire_en_2.jpg",
            },
            {
                "tag": "🔋 SOLAR & 8 METALS",
                "title": "12V / 24V / 48V Off-Grid Sizing",
                "desc": "Class-T fuses, pure nickel battery strips & 40% conduit fill tables.",
                "img": "assets/wire_en_3.jpg",
            },
        ],
    },
    "carpentry_blog": {
        "slug": "carpentry_blog",
        "lang": "en",
        "title": "Carpentry, Roof Framing & Construction Engineering Lab",
        "subtitle": "Roof Pitch Rafters, Stair Stringers, 1/16\" Tape Fractions, Concrete Volume (1.35 Voids) & IRC Code Check",
        "accent": "#F59E0B",
        "accent_secondary": "#38BDF8",
        "header_bg": "linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%)",
        "badge_bg": "rgba(245, 158, 11, 0.18)",
        "card_bg": "#131a26",
        "app_id": "com.pbideasvirtuales.constructioncarpentrycalc",
        "app_name": "Framing & Roof Calc: Tape 1/16",
        "brand_badge": "PRO CARPENTRY SUITE • FOR ANDROID",
        "app_badge": "🪚 Visual 1/16\" Tape Zoom • Voice Readout • IRC Stair Code Check",
        "privacy_policy": "../privacidad-utilidades.html",
        "launch_fomo": "🔥 LAUNCH EDITION (v1.0) — EARLY ADOPTER ACCESS: Download free on Android right now to lock in all core framing, rafter, stair & concrete calculators unlocked before the upcoming Pro subscription update!",
        "app_desc": "Job-site engineering instrument with dual units (US Imperial fractions ↔ Metric). Features visual 1/16\" tape zoom with red needle, 1-tap fractions, voice readout on ladders, roof pitch & rafters (Common, Hip/Valley, Jack), IRC stair stringers, raked wall studs, and concrete cubic yards.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.constructioncarpentrycalc&hl=en_US&gl=US&referrer=utm_source%3Dgithub_carpentry_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Download Free on Google Play (v1.0)",
        "widget_type": "rafter_stair_calc",
        "carousel_slides": [
            {
                "tag": "📏 ZERO DECIMAL MATH",
                "title": "Visual 1/16\" Tape Measure Zoom",
                "desc": "Laser needle points to exact 1/16\" cut marks. 1-tap fraction keypad.",
                "img": "assets/carpentry_en_1.jpg",
            },
            {
                "tag": "📐 CODE COMPLIANCE",
                "title": "Stair Stringer & IRC R311.7.5 Check",
                "desc": "Equal risers, run, 2x12 board length & 1st-step tread drop deduction.",
                "img": "assets/carpentry_en_2.jpg",
            },
            {
                "tag": "🗣️ HANDS-FREE ON LADDER",
                "title": "Roof Rafters & Voice Readout",
                "desc": "Common, Hip/Valley & Jack rafters with cut angles spoken aloud.",
                "img": "assets/carpentry_en_3.jpg",
            },
        ],
    },
    "rv_camper_blog": {
        "slug": "rv_camper_blog",
        "lang": "en",
        "title": "RV Overlanding, Camper Leveling & Off-Grid HVAC Lab",
        "subtitle": "Axle Leveling Math, 3-Degree Absorption Fridge Protection, Diesel Heater Sizing & LiFePO4 Solar Batteries",
        "accent": "#10B981",
        "accent_secondary": "#F59E0B",
        "header_bg": "linear-gradient(135deg, #064E3B 0%, #022C22 50%, #0d1117 100%)",
        "badge_bg": "rgba(16, 185, 129, 0.18)",
        "card_bg": "#111f18",
        "app_id": "com.pbideasvirtuales.rvcamperleveler",
        "app_name": "RV & Home Leveler: Solar, HVAC",
        "brand_badge": "OVERLANDING TOOLKIT • FOR ANDROID",
        "app_badge": "🚐 Dual Wheel Leveling • Fridge 3° Warning • Voice Guided",
        "privacy_policy": "../privacidad-utilidades.html",
        "launch_fomo": "🔥 LAUNCH EDITION (v1.0) — EARLY ADOPTER ACCESS: Download free on Android right now to secure all RV leveling, HVAC & solar battery calculators before the Pro subscription release!",
        "app_desc": "Park perfectly level without leaving your driver's seat. Voice-guided leveling calculates exact block heights under each tire based on your wheelbase. Includes 3° absorption fridge safety warning, off-grid LiFePO4/AGM solar calculator, and diesel heater altitude tuning.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.rvcamperleveler&hl=en_US&gl=US&referrer=utm_source%3Dgithub_rv_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Download Free on Google Play (v1.0)",
        "widget_type": "rv_level_calc",
        "carousel_slides": [
            {
                "tag": "🚐 DUAL-AXIS LEVELER",
                "title": "Voice-Guided Tire Leveling",
                "desc": "Calculates exact block inches/cm under each wheel from your driver's seat.",
                "img": "assets/leveler_en_1.jpg",
            },
            {
                "tag": "🚨 APPLIANCE PROTECTION",
                "title": "3-Degree Fridge Safety Alert",
                "desc": "Prevents catastrophic ammonia boiler crystallization & $2500 replacement.",
                "img": "assets/leveler_en_2.jpg",
            },
            {
                "tag": "☀️ OFF-GRID SURVIVAL",
                "title": "LiFePO4 Solar & Diesel Sizing",
                "desc": "Avoid soot buildup at high altitude and balance lithium battery banks.",
                "img": "assets/leveler_en_3.jpg",
            },
        ],
    },
    "country_radio_blog": {
        "slug": "country_radio_blog",
        "lang": "en",
        "title": "Country Radio & Outlaw Legends Chronicle",
        "subtitle": "Classic Country, 90s Hits, Nashville Stories, Honky Tonk History & Pure Acoustic Heritage",
        "accent": "#D97706",
        "accent_secondary": "#DC2626",
        "header_bg": "linear-gradient(135deg, #451A03 0%, #1c0a00 50%, #0d1117 100%)",
        "badge_bg": "rgba(217, 119, 6, 0.2)",
        "card_bg": "#21160d",
        "app_id": "com.pbideasvirtuales.countryradio",
        "app_name": "Country Radio: Live Music",
        "brand_badge": "COUNTRY MUSIC SUITE • FOR ANDROID",
        "app_badge": "🤠 24/7 Live Country • Legends & Stories • 0% Crashes",
        "privacy_policy": "../privacidad.html",
        "launch_fomo": "📻 FREE LAUNCH EDITION: Enjoy unlimited commercial-free live country streams, legends biography guides & country trivia completely free on Android!",
        "app_desc": "The ultimate home for authentic country music lovers. Stream classic country, 90s anthems, bluegrass, and Texas red dirt live 24/7. Discover exclusive biographies of Johnny Cash, Hank Williams, and Dolly Parton, plus an interactive country music trivia challenge.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.countryradio&hl=en_US&gl=US&referrer=utm_source%3Dgithub_country_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Download Free on Google Play",
        "widget_type": "country_jukebox",
        "carousel_slides": [
            {
                "tag": "📻 24/7 LIVE STREAM",
                "title": "Classic Country & 90s Anthems",
                "desc": "Crystal clear streaming from Nashville, Texas, and across the Heartland.",
                "img": "assets/country_en_1.jpg",
            },
            {
                "tag": "🎸 OUTLAW LEGENDS",
                "title": "Johnny Cash, Hank & Dolly",
                "desc": "Deep historical chronicles, rare studio stories, and legendary recordings.",
                "img": "assets/country_en_2.jpg",
            },
            {
                "tag": "🏆 COUNTRY TRIVIA",
                "title": "200-Question Trivia Challenge",
                "desc": "Earn ad-free listening rewards while testing your country knowledge.",
                "img": "assets/country_en_3.jpg",
            },
        ],
    },
    "christmas_radio_blog": {
        "slug": "christmas_radio_blog",
        "lang": "en",
        "title": "Christmas Radio & Holiday Legends Chronicle",
        "subtitle": "1940s-1950s Crooner Classics, Bing Crosby, Frank Sinatra, Nat King Cole & Heartwarming Christmas Miracles",
        "accent": "#EF4444",
        "accent_secondary": "#10B981",
        "header_bg": "linear-gradient(135deg, #7F1D1D 0%, #300505 50%, #0d1117 100%)",
        "badge_bg": "rgba(239, 68, 68, 0.2)",
        "card_bg": "#221111",
        "app_id": "com.pbideasvirtuales.christmasmusicradio",
        "app_name": "Christmas Radio: Holiday Music",
        "brand_badge": "HOLIDAY MUSIC SUITE • FOR ANDROID",
        "app_badge": "🎄 24/7 Christmas Classics • Holiday Legends & Trivia",
        "privacy_policy": "../privacidad.html",
        "launch_fomo": "❄️ FREE HOLIDAY EDITION: Fill your home with warmth! Listen to commercial-free vintage Christmas crooners, carols & holiday stories free on Android!",
        "app_desc": "Bring the timeless warmth of Christmas to your home. Stream 24/7 live vintage crooners, instrumental carols, and cozy acoustic melodies. Explore inspiring stories like the 1914 Christmas Truce and Saint Nicholas, plus an interactive holiday quiz.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.christmasmusicradio&hl=en_US&gl=US&referrer=utm_source%3Dgithub_christmas_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Download Free on Google Play",
        "widget_type": "christmas_countdown",
        "carousel_slides": [
            {
                "tag": "🎄 VINTAGE CROONERS",
                "title": "Bing Crosby & Frank Sinatra",
                "desc": "Timeless 1940s-1950s warmth and cozy acoustic holiday carols 24/7.",
                "img": "assets/christmas_en_1.jpg",
            },
            {
                "tag": "🕊️ HOLIDAY MIRACLES",
                "title": "The 1914 Truce & Silent Night",
                "desc": "Historical stories of faith, reconciliation, and holiday traditions.",
                "img": "assets/christmas_en_2.jpg",
            },
            {
                "tag": "🎅 AD-FREE REWARDS",
                "title": "Holiday Trivia & Peaceful Music",
                "desc": "Answer festive questions and earn continuous uninterrupted playback.",
                "img": "assets/christmas_en_3.jpg",
            },
        ],
    },
    "radios_mexico_blog": {
        "slug": "radios_mexico_blog",
        "lang": "es",
        "title": "Radios de México en Vivo y Crónicas de Leyendas",
        "subtitle": "Emisoras de los 32 Estados, Música Norteña, Rancheras, Banda, Noticias y las Grandes Leyendas del Orgullo Mexicano",
        "accent": "#10B981",
        "accent_secondary": "#F43F5E",
        "header_bg": "linear-gradient(135deg, #064E3B 0%, #111827 50%, #881337 100%)",
        "badge_bg": "rgba(16, 185, 129, 0.2)",
        "card_bg": "#121d18",
        "app_id": "com.pbideasvirtuales.radiomexicofmam",
        "app_name": "Radios de México FM AM En Vivo",
        "brand_badge": "SUITE PROFESIONAL • PARA ANDROID",
        "app_badge": "🇲🇽 Emisoras de los 32 Estados • Leyendas Mexicanas y Trivia",
        "privacy_policy": "../privacidad.html",
        "launch_fomo": "🇲🇽 EDICIÓN GRATUITA DE LANZAMIENTO: Lleva la voz de tu tierra en el bolsillo. Escucha gratis y sin interrupciones tus estaciones favoritas de México en Android!",
        "app_desc": "La aplicación definitiva para conectar con México desde cualquier parte del mundo. Sintoniza estaciones de radio en vivo de los 32 estados sin cortes: música norteña, mariachi, banda y noticias. Incluye 40 crónicas de leyendas e historia mexicana y trivia de orgullo patrio.",
        "play_url": "https://play.google.com/store/apps/details?id=com.pbideasvirtuales.radiomexicofmam&hl=es_419&gl=US&referrer=utm_source%3Dgithub_mexico_blog%26utm_medium%3Dorganic_seo%26utm_campaign%3Dlaunch_v1",
        "cta_text": "📲 Descargar Gratis en Google Play",
        "widget_type": "mexico_explorer",
        "carousel_slides": [
            {
                "tag": "🇲🇽 32 ESTADOS EN VIVO",
                "title": "Jalisco, Sinaloa, Monterrey y CDMX",
                "desc": "Emisoras de toda la República con audio optimizado y cero cortes.",
                "img": "assets/mexico_es_1.jpg",
            },
            {
                "tag": "🥊 GRANDES ÍDOLOS",
                "title": "Chávez, Hugo Sánchez y El Santo",
                "desc": "Crónicas maestras del deporte y la cultura que marcaron a generaciones.",
                "img": "assets/mexico_es_2.jpg",
            },
            {
                "tag": "📻 SIN INTERRUPCIONES",
                "title": "Trivia de Orgullo y Música",
                "desc": "Lleva la voz y la emoción de tu tierra natal siempre en tu bolsillo.",
                "img": "assets/mexico_es_3.jpg",
            },
        ],
    },
}


def get_interactive_widget_html(widget_type: str, accent: str, accent2: str, play_url: str) -> str:
    """Return interactive HTML/JS widget tailored to each portal's niche."""
    if widget_type == "wire_calc":
        return f"""
        <div style="background:#161b22; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">⚡ Live Interactive Mini-Calculator: Voltage Drop &amp; Joule Heat</h3>
                <span style="background:rgba(0,230,118,0.15); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Ohm's Law Engine</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:16px;">Test conductor resistance (R = &rho;&middot;L/A) and see heat wasted in the cable before installation:</p>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:14px; margin-bottom:16px;">
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">System Voltage:</label><br>
                    <select id="sysVolt" style="width:100%; margin-top:6px; background:#161b22; color:#fff; border:1px solid #30363d; padding:8px; border-radius:6px;" onchange="calcWireMini()">
                        <option value="12">12V DC (Caravan / Off-Grid)</option>
                        <option value="24">24V DC (Solar / Marine)</option>
                        <option value="48">48V DC (Off-Grid Lithium)</option>
                        <option value="120">120V AC (US Single-Phase)</option>
                        <option value="230" selected>230V / 240V AC (Single-Phase)</option>
                    </select>
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Load Current: <span id="ampVal" style="color:{accent};">20 A</span></label><br>
                    <input type="range" id="ampSlider" min="5" max="40" step="1" value="20" style="width:100%; margin-top:10px;" oninput="calcWireMini()">
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">One-Way Distance: <span id="distVal" style="color:{accent};">45 m (148 ft)</span></label><br>
                    <input type="range" id="distSlider" min="5" max="100" step="5" value="45" style="width:100%; margin-top:10px;" oninput="calcWireMini()">
                </div>
            </div>
            <div id="wireResult" style="padding:14px; background:#0d1117; border-left:4px solid #ff5252; border-radius:8px; margin-top:10px; font-size:0.95em;">
                Voltage Drop on 4 mm² (12 AWG): <strong>7.88V (3.43%)</strong> &mdash; <strong style="color:#ff5252;">⚠️ EXCEEDS 3% LIMIT!</strong><br>
                <span style="font-size:0.9em; color:#8b949e;">Joule Heat Loss in Cable: <strong>157.5 Watts</strong></span>
            </div>
            <script>
            function calcWireMini() {{
                let V = parseFloat(document.getElementById('sysVolt').value);
                let I = parseFloat(document.getElementById('ampSlider').value);
                let L = parseFloat(document.getElementById('distSlider').value);
                document.getElementById('ampVal').innerText = I + ' A';
                document.getElementById('distVal').innerText = L + ' m (' + Math.round(L*3.28084) + ' ft)';
                let R = (2 * L * 0.0175) / 4.0;
                let vdrop = (I * R).toFixed(2);
                let pct = ((vdrop / V) * 100).toFixed(2);
                let watts = (I * I * R).toFixed(1);
                let box = document.getElementById('wireResult');
                let col = pct > 3.0 ? '#ff5252' : '#00e676';
                box.style.borderLeftColor = col;
                let msg = pct > 3.0
                    ? '⚠️ EXCEEDS 3% LIMIT! Use the full Android app to auto-size the exact AWG / mm² gauge & breaker.'
                    : '✅ SAFE (<3% Voltage Drop). Verify thermal capacity (Ib ≤ In ≤ Iz) before installing.';
                box.innerHTML = 'Voltage Drop on 4 mm² (~12 AWG): <strong>' + vdrop + 'V (' + pct + '%)</strong> &mdash; <strong style="color:' + col + ';">' + msg + '</strong><br><span style="font-size:0.9em; color:#8b949e;">Joule Heat Loss in Cable: <strong>' + watts + ' Watts</strong></span>';
            }}
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#00F2FE; font-weight:bold;">💡 Need auto AWG/mm² sizing, 8 conductor metals &amp; breaker trip math?</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#0d1117; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Unlock Android Toolkit &rarr;</a>
            </div>
        </div>
        """

    elif widget_type == "rafter_stair_calc":
        return f"""
        <div style="background:#131a26; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">🪚 Live Field Estimator: Common Rafter Pitch &amp; IRC Stair Code</h3>
                <span style="background:rgba(245,158,11,0.2); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Trigonometric Blueprint</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:16px;">Test roof rafters and stair stringers with instant building code validation:</p>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:14px; margin-bottom:16px;">
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Roof Pitch (X/12):</label><br>
                    <select id="roofPitch" style="width:100%; margin-top:6px; background:#161b22; color:#fff; border:1px solid #30363d; padding:8px; border-radius:6px;" onchange="calcRafterMini()">
                        <option value="4">4/12 (~18.4° low slope)</option>
                        <option value="6" selected>6/12 (26.6° standard)</option>
                        <option value="8">8/12 (33.7° steep)</option>
                        <option value="10">10/12 (39.8° alpine)</option>
                        <option value="12">12/12 (45.0° cathedral)</option>
                    </select>
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Building Run (Half Span): <span id="runVal" style="color:{accent};">12 ft (144 in)</span></label><br>
                    <input type="range" id="runSlider" min="6" max="24" step="1" value="12" style="width:100%; margin-top:10px;" oninput="calcRafterMini()">
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Stair Total Rise: <span id="stairVal" style="color:{accent};">70 in</span></label><br>
                    <input type="range" id="stairSlider" min="30" max="110" step="2" value="70" style="width:100%; margin-top:10px;" oninput="calcRafterMini()">
                </div>
            </div>
            <div id="rafterResult" style="padding:14px; background:#0d1117; border-left:4px solid {accent}; border-radius:8px; margin-top:10px; font-size:0.95em;">
                Rafter Line Length: <strong>13 ft 5 in (160.99")</strong> &bull; Plumb Cut: <strong>26.6°</strong> &bull; Seat Cut: <strong>63.4°</strong><br>
                Stair IRC Code Check: <strong>9 Risers @ 7-3/4"</strong> &mdash; <strong style="color:#00e676;">✅ PASSES IRC R311.7.5 CODE (&le;7-3/4")</strong>
            </div>
            <script>
            function calcRafterMini() {{
                let pitch = parseFloat(document.getElementById('roofPitch').value);
                let runFt = parseFloat(document.getElementById('runSlider').value);
                let stairIn = parseFloat(document.getElementById('stairSlider').value);
                document.getElementById('runVal').innerText = runFt + ' ft (' + (runFt*12) + ' in)';
                document.getElementById('stairVal').innerText = stairIn + ' in';
                let mult = Math.sqrt(1 + Math.pow(pitch/12.0, 2));
                let rafterIn = runFt * 12.0 * mult;
                let ft = Math.floor(rafterIn / 12);
                let remIn = Math.round(rafterIn % 12);
                let angle = (Math.atan(pitch/12.0) * (180/Math.PI)).toFixed(1);
                let seatAngle = (90 - angle).toFixed(1);
                let risers = Math.round(stairIn / 7.5);
                if (risers < 1) risers = 1;
                let riserH = (stairIn / risers).toFixed(2);
                let codePass = riserH <= 7.75;
                let col = codePass ? '#00e676' : '#ff5252';
                let codeMsg = codePass ? '✅ PASSES IRC R311.7.5 CODE' : '⚠️ FAILS CODE (>7-3/4" max riser)';
                let box = document.getElementById('rafterResult');
                box.style.borderLeftColor = col;
                box.innerHTML = 'Common Rafter: <strong>' + ft + ' ft ' + remIn + ' in (' + rafterIn.toFixed(1) + '\")</strong> &bull; Plumb Cut: <strong>' + angle + '°</strong> &bull; Seat Cut: <strong>' + seatAngle + '°</strong><br>Stair Layout: <strong>' + risers + ' Risers @ ' + riserH + '\"</strong> &mdash; <strong style="color:' + col + ';">' + codeMsg + '</strong>';
            }}
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#38BDF8; font-weight:bold;">📐 Want 1/16" visual tape zoom, 1-tap fractions, hip/valley &amp; concrete cubic yards?</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#0d1117; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Unlock Android Toolkit &rarr;</a>
            </div>
        </div>
        """

    elif widget_type == "rv_level_calc":
        return f"""
        <div style="background:#111f18; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">🚐 Live RV Leveling &amp; Absorption Fridge Safety Simulator</h3>
                <span style="background:rgba(16,185,129,0.2); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Dual-Axis Leveler</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:16px;">Calculate exact leveling block heights under tires &amp; protect your absorption fridge ammonia boiler:</p>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:14px; margin-bottom:16px;">
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">RV Wheelbase: <span id="wbVal" style="color:{accent};">160 in (4.06 m)</span></label><br>
                    <input type="range" id="wbSlider" min="100" max="250" step="5" value="160" style="width:100%; margin-top:10px;" oninput="calcRvMini()">
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Side-to-Side Roll Angle: <span id="rollVal" style="color:{accent};">2.2°</span></label><br>
                    <input type="range" id="rollSlider" min="0" max="5" step="0.1" value="2.2" style="width:100%; margin-top:10px;" oninput="calcRvMini()">
                </div>
                <div style="background:#0d1117; padding:12px; border-radius:10px; border:1px solid #30363d;">
                    <label style="font-weight:bold; font-size:0.88em; color:#8b949e;">Front-to-Back Pitch: <span id="pitchVal" style="color:{accent};">1.5°</span></label><br>
                    <input type="range" id="pitchSlider" min="0" max="5" step="0.1" value="1.5" style="width:100%; margin-top:10px;" oninput="calcRvMini()">
                </div>
            </div>
            <div id="rvResult" style="padding:14px; background:#0d1117; border-left:4px solid #00e676; border-radius:8px; margin-top:10px; font-size:0.95em;">
                Blocks Required: <strong>Right Tires +2.7" (6.8 cm)</strong> &bull; <strong>Front Tires +4.2" (10.6 cm)</strong><br>
                Fridge Status: <strong style="color:#00e676;">✅ SAFE (&lt;3.0° Tilt) &mdash; Ammonia refrigerant circulates freely by gravity.</strong>
            </div>
            <script>
            function calcRvMini() {{
                let wb = parseFloat(document.getElementById('wbSlider').value);
                let roll = parseFloat(document.getElementById('rollSlider').value);
                let pitch = parseFloat(document.getElementById('pitchSlider').value);
                document.getElementById('wbVal').innerText = wb + ' in (' + (wb*0.0254).toFixed(2) + ' m)';
                document.getElementById('rollVal').innerText = roll.toFixed(1) + '°';
                document.getElementById('pitchVal').innerText = pitch.toFixed(1) + '°';
                let rollLift = 72 * Math.sin(roll * Math.PI / 180);
                let pitchLift = wb * Math.sin(pitch * Math.PI / 180);
                let danger = roll >= 3.0 || pitch >= 3.0;
                let col = danger ? '#ff5252' : '#00e676';
                let statusMsg = danger
                    ? '🚨 DANGER (&ge;3.0° Tilt)! Absorption fridge ammonia will overheat and crystallize ($2500+ damage)!'
                    : '✅ SAFE (&lt;3.0° Tilt) &mdash; Ammonia refrigerant circulates safely by gravity.';
                let box = document.getElementById('rvResult');
                box.style.borderLeftColor = col;
                box.innerHTML = 'Block Height: <strong>Side Roll: ' + rollLift.toFixed(1) + '\" (' + (rollLift*2.54).toFixed(1) + ' cm)</strong> &bull; <strong>Length Pitch: ' + pitchLift.toFixed(1) + '\" (' + (pitchLift*2.54).toFixed(1) + ' cm)</strong><br>Fridge Protection: <strong style="color:' + col + ';">' + statusMsg + '</strong>';
            }}
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#F59E0B; font-weight:bold;">🚐 Want voice-guided leveling from the driver's seat &amp; off-grid solar math?</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#0d1117; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Unlock Android Toolkit &rarr;</a>
            </div>
        </div>
        """

    elif widget_type == "country_jukebox":
        return f"""
        <div style="background:#21160d; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">🤠 Interactive Country Legends Jukebox &amp; Trivia</h3>
                <span style="background:rgba(217,119,6,0.2); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Nashville Heritage</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:14px;">Select an icon of country music to preview their legacy and test your knowledge:</p>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;">
                <button onclick="pickLegend(0)" style="background:#451A03; color:#fff; border:1px solid #D97706; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Johnny Cash</button>
                <button onclick="pickLegend(1)" style="background:#451A03; color:#fff; border:1px solid #D97706; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Hank Williams</button>
                <button onclick="pickLegend(2)" style="background:#451A03; color:#fff; border:1px solid #D97706; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Dolly Parton</button>
                <button onclick="pickLegend(3)" style="background:#451A03; color:#fff; border:1px solid #D97706; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Willie Nelson</button>
            </div>
            <div id="legendBox" style="background:#0d1117; padding:16px; border-left:4px solid {accent}; border-radius:8px; font-size:0.95em;">
                <h4 style="margin:0 0 6px; color:{accent};">Johnny Cash &mdash; "The Man in Black"</h4>
                <p style="color:#c9d1d9; margin:0 0 10px;">"I wear black for the poor and the beaten down, living in the hopeless, hungry side of town." Recorded legendary live concerts at Folsom Prison and San Quentin.</p>
                <span style="font-size:0.88em; color:#FFB300;">🎸 Did you know? Cash was the first artist ever to be inducted into the Country, Rock, and Songwriters Halls of Fame.</span>
            </div>
            <script>
            let legends = [
                {{ name: 'Johnny Cash — \"The Man in Black\"', text: '\"I wear black for the poor and the beaten down, living in the hopeless, hungry side of town.\" Recorded legendary live concerts at Folsom Prison and San Quentin.', fact: 'Cash was the first artist ever inducted into the Country, Rock, and Songwriters Halls of Fame.' }},
                {{ name: 'Hank Williams — The Lonesome Poet', text: '\"Hear that lonesome whippoorwill, he sounds too blue to fly.\" In just 29 years of life, he wrote the foundation stones of country music.', fact: 'He wrote iconic hits like \"Your Cheatin Heart\" and \"I\'m So Lonesome I Could Cry\" on the back of brown paper bags.' }},
                {{ name: 'Dolly Parton — The Smoky Mountain Queen', text: '\"Find out who you are and do it on purpose.\" Wrote \"Jolene\" and \"I Will Always Love You\" in the very same 24-hour recording session.', fact: 'Her Imagination Library has gifted over 200 million free books to children worldwide.' }},
                {{ name: 'Willie Nelson — Red Headed Stranger', text: '\"The early bird gets the worm, but the second mouse gets the cheese.\" Left polished Nashville to pioneer Outlaw Country with his battered acoustic guitar \"Trigger\".', fact: 'Trigger has been played in over 10,000 concerts and carries autographs from Johnny Cash and Leon Russell.' }}
            ];
            function pickLegend(idx) {{
                let l = legends[idx];
                document.getElementById('legendBox').innerHTML = '<h4 style=\"margin:0 0 6px; color:#D97706;\">' + l.name + '</h4><p style=\"color:#c9d1d9; margin:0 0 10px;\">' + l.text + '</p><span style=\"font-size:0.88em; color:#FFB300;\">🎸 Trivia: ' + l.fact + '</span>';
            }}
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#FFB300; font-weight:bold;">📻 Stream 100+ live classic &amp; 90s country radio stations 24/7 on Android!</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#0d1117; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Listen Free on Android &rarr;</a>
            </div>
        </div>
        """

    elif widget_type == "christmas_countdown":
        return f"""
        <div style="background:#221111; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">🎄 Real-Time Holiday Countdown &amp; Vintage Crooner Trivia</h3>
                <span style="background:rgba(239,68,68,0.2); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Holiday Magic</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:14px;">How many days until Christmas? Plus timeless secrets behind the golden age of holiday music:</p>
            <div style="display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-bottom:16px; text-align:center;">
                <div style="background:#0d1117; border:1px solid #30363d; padding:12px 18px; border-radius:10px; min-width:80px;">
                    <div id="cDays" style="font-size:1.8em; font-weight:900; color:{accent};">--</div>
                    <div style="font-size:0.75em; color:#8b949e; text-transform:uppercase;">Days</div>
                </div>
                <div style="background:#0d1117; border:1px solid #30363d; padding:12px 18px; border-radius:10px; min-width:80px;">
                    <div id="cHours" style="font-size:1.8em; font-weight:900; color:#10B981;">--</div>
                    <div style="font-size:0.75em; color:#8b949e; text-transform:uppercase;">Hours</div>
                </div>
                <div style="background:#0d1117; border:1px solid #30363d; padding:12px 18px; border-radius:10px; min-width:80px;">
                    <div id="cMins" style="font-size:1.8em; font-weight:900; color:#FEF08A;">--</div>
                    <div style="font-size:0.75em; color:#8b949e; text-transform:uppercase;">Mins</div>
                </div>
            </div>
            <div style="background:#0d1117; padding:14px; border-left:4px solid {accent}; border-radius:8px; font-size:0.92em; color:#c9d1d9;">
                ❄️ <strong>Golden Age Fact:</strong> Bing Crosby's <em>"White Christmas"</em> (1942) remains the best-selling physical music single in world history (+50 million copies sold), written by Irving Berlin poolside in California!
            </div>
            <script>
            function updateCountdown() {{
                let now = new Date();
                let year = now.getFullYear();
                let xmas = new Date(year, 11, 25);
                if (now > xmas) xmas = new Date(year + 1, 11, 25);
                let diff = xmas - now;
                let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                let h = Math.floor((diff / (1000 * 60 * 60)) % 24);
                let m = Math.floor((diff / 1000 / 60) % 60);
                document.getElementById('cDays').innerText = d;
                document.getElementById('cHours').innerText = h;
                document.getElementById('cMins').innerText = m;
            }}
            updateCountdown();
            setInterval(updateCountdown, 60000);
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#10B981; font-weight:bold;">🎅 Bring vintage holiday cheer 24/7 into your living room on Android!</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#fff; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Listen Free on Android &rarr;</a>
            </div>
        </div>
        """

    elif widget_type == "mexico_explorer":
        return f"""
        <div style="background:#121d18; border:2px solid {accent}; border-radius:14px; padding:22px; margin:34px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <h3 style="margin:0; color:{accent}; font-size:1.25em;">🇲🇽 Explorador Musical y Cultural por Estados de México</h3>
                <span style="background:rgba(16,185,129,0.2); color:{accent}; padding:3px 10px; border-radius:12px; font-size:0.8em; font-weight:bold;">Orgullo Mexicano</span>
            </div>
            <p style="color:#c9d1d9; font-size:0.92em; margin-bottom:14px;">Elige un estado de la República Mexicana para descubrir su tradición musical y emisoras en vivo:</p>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;">
                <button onclick="pickEstado(0)" style="background:#064E3B; color:#fff; border:1px solid #10B981; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Jalisco</button>
                <button onclick="pickEstado(1)" style="background:#064E3B; color:#fff; border:1px solid #10B981; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Sinaloa</button>
                <button onclick="pickEstado(2)" style="background:#064E3B; color:#fff; border:1px solid #10B981; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Michoacán</button>
                <button onclick="pickEstado(3)" style="background:#064E3B; color:#fff; border:1px solid #10B981; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">CDMX</button>
                <button onclick="pickEstado(4)" style="background:#064E3B; color:#fff; border:1px solid #10B981; padding:8px 14px; border-radius:20px; cursor:pointer; font-weight:bold;">Nuevo León</button>
            </div>
            <div id="estadoBox" style="background:#0d1117; padding:16px; border-left:4px solid {accent}; border-radius:8px; font-size:0.95em;">
                <h4 style="margin:0 0 6px; color:{accent};">Jalisco &mdash; Cuna del Mariachi y el Tequila</h4>
                <p style="color:#c9d1d9; margin:0 0 10px;">Hogar del son jalisciense, trompetas vibrantes y guitarras de golpe. Cuna de figuras históricas y epicentro de las fiestas patrias.</p>
                <span style="font-size:0.88em; color:#F43F5E;">📻 En la app: Sintoniza en vivo emisoras de Guadalajara, Puerto Vallarta y los Altos de Jalisco en 1 toque.</span>
            </div>
            <script>
            let estados = [
                {{ name: 'Jalisco — Cuna del Mariachi y el Tequila', text: 'Hogar del son jalisciense, trompetas vibrantes y guitarras de golpe. Cuna de figuras históricas y epicentro de las fiestas patrias.', note: 'En la app: Emisoras de Guadalajara, Puerto Vallarta y los Altos de Jalisco en vivo.' }},
                {{ name: 'Sinaloa — Corazón de la Banda y la Tambora', text: 'Tierra de la tambora sinaloense tradicional, charchetas, clarinetes y trombones con ritmos que hacen bailar a todo México.', note: 'En la app: Emisoras de Culiacán, Mazatlán, Los Mochis y Guasave sin cortes.' }},
                {{ name: 'Michoacán — Alma Purépecha y Pirekuas', text: 'Tierra de lagos, Día de Muertos en Pátzcuaro y el sonido de las pirekuas, patrimonio cultural inmaterial de la humanidad.', note: 'En la app: Emisoras de Morelia, Uruapan, Zamora y Lázaro Cárdenas en vivo.' }},
                {{ name: 'CDMX — El Pulso de la Gran Metrópoli', text: 'El epicentro informativo, cultural y musical del país. Noticias al instante, rock en español, jazz y cumbia sonidera.', note: 'En la app: Las cadenas radiales más escuchadas de la capital mexicana con audio HD.' }},
                {{ name: 'Nuevo León — Tierra Norteña y Acordeón', text: 'Cuna de la polka norteña, redova, chotis y el sonido inconfundible del acordeón y el bajo sexto de Monterrey.', note: 'En la app: Emisoras de Monterrey, Guadalupe y San Nicolás de los Garza en vivo.' }}
            ];
            function pickEstado(idx) {{
                let e = estados[idx];
                document.getElementById('estadoBox').innerHTML = '<h4 style=\"margin:0 0 6px; color:#10B981;\">' + e.name + '</h4><p style=\"color:#c9d1d9; margin:0 0 10px;\">' + e.text + '</p><span style=\"font-size:0.88em; color:#F43F5E;\">📻 ' + e.note + '</span>';
            }}
            </script>
            <div style="margin-top:14px; padding-top:12px; border-top:1px solid #30363d; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <span style="font-size:0.88em; color:#F43F5E; font-weight:bold;">🇲🇽 ¡Lleva a México en tu bolsillo con radios de los 32 estados!</span>
                <a href="{play_url}" target="_blank" rel="noopener" style="background:{accent}; color:#0d1117; font-weight:800; padding:8px 18px; border-radius:20px; text-decoration:none; font-size:0.88em;">Descargar Gratis en Android &rarr;</a>
            </div>
        </div>
        """
    return ""


def render_sidebar_html(blog_cfg: dict, current_slug: str, all_arts: list) -> str:
    """Render sticky sidebar with ad carousel and newest-first scrollable article directory."""
    accent = blog_cfg["accent"]
    accent2 = blog_cfg.get("accent_secondary", "#FFB300")

    sorted_arts = sorted(all_arts, key=lambda x: (x.get("date", ""), x["slug"]), reverse=True)
    articles_links = ""
    for a in sorted_arts:
        is_active = a["slug"] == current_slug
        bg = "rgba(255, 255, 255, 0.08)" if is_active else "#0d1117"
        border_col = accent if is_active else "#30363d"
        badge = f'<span style="background:{accent}; color:#0d1117; font-size:0.7em; font-weight:900; padding:2px 6px; border-radius:4px; margin-left:6px;">READING</span>' if is_active else ""
        thumb = f'<img src="{a["hero_img"]}" alt="{a["title"]}" style="width:54px; height:54px; object-fit:cover; border-radius:8px; flex-shrink:0;">' if a.get("hero_img") else ""

        articles_links += f"""
        <a href="{a['slug']}.html" style="display:flex; gap:12px; align-items:center; background:{bg}; border:1px solid {border_col}; border-radius:10px; padding:10px; margin-bottom:10px; text-decoration:none; transition:transform 0.15s ease;">
            {thumb}
            <div style="flex:1; min-width:0;">
                <div style="color:#ffffff; font-size:0.86em; font-weight:bold; line-height:1.3; overflow:hidden; text-overflow:ellipsis; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">
                    {a['title']} {badge}
                </div>
                <div style="color:#8b949e; font-size:0.75em; margin-top:4px;">{a['date']}</div>
            </div>
        </a>
        """

    slides = blog_cfg.get("carousel_slides", [])
    slides_html = ""
    dots_html = ""
    for i, s in enumerate(slides):
        display_style = "display:block;" if i == 0 else "display:none;"
        dot_bg = accent if i == 0 else "#4b5563"
        slides_html += f"""
        <div class="sidebar-slide" data-slide="{i}" style="{display_style} text-align:center;">
            <div style="display:inline-block; background:{blog_cfg['badge_bg']}; color:{accent}; font-size:0.75em; font-weight:900; letter-spacing:0.8px; padding:3px 10px; border-radius:12px; text-transform:uppercase; margin-bottom:8px;">
                {s['tag']}
            </div>
            <div style="background:#090d13; border:1px solid #21262d; border-radius:12px; padding:6px; margin-bottom:8px; display:flex; justify-content:center; align-items:center;">
                <img src="{s['img']}" alt="{s['title']}" style="max-height:250px; width:auto; max-width:100%; object-fit:contain; border-radius:8px; filter:drop-shadow(0 6px 14px rgba(0,0,0,0.6)); display:block; margin:0 auto;">
            </div>
            <h4 style="margin:4px 0 2px; color:#ffffff; font-size:0.95em; line-height:1.3;">{s['title']}</h4>
            <p style="color:#8b949e; font-size:0.8em; margin:0 0 8px; line-height:1.35;">{s['desc']}</p>
        </div>
        """
        dots_html += f'<span class="carousel-dot" onclick="switchSidebarSlide({i})" data-dot="{i}" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{dot_bg}; margin:0 4px; cursor:pointer; transition:background 0.3s;"></span>'

    is_es = blog_cfg.get("lang") == "es"
    free_txt = "📲 Instalar Gratis (v1.0)" if is_es else "📲 Get Free on Google Play (v1.0)"
    brand_badge_txt = blog_cfg.get("brand_badge", "ENGINEERING SUITE • FOR ANDROID")
    library_txt = f"📚 Más Guías y Crónicas ({len(sorted_arts)})" if is_es else f"📚 More Lab Field Guides ({len(sorted_arts)})"

    return f"""
    <aside class="sidebar-wrapper">
        <!-- TARJETA PUBLICITARIA CON CARRUSEL ANIMADO Y ROTATIVO -->
        <div style="background:{blog_cfg['card_bg']}; border:2px solid {accent}; border-radius:16px; padding:18px 16px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.5); position:relative;" id="adCardContainer">
            <div style="text-align:center; margin-bottom:12px; border-bottom:1px solid #30363d; padding-bottom:8px;">
                <span style="color:{accent}; font-size:0.78em; font-weight:900; letter-spacing:1px; text-transform:uppercase; display:inline-block;">
                    {brand_badge_txt}
                </span>
            </div>

            <div id="sidebarCarousel" onmouseenter="pauseCarousel()" onmouseleave="resumeCarousel()">
                {slides_html}
            </div>

            <!-- Indicadores de puntos -->
            <div style="text-align:center; margin:6px 0 12px;" id="carouselDots">
                {dots_html}
            </div>

            <a href="{blog_cfg['play_url']}" target="_blank" rel="noopener" style="display:block; text-align:center; background:{accent}; color:#0d1117; font-weight:900; font-size:0.95em; padding:12px 14px; border-radius:24px; text-decoration:none; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 4px 14px rgba(0,0,0,0.4);">
                {free_txt} &rarr;
            </a>
            <p style="font-size:0.74em; color:#8b949e; text-align:center; margin:8px 0 0;">✓ 100% Offline • ✓ Google Play Verified • ✓ No Ads in v1.0</p>
        </div>

        <script>
        let currentSlideIdx = 0;
        const totalSlides = {len(slides)};
        let slideTimer = null;

        function switchSidebarSlide(idx) {{
            currentSlideIdx = idx;
            document.querySelectorAll('.sidebar-slide').forEach((el, i) => {{
                el.style.display = (i === idx) ? 'block' : 'none';
            }});
            document.querySelectorAll('.carousel-dot').forEach((el, i) => {{
                el.style.background = (i === idx) ? '{accent}' : '#4b5563';
            }});
        }}

        function nextSidebarSlide() {{
            currentSlideIdx = (currentSlideIdx + 1) % totalSlides;
            switchSidebarSlide(currentSlideIdx);
        }}

        function startCarousel() {{
            if (!slideTimer && totalSlides > 1) {{
                slideTimer = setInterval(nextSidebarSlide, 3800);
            }}
        }}

        function pauseCarousel() {{
            if (slideTimer) {{
                clearInterval(slideTimer);
                slideTimer = null;
            }}
        }}

        function resumeCarousel() {{
            startCarousel();
        }}

        document.addEventListener('DOMContentLoaded', startCarousel);
        </script>

        <!-- NAVEGACIÓN A LOS OTROS ARTÍCULOS -->
        <div style="background:{blog_cfg['card_bg']}; border:1px solid #30363d; border-radius:14px; padding:18px;">
            <h4 style="margin:0 0 14px; font-size:0.98em; color:{accent2}; border-bottom:1px solid #30363d; padding-bottom:8px;">
                {library_txt}
            </h4>
            <div style="max-height:460px; overflow-y:auto; padding-right:4px;">
                {articles_links}
            </div>
        </div>
    </aside>
    """


def render_article_page(blog_cfg: dict, art: dict, all_arts: list) -> str:
    """Render individual SEO/GEO article HTML page."""
    accent = blog_cfg["accent"]
    accent2 = blog_cfg.get("accent_secondary", "#FFB300")
    widget_html = get_interactive_widget_html(blog_cfg["widget_type"], accent, accent2, blog_cfg["play_url"])
    sidebar_html = render_sidebar_html(blog_cfg, art["slug"], all_arts)

    hero_html = ""
    if art.get("hero_img"):
        hero_html = f"""
        <div style="margin:24px 0;">
            <img src="{art['hero_img']}" alt="{art['title']}" style="width:100%; max-height:420px; object-fit:cover; border-radius:14px; border:2px solid #30363d;">
            <p style="font-size:0.88em; color:#8b949e; margin-top:8px; text-align:center;">{art.get('hero_caption', '')}</p>
        </div>
        """

    schema_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": art["title"],
                "datePublished": art["date"],
                "description": art["summary"],
                "author": {"@type": "Organization", "name": "PB Ideas Virtuales"},
            },
            {
                "@type": "SoftwareApplication",
                "name": blog_cfg["app_name"],
                "operatingSystem": "Android",
                "applicationCategory": "UtilitiesApplication",
                "url": blog_cfg["play_url"],
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": art["faq_q"],
                        "acceptedAnswer": {"@type": "Answer", "text": art["faq_a"]},
                    }
                ],
            },
        ],
    }

    is_es = blog_cfg.get("lang") == "es"
    back_txt = "&larr; Volver al Inicio del Portal" if is_es else f"&larr; Back to {blog_cfg['title']} Home"
    faq_heading = "Pregunta Frecuente del Campo" if is_es else "Frequently Asked Technical Question"
    priv_txt = "Política de Privacidad" if is_es else "Privacy Policy"
    hub_txt = "Inicio Desarrollador" if is_es else "Main Developer Hub"
    topbar_cta = "Obtener en Google Play &rarr;" if is_es else "Get v1.0 on Google Play &rarr;"
    verified_line = "✓ Gratis en Android (Google Play) • ✓ Cero Bloqueos" if is_es else "✓ Free on Android (Google Play) • ✓ Works 100% Offline • ✓ 0% Crashes"

    return f"""<!DOCTYPE html>
<html lang="{blog_cfg['lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art['title']} | {blog_cfg['title']}</title>
    <meta name="description" content="{art['summary']}">
    <meta name="keywords" content="{art['keywords']}">
    <link rel="canonical" href="{SITE_URL}/{blog_cfg['slug']}/{art['slug']}.html">
    <script type="application/ld+json">{json.dumps(schema_ld, ensure_ascii=False)}</script>
    <style>
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background:#0d1117; color:#e6edf3; margin:0; line-height:1.75; }}
        .top-bar {{ background:#161b22; border-bottom:2px solid {accent2}; padding:10px 20px; text-align:center; font-size:0.9em; color:#fff; }}
        .top-bar a {{ color:{accent2}; font-weight:800; text-decoration:underline; }}
        header {{ background:{blog_cfg['header_bg']}; padding:28px 20px; border-bottom:3px solid {accent}; text-align:center; }}
        header a {{ color:{accent}; text-decoration:none; font-weight:bold; font-size:1.05em; }}
        
        .layout-container {{ max-width:1220px; margin:0 auto; padding:32px 20px; display:flex; gap:36px; align-items:flex-start; }}
        .main-content {{ flex:1; min-width:0; }}
        .sidebar-wrapper {{ width:340px; flex-shrink:0; position:sticky; top:20px; }}
        
        @media (max-width: 960px) {{
            .layout-container {{ flex-direction:column; }}
            .sidebar-wrapper {{ width:100%; position:static; margin-top:20px; }}
        }}

        h1 {{ color:#ffffff; font-size:2.2em; line-height:1.25; margin-bottom:10px; }}
        h2 {{ color:{accent2}; margin-top:36px; border-bottom:1px solid #21262d; padding-bottom:8px; }}
        code {{ background:#161b22; color:{accent}; padding:2px 6px; border-radius:4px; font-size:0.95em; }}
        .meta {{ color:#8b949e; font-size:0.9em; margin-bottom:22px; }}
        .cta-card {{ background:{blog_cfg['card_bg']}; border:2px solid {accent2}; border-radius:18px; padding:30px 24px; margin:38px 0; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.65); }}
        .cta-badge {{ display:inline-block; background:{blog_cfg['badge_bg']}; color:{accent2}; padding:6px 16px; border-radius:20px; font-size:0.86em; font-weight:bold; margin-bottom:12px; }}
        .fomo-box {{ background:rgba(255,255,255,0.06); border:1px dashed {accent}; color:#e6edf3; padding:12px 16px; border-radius:10px; max-width:660px; margin:12px auto 18px; font-size:0.92em; }}
        .cta-btn {{ display:inline-block; margin-top:10px; padding:16px 36px; background:{accent2}; color:#0d1117; font-weight:900; font-size:1.1em; text-decoration:none; border-radius:30px; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 4px 15px rgba(0,0,0,0.4); }}
        .faq-box {{ background:#161b22; padding:22px; border-left:4px solid {accent}; border-radius:8px; margin-top:34px; }}
        footer {{ text-align:center; padding:30px 20px; color:#8b949e; border-top:1px solid #21262d; margin-top:50px; font-size:0.9em; }}
        footer a {{ color:{accent}; text-decoration:none; }}
    </style>
</head>
<body>
    <div class="top-bar">
        {blog_cfg['launch_fomo']} <a href="{blog_cfg['play_url']}" target="_blank" rel="noopener">{topbar_cta}</a>
    </div>
    <header>
        <a href="index.html">{back_txt}</a>
    </header>
    
    <div class="layout-container">
        <main class="main-content">
            <h1>{art['title']}</h1>
            <div class="meta">Updated {art['date']} • By PB Ideas Virtuales Team</div>
            {hero_html}
            {art['body_html']}
            {widget_html}
            <div class="cta-card">
                <div class="cta-badge">{blog_cfg['app_badge']}</div>
                <h2 style="margin-top:4px; color:#fff; border:none;">{blog_cfg['app_name']}</h2>
                <p style="color:#c9d1d9; max-width:680px; margin:10px auto;">{blog_cfg['app_desc']}</p>
                <div class="fomo-box">{blog_cfg['launch_fomo']}</div>
                <a href="{blog_cfg['play_url']}" target="_blank" rel="noopener" class="cta-btn">{blog_cfg['cta_text']}</a>
                <p style="font-size:0.82em; color:#8b949e; margin-top:12px; margin-bottom:0;">{verified_line}</p>
            </div>
            <div class="faq-box">
                <h3 style="margin-top:0; color:{accent};">{faq_heading}</h3>
                <p><strong>{art['faq_q']}</strong></p>
                <p style="margin-bottom:0;">{art['faq_a']}</p>
            </div>
        </main>
        {sidebar_html}
    </div>

    <footer>
        <p>&copy; 2026 PB Ideas Virtuales • <a href="../index.html">{hub_txt}</a> • <a href="{blog_cfg['privacy_policy']}">{priv_txt}</a></p>
    </footer>
</body>
</html>"""


def render_blog_index(blog_cfg: dict, articles: list) -> str:
    """Render portal index page for an individual blog."""
    accent = blog_cfg["accent"]
    accent2 = blog_cfg.get("accent_secondary", "#FFB300")
    widget_html = get_interactive_widget_html(blog_cfg["widget_type"], accent, accent2, blog_cfg["play_url"])
    sidebar_html = render_sidebar_html(blog_cfg, "", articles)

    is_es = blog_cfg.get("lang") == "es"
    priv_txt = "Política de Privacidad" if is_es else "Privacy Policy"
    hub_txt = "Inicio Desarrollador" if is_es else "Main Developer Hub"
    latest_txt = "Últimas Crónicas y Guías Editoriales" if is_es else "Latest Field Guides &amp; Technical Manuals"
    verified_txt = "✓ Gratis en Android &bull; ✓ Audio Optimizado &bull; ✓ Sin Cortes" if is_es else "✓ Free on Android &bull; ✓ 100% Offline &bull; ✓ Verified Calculations"
    topbar_cta = "Obtener en Google Play &rarr;" if is_es else "Get v1.0 on Google Play &rarr;"
    read_cta = "Leer Crónica Completa &rarr;" if is_es else "Read Full Guide &amp; Calculator &rarr;"

    cards_html = ""
    for a in sorted(articles, key=lambda x: (x.get("date", ""), x["slug"]), reverse=True):
        thumb_html = f'<img src="{a["hero_img"]}" alt="{a["title"]}" style="width:100%; height:220px; object-fit:cover; border-radius:10px; margin-bottom:14px;">' if a.get("hero_img") else ""
        cards_html += f"""
        <div class="post-card" style="background:{blog_cfg['card_bg']}; border:1px solid #30363d; border-radius:14px; padding:24px; margin-bottom:24px; transition:border-color 0.2s;">
            {thumb_html}
            <div style="color:{accent2}; font-size:0.85em; font-weight:bold; text-transform:uppercase;">Published {a['date']} • Editorial Field Guide</div>
            <h2 style="margin:8px 0 10px; font-size:1.5em; border:none; padding:0;"><a href="{a['slug']}.html" style="color:#ffffff; text-decoration:none;">{a['title']}</a></h2>
            <p style="color:#c9d1d9; line-height:1.6;">{a['summary']}</p>
            <a href="{a['slug']}.html" style="color:{accent}; font-weight:bold; text-decoration:none; font-size:1.02em;">{read_cta}</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="{blog_cfg['lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{blog_cfg['title']} | {blog_cfg['app_name']}</title>
    <meta name="description" content="{blog_cfg['subtitle']}">
    <link rel="canonical" href="{SITE_URL}/{blog_cfg['slug']}/">
    <style>
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background:#0d1117; color:#e6edf3; margin:0; line-height:1.65; }}
        .top-bar {{ background:#161b22; border-bottom:2px solid {accent2}; padding:10px 20px; text-align:center; font-size:0.9em; color:#fff; }}
        .top-bar a {{ color:{accent2}; font-weight:800; text-decoration:underline; }}
        header {{ background:{blog_cfg['header_bg']}; padding:45px 20px; border-bottom:3px solid {accent}; text-align:center; }}
        header h1 {{ margin:0; color:{accent}; font-size:2.4em; }}
        header p {{ color:#c9d1d9; font-size:1.15em; max-width:740px; margin:12px auto 0; }}
        
        .layout-container {{ max-width:1220px; margin:0 auto; padding:36px 20px; display:flex; gap:36px; align-items:flex-start; }}
        .main-content {{ flex:1; min-width:0; }}
        .sidebar-wrapper {{ width:340px; flex-shrink:0; position:sticky; top:20px; }}
        
        @media (max-width: 960px) {{
            .layout-container {{ flex-direction:column; }}
            .sidebar-wrapper {{ width:100%; position:static; margin-top:20px; }}
        }}

        .hero-app {{ background:{blog_cfg['card_bg']}; border:2px solid {accent2}; border-radius:18px; padding:30px 24px; margin-bottom:40px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.6); }}
        .fomo-box {{ background:rgba(255,255,255,0.06); border:1px dashed {accent}; color:#e6edf3; padding:12px 16px; border-radius:10px; max-width:660px; margin:12px auto 18px; font-size:0.92em; }}
        .cta-btn {{ display:inline-block; margin-top:10px; padding:16px 34px; background:{accent2}; color:#0d1117; font-weight:900; font-size:1.08em; text-decoration:none; border-radius:30px; text-transform:uppercase; box-shadow:0 4px 15px rgba(0,0,0,0.4); }}
        footer {{ text-align:center; padding:30px 20px; color:#8b949e; border-top:1px solid #21262d; margin-top:50px; font-size:0.9em; }}
        footer a {{ color:{accent}; text-decoration:none; }}
    </style>
</head>
<body>
    <div class="top-bar">
        {blog_cfg['launch_fomo']} <a href="{blog_cfg['play_url']}" target="_blank" rel="noopener">{topbar_cta}</a>
    </div>
    <header>
        <h1>{blog_cfg['title']}</h1>
        <p>{blog_cfg['subtitle']}</p>
    </header>

    <div class="layout-container">
        <main class="main-content">
            <div class="hero-app">
                <span style="background:{blog_cfg['badge_bg']}; color:{accent2}; padding:6px 14px; border-radius:16px; font-size:0.85em; font-weight:bold;">
                    {blog_cfg['app_badge']}
                </span>
                <h2 style="color:#ffffff; margin:14px 0 8px; font-size:1.8em;">{blog_cfg['app_name']}</h2>
                <p style="color:#c9d1d9; max-width:680px; margin:0 auto 14px; font-size:0.98em;">{blog_cfg['app_desc']}</p>
                <div class="fomo-box">{blog_cfg['launch_fomo']}</div>
                <a href="{blog_cfg['play_url']}" target="_blank" rel="noopener" class="cta-btn">{blog_cfg['cta_text']}</a>
                <p style="font-size:0.8em; color:#8b949e; margin-top:10px; margin-bottom:0;">{verified_txt}</p>
            </div>

            {widget_html}

            <h2 style="color:#ffffff; font-size:1.6em; border-bottom:2px solid {accent}; padding-bottom:8px; margin-bottom:24px;">{latest_txt}</h2>
            {cards_html}
        </main>
        {sidebar_html}
    </div>

    <footer>
        <p>&copy; 2026 PB Ideas Virtuales • <a href="../index.html">{hub_txt}</a> • <a href="{blog_cfg['privacy_policy']}">{priv_txt}</a></p>
    </footer>
</body>
</html>"""


def build_master_sitemap(all_urls: list) -> None:
    """Write root sitemap.xml covering main hub, all 6 portals, and all articles."""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    today = today_arg_str()
    for u in all_urls:
        xml_lines.append(
            f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>"""
        )
    xml_lines.append("</urlset>")
    sitemap_path = REPO_DIR / "sitemap.xml"
    sitemap_path.write_text("\n".join(xml_lines), encoding="utf-8")
    print(f"Master sitemap.xml updated with {len(all_urls)} URLs.")


def build_master_index() -> None:
    """Write root index.html developer hub linking to all 6 portals and separated policies."""
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PB Ideas Virtuales | Independent Android Apps, Technical Labs &amp; Radio Blogs</title>
    <meta name="description" content="Official hub of PB Ideas Virtuales — independent Android utility apps (Electrical, Carpentry, RV Camper), technical engineering blogs, and thematic live streaming radio apps &amp; chronicles.">
    <meta name="p:domain_verify" content="32f5e448e9ac4fe74014e22e49efd97a"/>
    <link rel="canonical" href="{SITE_URL}/">
    <style>
        * {{ box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background:#0d1117; color:#e6edf3; margin:0; line-height:1.65; }}
        header {{ background:linear-gradient(135deg, #161b22 0%, #05070a 100%); padding:52px 20px 38px; text-align:center; border-bottom:3px solid #00E676; }}
        .studio-pill {{ display:inline-block; background:rgba(0, 230, 118, 0.12); color:#00E676; border:1px solid rgba(0, 230, 118, 0.35); padding:6px 16px; border-radius:20px; font-size:0.82em; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; margin-bottom:14px; }}
        header h1 {{ margin:0; color:#ffffff; font-size:2.6em; letter-spacing:-0.5px; }}
        header h1 span {{ color:#00E676; }}
        header p {{ color:#c9d1d9; font-size:1.12em; max-width:780px; margin:14px auto 0; }}
        .quick-nav {{ display:flex; flex-wrap:wrap; justify-content:center; gap:10px; margin-top:24px; }}
        .quick-nav a {{ background:#161b22; color:#e6edf3; border:1px solid #30363d; padding:8px 16px; border-radius:20px; text-decoration:none; font-size:0.88em; font-weight:600; transition:border-color 0.2s, color 0.2s; }}
        .quick-nav a:hover {{ border-color:#00E676; color:#00E676; }}
        .container {{ max-width:1180px; margin:0 auto; padding:38px 20px; }}
        .section-head {{ margin:14px 0 24px; border-bottom:2px solid #21262d; padding-bottom:12px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-end; gap:10px; }}
        .section-head h2 {{ margin:0; color:#ffffff; font-size:1.7em; }}
        .section-head span {{ color:#8b949e; font-size:0.92em; }}
        .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap:22px; margin-bottom:52px; }}
        .card {{ background:#161b22; border:1px solid #30363d; border-radius:16px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; min-width:0; transition:transform 0.2s, border-color 0.2s; }}
        .card:hover {{ transform:translateY(-4px); border-color:#00E676; }}
        .app-tag {{ display:inline-block; background:#0d1117; border:1px solid #30363d; color:#c9d1d9; padding:4px 11px; border-radius:12px; font-size:0.76em; font-weight:700; margin-bottom:12px; align-self:flex-start; }}
        .card h3 {{ margin:0 0 6px; font-size:1.3em; color:#ffffff; }}
        .card .sub-blog {{ font-size:0.9em; font-weight:700; margin-bottom:10px; }}
        .card .sub-blog a {{ text-decoration:none; }}
        .card .sub-blog a:hover {{ text-decoration:underline; }}
        .card p {{ color:#c9d1d9; font-size:0.93em; line-height:1.58; margin:0 0 18px; }}
        .btn-row {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:auto; }}
        .btn {{ display:inline-block; flex:1 1 auto; padding:9px 12px; border-radius:20px; font-weight:700; text-decoration:none; font-size:0.82em; text-align:center; white-space:nowrap; transition:opacity 0.2s; }}
        .btn:hover {{ opacity:0.9; }}
        .btn-outline {{ background:transparent; border:1px solid #30363d; color:#e6edf3; }}
        .btn-outline:hover {{ border-color:#00E676; color:#00E676; }}
        .blogs-split {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap:22px; margin-bottom:52px; }}
        .blog-dir-box {{ background:#131820; border:1px solid #30363d; border-radius:16px; padding:24px; }}
        .blog-dir-box h3 {{ margin:0 0 6px; font-size:1.25em; color:#ffffff; }}
        .blog-dir-box .dir-sub {{ color:#8b949e; font-size:0.88em; margin:0 0 16px; }}
        .blog-list {{ list-style:none; padding:0; margin:0; }}
        .blog-list li {{ border-top:1px solid #21262d; padding:12px 0; }}
        .blog-list li:last-child {{ padding-bottom:0; }}
        .blog-list a {{ font-weight:700; text-decoration:none; font-size:0.98em; }}
        .blog-list a:hover {{ text-decoration:underline; }}
        .blog-list small {{ display:block; color:#8b949e; margin-top:3px; font-size:0.86em; }}
        .dev-box {{ background:linear-gradient(135deg, #161b22 0%, #0f141c 100%); border:1px solid #30363d; border-left:4px solid #00E676; border-radius:16px; padding:28px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:20px; }}
        .dev-box-text {{ flex:1; min-width:260px; }}
        .dev-box-text h2 {{ margin:0 0 8px; color:#ffffff; font-size:1.45em; }}
        .dev-box-text p {{ margin:0; color:#c9d1d9; font-size:0.95em; }}
        footer {{ text-align:center; padding:36px 20px; color:#8b949e; border-top:1px solid #21262d; margin-top:40px; font-size:0.9em; }}
        footer a {{ color:#00E676; text-decoration:none; margin:0 8px; }}
        footer a:hover {{ text-decoration:underline; }}
    </style>
</head>
<body>
    <header>
        <div class="studio-pill">Independent Android App Studio &amp; Field Knowledge Hub</div>
        <h1><span>PB Ideas Virtuales</span></h1>
        <p>Precision Android job-site calculators, DIY engineering field guides, and live streaming thematic radio applications &mdash; built for clarity and offline reliability.</p>
        <nav class="quick-nav" aria-label="Quick sections">
            <a href="#technical-apps">⚙️ Technical Apps</a>
            <a href="#radio-apps">📻 Radio Apps</a>
            <a href="#blogs-directory">📚 Blogs Directory</a>
            <a href="#developer-support">📱 Full Play Store Catalog &amp; Support</a>
        </nav>
    </header>

    <div class="container">
        <section id="technical-apps">
            <div class="section-head">
                <h2>⚙️ Engineering &amp; Field Utility Apps for Android</h2>
                <span>Job-site calculators + dedicated technical blogs</span>
            </div>
            <div class="grid">
                <div class="card" style="border-top:4px solid #F59E0B;">
                    <div>
                        <span class="app-tag" style="color:#F59E0B; border-color:rgba(245,158,11,0.35);">ANDROID APP • CARPENTRY &amp; FRAMING</span>
                        <h3>Framing &amp; Roof Calc: Tape 1/16</h3>
                        <div class="sub-blog"><a href="carpentry_blog/" style="color:#F59E0B;">📐 Carpentry, Roof Framing &amp; Construction Lab</a></div>
                        <p>Visual 1/16&quot; tape zoom, voice-readout rafters (Common, Hip/Valley, Jack), IRC stair stringers, raked walls &amp; concrete volume calculator.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.constructioncarpentrycalc&amp;hl=en_US&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#F59E0B; color:#0d1117;">📲 Get on Google Play</a>
                        <a href="carpentry_blog/" class="btn btn-outline">📖 Technical Blog &rarr;</a>
                    </div>
                </div>

                <div class="card" style="border-top:4px solid #00E676;">
                    <div>
                        <span class="app-tag" style="color:#00E676; border-color:rgba(0,230,118,0.35);">ANDROID APP • ELECTRICAL &amp; SOLAR</span>
                        <h3>Wire Size &amp; Voltage Drop Calc</h3>
                        <div class="sub-blog"><a href="electric_blog/" style="color:#00E676;">⚡ Electrical Engineering &amp; Solar Wiring Lab</a></div>
                        <p>NEC AWG &amp; Metric IEC mm&sup2; cable sizing, voltage drop %, circuit breaker matching (Ib &le; In &le; Iz), 8 metals, motors &amp; 40% conduit fill.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.voltagedropwiresizecalc&amp;hl=en_US&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#00E676; color:#0d1117;">📲 Get on Google Play</a>
                        <a href="electric_blog/" class="btn btn-outline">📖 Technical Blog &rarr;</a>
                    </div>
                </div>

                <div class="card" style="border-top:4px solid #10B981;">
                    <div>
                        <span class="app-tag" style="color:#10B981; border-color:rgba(16,185,129,0.35);">ANDROID APP • RV, HOME &amp; SOLAR</span>
                        <h3>RV &amp; Home Leveler: Solar Calc</h3>
                        <div class="sub-blog"><a href="rv_camper_blog/" style="color:#10B981;">🚐 RV Overlanding, Camper Leveling &amp; HVAC Lab</a></div>
                        <p>Voice-guided wheelbase block leveling, 3-degree absorption fridge warning, 2% drain slope, BTU/kW HVAC &amp; LiFePO4 off-grid solar sizing.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.rvcamperleveler&amp;hl=en_US&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#10B981; color:#0d1117;">📲 Get on Google Play</a>
                        <a href="rv_camper_blog/" class="btn btn-outline">📖 Technical Blog &rarr;</a>
                    </div>
                </div>
            </div>
        </section>

        <section id="radio-apps">
            <div class="section-head">
                <h2>📻 Thematic Live Radio Apps for Android</h2>
                <span>24/7 streaming networks + music history blogs</span>
            </div>
            <div class="grid">
                <div class="card" style="border-top:4px solid #D97706;">
                    <div>
                        <span class="app-tag" style="color:#D97706; border-color:rgba(217,119,6,0.35);">ANDROID APP • COUNTRY MUSIC</span>
                        <h3>Country Radio: Classic &amp; 90s</h3>
                        <div class="sub-blog"><a href="country_radio_blog/" style="color:#D97706;">🤠 Country Radio &amp; Outlaw Legends Chronicle</a></div>
                        <p>Classic country, 90s hits, Nashville bluegrass &amp; Texas Red Dirt streaming 24/7, plus artist biographies and country music trivia.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.countryradio&amp;hl=en_US&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#D97706; color:#0d1117;">📲 Get on Google Play</a>
                        <a href="country_radio_blog/" class="btn btn-outline">📖 Legends Blog &rarr;</a>
                    </div>
                </div>

                <div class="card" style="border-top:4px solid #EF4444;">
                    <div>
                        <span class="app-tag" style="color:#EF4444; border-color:rgba(239,68,68,0.35);">ANDROID APP • HOLIDAY RADIO</span>
                        <h3>Christmas Radio: Holiday Music</h3>
                        <div class="sub-blog"><a href="christmas_radio_blog/" style="color:#EF4444;">🎄 Christmas Radio &amp; Holiday Legends Chronicle</a></div>
                        <p>Vintage 1940s&ndash;1950s crooners, peaceful acoustic Christmas carols 24/7, heartwarming holiday history chronicles &amp; interactive quiz.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.christmasmusicradio&amp;hl=en_US&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#EF4444; color:#ffffff;">📲 Get on Google Play</a>
                        <a href="christmas_radio_blog/" class="btn btn-outline">📖 Holiday Blog &rarr;</a>
                    </div>
                </div>

                <div class="card" style="border-top:4px solid #10B981;">
                    <div>
                        <span class="app-tag" style="color:#10B981; border-color:rgba(16,185,129,0.35);">ANDROID APP • RADIOS DE MÉXICO</span>
                        <h3>Radios de México FM AM En Vivo</h3>
                        <div class="sub-blog"><a href="radios_mexico_blog/" style="color:#10B981;">🇲🇽 Radios de México en Vivo y Crónicas</a></div>
                        <p>Emisoras de los 32 estados de la República Mexicana (norteña, ranchera, banda y noticias), 40 crónicas históricas y trivia mexicana.</p>
                    </div>
                    <div class="btn-row">
                        <a href="https://play.google.com/store/apps/details?id=com.pbideasvirtuales.radiomexicofmam&amp;hl=es_419&amp;gl=US&amp;referrer=utm_source%3Dgithub_hub%26utm_medium%3Ddeveloper_portal%26utm_campaign%3Dhub_v1" target="_blank" rel="noopener" class="btn" style="background:#10B981; color:#0d1117;">📲 Descargar en Play Store</a>
                        <a href="radios_mexico_blog/" class="btn btn-outline">📖 Blog de Crónicas &rarr;</a>
                    </div>
                </div>
            </div>
        </section>

        <section id="blogs-directory">
            <div class="section-head">
                <h2>📚 Blogs Directory &amp; Reference Portals</h2>
                <span>Browse articles, interactive tools &amp; guides directly by category</span>
            </div>
            <div class="blogs-split">
                <div class="blog-dir-box" style="border-top:3px solid #00E676;">
                    <h3>🛠️ Technical &amp; Engineering Blogs</h3>
                    <p class="dir-sub">Field math, building codes (IRC / NEC / IEC), interactive web estimators &amp; DIY reference sheets.</p>
                    <ul class="blog-list">
                        <li>
                            <a href="carpentry_blog/" style="color:#F59E0B;">📐 Carpentry &amp; Roof Framing Blog &rarr;</a>
                            <small>Roof pitch X:12, common rafters, birdsmouth IRC rules, 1/16&quot; tape fractions, framing corners &amp; concrete yards.</small>
                        </li>
                        <li>
                            <a href="electric_blog/" style="color:#00E676;">⚡ Electrical &amp; Solar Wiring Blog &rarr;</a>
                            <small>AWG vs. mm&sup2; conductor sizing, voltage drop limits, breaker coordination, conduit fill &amp; LiFePO4 nickel strips.</small>
                        </li>
                        <li>
                            <a href="rv_camper_blog/" style="color:#10B981;">🚐 RV Overlanding &amp; Camper Leveling Blog &rarr;</a>
                            <small>3-degree fridge safety, LiFePO4 vs. AGM cold-weather charging, solar MPPT/DC-DC &amp; diesel heater altitude tuning.</small>
                        </li>
                    </ul>
                </div>

                <div class="blog-dir-box" style="border-top:3px solid #D97706;">
                    <h3>🎙️ Music, Radio &amp; Cultural Blogs</h3>
                    <p class="dir-sub">Artist biographies, seasonal traditions, cultural chronicles &amp; music history portals.</p>
                    <ul class="blog-list">
                        <li>
                            <a href="country_radio_blog/" style="color:#D97706;">🤠 Country Radio &amp; Outlaw Legends Blog &rarr;</a>
                            <small>Johnny Cash, Hank Williams, Dolly Parton, Willie Nelson &amp; Nashville songwriting history.</small>
                        </li>
                        <li>
                            <a href="christmas_radio_blog/" style="color:#EF4444;">🎄 Christmas Radio &amp; Holiday Legends Blog &rarr;</a>
                            <small>Classic holiday carol origins, Handel&apos;s Messiah, Saint Nicholas, Saint Francis &amp; vintage crooners.</small>
                        </li>
                        <li>
                            <a href="radios_mexico_blog/" style="color:#10B981;">🇲🇽 Blog de Radios de México y Leyendas &rarr;</a>
                            <small>Crónicas de ídolos del deporte, cultura e historia de México (El Santo, Chávez, Hugo Sánchez, Valenzuela).</small>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <section id="developer-support">
            <div class="dev-box">
                <div class="dev-box-text">
                    <h2>📱 PB Ideas Virtuales on Google Play &amp; Developer Support</h2>
                    <p>Looking for our full catalog (including Rock, Jazz, Blues, Classical, Retro 50s&ndash;90s &amp; regional streaming apps)? All applications listed here are independently developed for Android by <strong>PB Ideas Virtuales</strong>.<br>
                    Support &amp; privacy inquiries: <a href="mailto:pb.ideasvirtuales@gmail.com" style="color:#00E676;">pb.ideasvirtuales@gmail.com</a></p>
                </div>
                <div class="btn-row">
                    <a href="https://play.google.com/store/apps/developer?id=PB+Ideas+Virtuales" target="_blank" rel="noopener" class="btn" style="background:#00E676; color:#0d1117;">View Full Google Play Catalog &rarr;</a>
                </div>
            </div>
        </section>
    </div>

    <footer>
        <p>&copy; 2026 PB Ideas Virtuales (Independent Android Developer) &bull; <a href="privacidad-utilidades.html">Privacy Policy (Utilities)</a> &bull; <a href="privacidad.html">Privacy Policy (Media)</a> &bull; <a href="sitemap.xml">Sitemap</a> &bull; <a href="mailto:pb.ideasvirtuales@gmail.com">Support</a></p>
    </footer>
</body>
</html>"""
    auditar_politicas_estrictas(index_html, "root index.html")
    (REPO_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print("Master index.html updated.")


def rebuild_blogs(all_articles: list, target_blogs: list = None) -> None:
    """
    Render target blogs (or all 6 blogs when target_blogs is None), audit HTML output,
    and update master sitemap.xml + index.html.
    """
    all_site_urls = [f"{SITE_URL}/"]

    for blog_slug, blog_cfg in BLOG_CONFIGS.items():
        blog_articles = [a for a in all_articles if a["blog"] == blog_slug]
        all_site_urls.append(f"{SITE_URL}/{blog_slug}/")
        for a in blog_articles:
            all_site_urls.append(f"{SITE_URL}/{blog_slug}/{a['slug']}.html")

        if target_blogs is not None and blog_slug not in target_blogs:
            continue

        blog_dir = REPO_DIR / blog_slug
        blog_dir.mkdir(parents=True, exist_ok=True)
        (blog_dir / "assets").mkdir(parents=True, exist_ok=True)

        print(f"Building [{blog_slug}] ({len(blog_articles)} articles)...")
        for art in blog_articles:
            html = render_article_page(blog_cfg, art, blog_articles)
            auditar_politicas_estrictas(html, f"{blog_slug}/{art['slug']}.html")
            (blog_dir / f"{art['slug']}.html").write_text(html, encoding="utf-8")

        index_html = render_blog_index(blog_cfg, blog_articles)
        auditar_politicas_estrictas(index_html, f"{blog_slug}/index.html")
        (blog_dir / "index.html").write_text(index_html, encoding="utf-8")

    build_master_sitemap(all_site_urls)
    build_master_index()
