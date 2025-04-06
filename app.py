import streamlit as st
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import random
import string
import feedparser
import matplotlib.pyplot as plt

st.set_page_config(page_title="Adstralia Community Tools", layout="wide")
st.markdown("""
    <style>
        .main > div {
            padding-top: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            padding: 12px;
        }
        .stCodeBlock pre {
            background-color: #f5f5f5;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Branding
st.sidebar.image("logo.png", width=180)
st.sidebar.markdown("""
### 💼 Adstralia Community Tools
Helping Aussie businesses grow smarter with SEO, automation & digital strategy.

📧 [info@adstralia.com.au](mailto:info@adstralia.com.au)  
🌐 [www.adstralia.com.au](https://www.adstralia.com.au)
---
""")

st.title("🌱 Adstralia Community Tools")
st.caption("Helping local Aussie businesses thrive online with smart, free tools 🇦🇺")

# Tool: Local SEO Analyzer
def local_seo_analyzer():
    st.header("🔍 Advanced Local SEO Analyzer")
    url = st.text_input("Enter your business website URL:", key="seo_url")
    keyword = st.text_input("Enter your local keyword (e.g. 'Melbourne plumber')", key="seo_keyword")

    if url and st.button("Analyze", key="seo_analyze"):
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            score = 0
            total = 8

            title = soup.title.string.strip() if soup.title else "N/A"
            meta_desc = soup.find("meta", attrs={"name": "description"})
            has_viewport = bool(soup.find("meta", attrs={"name": "viewport"}))
            phone_present = bool(re.search(r'(\+?61\s*|0)[\(\)\d\s\-]{8,}', soup.text))
            address_present = bool(re.search(r'(\d+\s+)?[\w\s]+(St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Parade|Drive|Dr)\b', soup.text, re.IGNORECASE))
            map_embed = bool(re.search(r'www.google.com/maps/embed', soup.decode()))
            schema_local = 'LocalBusiness' in soup.decode()
            alt_images = soup.find_all("img", alt=True)
            h_tags = soup.find_all(['h1', 'h2', 'h3'])

            keyword_in_title = keyword.lower() in title.lower() if keyword else False
            keyword_in_headings = any(keyword.lower() in h.get_text().lower() for h in h_tags) if keyword else False

            score += int(bool(title != "N/A"))
            score += int(bool(meta_desc))
            score += int(has_viewport)
            score += int(phone_present)
            score += int(address_present)
            score += int(map_embed)
            score += int(schema_local)
            score += int(len(alt_images) >= 3)

            st.metric("Local SEO Score", f"{score}/{total}")
            st.markdown("---")

            st.write("**Title Tag:**", title)
            st.write("**Meta Description:**", meta_desc['content'] if meta_desc else "❌ Missing")
            st.write("**Mobile Friendly (Viewport Tag):**", "✅ Yes" if has_viewport else "❌ No")
            st.write("**Phone Number on Page:**", "✅ Found" if phone_present else "❌ Not Found")
            st.write("**Address Present (NAP):**", "✅ Yes" if address_present else "❌ No")
            st.write("**Google Maps Embed:**", "✅ Yes" if map_embed else "❌ No")
            st.write("**Schema.org Markup (LocalBusiness):**", "✅ Yes" if schema_local else "❌ No")
            st.write("**Images with Alt Tags:**", len(alt_images))

            if keyword:
                st.markdown("---")
                st.subheader("📌 Keyword Presence Check")
                st.write(f"**Keyword in Title:** {'✅ Yes' if keyword_in_title else '❌ No'}")
                st.write(f"**Keyword in H1–H3 Tags:** {'✅ Yes' if keyword_in_headings else '❌ No'}")

        except Exception as e:
            st.error(f"Failed to analyze site: {e}")

# Tool: Business Name Generator (Enhanced)
def business_name_generator():
    st.header("🤖 Business Name Generator (Advanced)")
    industry = st.text_input("What's your industry or niche?", key="biz_industry")
    keywords = st.text_input("Optional: Enter keywords (comma-separated)", key="biz_keywords")
    style = st.selectbox("Choose naming style:", ["Brandable", "Aussie Slang", "Creative", "Minimalist"], key="biz_style")
    if industry and st.button("Generate Business Names", key="generate_names"):
        random_words = [
            "Koala", "Boomerang", "Wattle", "Billabong", "Dingo", "Echo", "Nimbus", "Sprout", "Zentrix", "Nudge",
            "Kookaburra", "Outback", "Coral", "Tassie", "Wombat", "Platypus", "Bushfire", "Snag", "Vegemite", "Uluru",
            "Larrikin", "Bushland", "Booma", "Sunburnt", "Emu", "Booma", "Wander", "Didgeridoo", "Sunset", "Bluegum",
            "Croco", "Aussura", "Shazza", "Wazza", "Eucaly", "Tinnie", "Dusty", "Snappy", "Sunny", "Jackaroo", "Outroo",
            "Jillaroo", "Trackie", "Drongo", "Tazzy", "Ocker", "Bushie", "Koality", "Truebrand", "Wattleleaf", "Redcentre"
        ]

        endings = [
            "ify", "sy", "loop", "scape", "works", "mate", "craft", "tap", "ly", "gen",
            "hub", "crate", "pulse", "flow", "zone", "nation", "boom", "nest", "click", "pop",
            "dash", "pilot", "fuel", "fix", "core", "crew", "forge", "lift", "stack", "lab",
            "mint", "spark", "wave", "deck", "byte", "snap", "bot", "link", "grid", "mill",
            "bay", "nova", "port", "cart", "node", "tap", "rise", "tag", "co", "dna"
        ]

        slangs = [
            "True Blue", "Fair Dinkum", "Ripper", "Bonza", "No Worries", "Bloody Beaut", "Straya", "Legendary", "Aussie Made",
            "Mate’s Rates", "Crikey Good", "Too Right", "Deadset", "You Beaut", "Fair Go", "Flat Out", "Hard Yakka",
            "Bush Bred", "Strewth", "Good Onya", "Grouse", "Onya Mate", "Avo Legend", "Fair Crack", "Aussie As",
            "Outback Strong", "Top Notch", "Choice Bro", "Ridgy Didge", "Snag King", "Chockers Biz", "Hot Tin", "Top Bloke",
            "Veggie Mate", "Sausage Roll", "Witchetty Tough", "True Cobber", "Fair Trade-o", "Real Deal", "Flamin' Good",
            "Oathworthy", "Dinkum Digital", "No Drama", "Local As", "Jackaroo Ready", "Dropbear Safe", "Swagman Style",
            "Dusty Deals", "Croc-Approved", "Proper Ripper"
        ]

        user_words = [w.strip().capitalize() for w in keywords.split(",") if w.strip()] if keywords else []
        all_combos = []

        base = industry.lower()
        sources = random_words + user_words if user_words else random_words

        for i in range(15):
            prefix = random.choice(sources)
            suffix = random.choice(endings)
            slang_prefix = random.choice(slangs)

            brandable = f"{prefix}{base[:3]}{suffix}".capitalize()
            creative = f"{base.capitalize()}{suffix}".capitalize()
            slang = f"{slang_prefix} {prefix} {base.capitalize()}"
            mini = f"{base[:4].capitalize()}Co"

            if style == "Brandable":
                all_combos.append(brandable)
            elif style == "Creative":
                all_combos.append(creative)
            elif style == "Aussie Slang":
                all_combos.append(slang)
            elif style == "Minimalist":
                all_combos.append(mini)

        unique_names = list(set(all_combos))[:5]
        st.success("Here are your advanced business name ideas:")
        for name in unique_names:
            st.markdown(f"🎯 <span style='font-size:18px;font-weight:bold;'>{name}</span>", unsafe_allow_html=True)

# Tool: Business Health Report
def business_health_check():
    st.header("📋 Business Health Report")
    url = st.text_input("Enter your website URL:", key="health_url")
    if url and st.button("Run Report", key="health_check"):
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            ssl = url.startswith("https")
            mobile_friendly = bool(soup.find("meta", attrs={"name": "viewport"}))
            contact_present = bool(re.search(r'(\+?61|0)[\s\d]{9,}', soup.text))
            email_present = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', soup.text))
            has_logo = bool(soup.find("img", src=re.compile("logo")))
            h1_count = len(soup.find_all('h1'))

            score = sum([ssl, mobile_friendly, contact_present, email_present, has_logo, h1_count > 0])

            st.metric("Health Score", f"{score}/6")
            st.write("**SSL Enabled:**", "✅" if ssl else "❌")
            st.write("**Mobile Friendly:**", "✅" if mobile_friendly else "❌")
            st.write("**Phone Number Visible:**", "✅" if contact_present else "❌")
            st.write("**Email Address Present:**", "✅" if email_present else "❌")
            st.write("**Logo Image Present:**", "✅" if has_logo else "❌")
            st.write("**At least one H1 Tag:**", "✅" if h1_count > 0 else "❌")
        except Exception as e:
            st.error(f"Error fetching site: {e}")

# Tool: Email Signature Generator
def email_signature_generator():
    st.header("✉️ Email Signature Generator")
    name = st.text_input("Full Name", key="sig_name")
    title = st.text_input("Job Title", key="sig_title")
    phone = st.text_input("Phone", key="sig_phone")
    email = st.text_input("Email", key="sig_email")
    website = st.text_input("Website", key="sig_website")
    logo_url = st.text_input("Logo URL (Optional)", key="sig_logo")
    facebook = st.text_input("Facebook URL", key="sig_facebook")
    linkedin = st.text_input("LinkedIn URL", key="sig_linkedin")
    instagram = st.text_input("Instagram URL", key="sig_instagram")
    color = st.color_picker("Choose your theme color:", "#00695c", key="sig_color")

    if st.button("Generate Signature", key="generate_signature"):
        html_sig = f"""
        <div style='font-family:sans-serif; color:{color};'>
            <strong style='color:{color};'>{name}</strong><br>
            <span>{title}</span><br>
            📞 <a href='tel:{phone}' style='color:{color}; text-decoration:none;'>{phone}</a> | 
            ✉️ <a href='mailto:{email}' style='color:{color}; text-decoration:none;'>{email}</a><br>
            🌐 <a href='{website}' style='color:{color}; text-decoration:none;'>{website}</a><br>
            {'<img src="' + logo_url + '" height="50">' if logo_url else ''}<br>
            {' '.join([f'<a href="{link}" style="color:{color}; text-decoration:none;">{platform}</a>' for platform, link in [('Facebook', facebook), ('LinkedIn', linkedin), ('Instagram', instagram)] if link])}
        </div>
        """
        st.markdown("### ✨ Your Branded Email Signature")
        st.code(html_sig, language='html')
        st.success("Copy and paste this HTML into your email settings or signature block.")

# Australian Government Support Tab
def gov_support_resources():
    st.header("🇦🇺 Government Help & Resources for Aussie Small Businesses")
    st.markdown("""
    The Australian Government provides a wide range of tools, grants, guides, and advice for small business owners. Whether you're starting out or scaling up, these official resources are designed to support your business success.
    
    **Explore official links below:**
    """)

    resources = [
        ("Business.gov.au – Main Hub for Small Business", "https://business.gov.au"),
        ("Grants and Programs Finder", "https://business.gov.au/grants-and-programs"),
        ("ATO – Small Business Tax Deductions & Help", "https://www.ato.gov.au/Business/Small-business-entity-concessions/"),
        ("Australian Business Licence and Information Service (ABLIS)", "https://ablis.business.gov.au/"),
        ("ASIC Business Name Registration", "https://asic.gov.au/for-business/registering-a-business-name/"),
        ("Fair Work – Hiring and Managing Staff", "https://www.fairwork.gov.au/"),
        ("Small Business Digital Solutions Program", "https://www.business.gov.au/Grants-and-Programs/Digital-Solutions"),
        ("Cyber Security for Small Business (ACSC)", "https://www.cyber.gov.au/"),
        ("IP Australia – Trademarks and Patents", "https://www.ipaustralia.gov.au/"),
        ("Business Victoria – Local Grants and Support", "https://business.vic.gov.au"),
        ("NSW Small Business Commission", "https://www.smallbusiness.nsw.gov.au"),
        ("Queensland Small Business Services", "https://www.business.qld.gov.au/"),
        ("South Australia Small Business Support", "https://business.sa.gov.au/"),
        ("Western Australia Small Business Development Corporation", "https://www.smallbusiness.wa.gov.au/"),
        ("NT Business Support Services", "https://business.nt.gov.au/"),
        ("Tasmanian Business Resources", "https://www.business.tas.gov.au/"),
        ("Australian Competition & Consumer Commission (ACCC)", "https://www.accc.gov.au/"),
        ("Business Energy Advice Program (BEAP)", "https://www.business.gov.au/Grants-and-Programs/Business-Energy-Advice-Program"),
        ("Export Finance Australia – Support for Exporters", "https://www.exportfinance.gov.au/"),
        ("Starting a Business Checklist", "https://business.gov.au/guide/starting"),
    ]

    for name, url in resources:
        st.markdown(f"🔗 **[{name}]({url})**")

    st.markdown("---")
    st.subheader("📡 Live Cyber & Business Updates (ACSC)")
    feed_url = "https://www.cyber.gov.au/rss"  # ACSC Threat Updates RSS Feed
    feed = feedparser.parse(feed_url)

    if feed.entries:
        for entry in feed.entries[:5]:
            st.markdown(f"🔸 [{entry.title}]({entry.link})")
            st.caption(f"🗓 {entry.published}")
    else:
        st.info("No live updates available at the moment.")

# Add tool interface with tabs
tabs = st.tabs([
    "🔍 Local SEO Analyzer",
    "🤖 Business Name Generator",
    "📋 Business Health Report",
    "✉️ Email Signature Generator",
    "🛠️ Gov Help & Resources",
    "📡 Live Cyber & Business Updates (ACSC)",
    "📅 Important Dates",
    "📄 Free Legal Templates",
    "💰 Grant Finder Guide",
    "🧮 Profit Calculator",
    "🎨 Free Design Tools",
    "📍 Local Directory Guide",
    "🧘 Mental Health & Wellbeing",
    "🌏 Multilingual Resources"
])

with tabs[0]:
    local_seo_analyzer()

with tabs[1]:
    business_name_generator()

with tabs[2]:
    business_health_check()

with tabs[3]:
    email_signature_generator()
with tabs[4]:
    gov_support_resources()
with tabs[5]:
    st.header("📡 Live Cyber & Business Updates (ACSC)")
    feed_url = "https://www.cyber.gov.au/rss"
    feed = feedparser.parse(feed_url)

    if feed.entries:
        for entry in feed.entries[:10]:
            st.markdown(f"🔸 [{entry.title}]({entry.link})")
            st.caption(f"🗓 {entry.published}")
    else:
        st.info("No live updates available at the moment.")
with tabs[6]:
    st.header("📅 Important Business Dates")
    st.markdown("""
    Keep track of critical business deadlines in Australia:

    - **Quarterly BAS Due**: 28th of the month following each quarter
    - **EOFY**: June 30  
    - **Tax Return Deadline**: October 31 (or later if using a tax agent)
    - **Super Guarantee Due Dates**: 28th of each quarter
    - [📌 ATO Key Dates](https://www.ato.gov.au/General/Key-dates/)
    """)

with tabs[7]:
    st.header("📄 Free Legal Templates for Small Businesses")
    st.markdown("""
    - [🔒 Privacy Policy (AU Compliant)](https://legalvision.com.au/free-privacy-policy-template-australia/)
    - [📃 Terms & Conditions Template](https://www.lawpath.com.au/templates/website-terms-and-conditions-template)
    - [📝 Simple Service Agreement](https://www.business.gov.au/planning/templates-and-tools/sample-contracts-and-templates)
    - [🔖 NDA (Non-Disclosure Agreement)](https://www.business.vic.gov.au/tools-and-templates/ndas)
    """)

with tabs[8]:
    st.header("💰 Grant Finder & Government Support")
    st.markdown("""
    Discover funding & grant opportunities for your small business:

    - [business.gov.au Grants Finder](https://business.gov.au/grants-and-programs)
    - [GrantConnect](https://www.grants.gov.au/)
    - [ATO Support for Small Business](https://www.ato.gov.au/business/)
    - [NSW Business Grants](https://www.service.nsw.gov.au/)
    """)

with tabs[9]:
    st.header("🧮 Advanced Small Business Profit Calculator")

    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input("Monthly Revenue ($)", min_value=0)
        cost = st.number_input("Cost of Goods Sold ($)", min_value=0)
    with col2:
        overheads = st.number_input("Monthly Overheads / Fixed Costs ($)", min_value=0)
        hours_worked = st.number_input("Monthly Work Hours (for hourly rate calc)", min_value=1, value=160)

    if st.button("💡 Calculate My Business Metrics"):
        gross_profit = revenue - cost
        net_profit = gross_profit - overheads
        profit_margin = (net_profit / revenue) * 100 if revenue else 0
        annual_profit = net_profit * 12
        hourly_rate = net_profit / hours_worked if hours_worked else 0
        breakeven_revenue = overheads + cost

        st.subheader("📊 Your Results")
        col3, col4 = st.columns(2)
        with col3:
            st.success(f"💰 Gross Profit: ${gross_profit:,.2f}")
            st.success(f"📉 Net Monthly Profit: ${net_profit:,.2f}")
            st.info(f"🧮 Profit Margin: {profit_margin:.2f}%")
        with col4:
            st.info(f"📆 Annual Profit Estimate: ${annual_profit:,.2f}")
            st.info(f"💸 Breakeven Revenue Needed: ${breakeven_revenue:,.2f}")
            st.warning(f"⏱️ Effective Hourly Rate: ${hourly_rate:,.2f}")

        # Optional chart
        labels = ["Revenue", "COGS", "Overheads", "Net Profit"]
        values = [revenue, cost, overheads, net_profit]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=["#007ACC", "#FF6347", "#FFA500", "#28a745"])
        ax.set_ylabel("Amount ($)")
        ax.set_title("💼 Monthly Business Financial Summary")
        st.pyplot(fig)


with tabs[10]:
    st.header("🎨 Free Business Design Tools")
    st.markdown("""
    - [Canva for Business](https://www.canva.com/) – Easy social & print designs  
    - [Hatchful by Shopify](https://hatchful.shopify.com/) – Free logo maker  
    - [Remove.bg](https://www.remove.bg/) – Remove image backgrounds  
    - [Looka](https://looka.com/) – AI-powered brand kits  
    """)

with tabs[11]:
    st.header("📍 Local Directory Submission Guide")
    st.markdown("""
    Get your business listed for better visibility & SEO:

    - [📘 Yellow Pages](https://www.yellowpages.com.au/)
    - [📘 StartLocal](https://www.startlocal.com.au/)
    - [📘 AussieWeb](https://www.aussieweb.com.au/)
    - [📘 HotFrog](https://www.hotfrog.com.au/)
    - [📘 TrueLocal](https://www.truelocal.com.au/)
    - [📘 Yelp AU](https://www.yelp.com.au/)
    """)

with tabs[12]:
    st.header("🧘 Mental Health & Business Wellbeing")
    st.markdown("""
    Running a business is tough. Here are support resources:

    - [Beyond Blue – Mental Health Help](https://www.beyondblue.org.au/)
    - [Heads Up – Workplace Wellbeing](https://www.headsup.org.au/)
    - [Small Business Support](https://www.business.gov.au/planning/emergency-management/mental-health-support)
    - [RU OK? for Business](https://www.ruok.org.au/workplace)
    """)

with tabs[13]:
    st.header("🌏 Multilingual Business Resources")
    st.markdown("""
    Support for migrant-owned and multilingual businesses:

    - [Translated ATO Guides](https://www.ato.gov.au/general/translations/)
    - [Business.gov.au Translations](https://business.gov.au/news/multilingual-resources)
    - [Small Business Multicultural Portal](https://www.smallbusiness.wa.gov.au/multicultural)
    """)
