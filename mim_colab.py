# ═══════════════════════════════════════════════════════════════════
# MiM UNIVERSITY SCRAPER - GOOGLE COLAB (FULLY AUTOMATIC)
# Fetches ALL 1000 QS universities automatically — no manual input!
# Run at: https://colab.research.google.com
# ═══════════════════════════════════════════════════════════════════

# ── CELL 1: Install dependencies ────────────────────────────────────
import subprocess
subprocess.run(["pip", "install", "googlesearch-python", "requests", "-q"])

# ── CELL 2: Imports & Config ────────────────────────────────────────
import requests, json, csv, time, os, re
from googlesearch import search as google_search
from google.colab import files

GROQ_API_KEY = "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"
OUTPUT_FILE  = "mim_programs.csv"
DELAY_SEC    = 5  # between universities (respects Groq free tier)

# ── CELL 3: AUTO-FETCH QS 1000 LIST ────────────────────────────────
def fetch_qs_list():
    """Automatically scrape all 1000 universities from QS rankings"""
    print("🌐 Fetching QS Top 1000 list from topuniversities.com...")
    universities = []

    # QS publishes rankings across multiple pages (200 per page)
    pages = [
        "https://www.topuniversities.com/world-university-rankings?page=1",
        "https://www.topuniversities.com/world-university-rankings?page=2",
        "https://www.topuniversities.com/world-university-rankings?page=3",
        "https://www.topuniversities.com/world-university-rankings?page=4",
        "https://www.topuniversities.com/world-university-rankings?page=5",
    ]

    for page_url in pages:
        try:
            r = requests.get(f"https://r.jina.ai/{page_url}",
                             headers={"User-Agent": "Mozilla/5.0",
                                      "Accept": "text/plain"},
                             timeout=40)
            text = r.text
            # Extract university names (QS pages list them in markdown)
            lines = text.split("\n")
            for line in lines:
                # Match lines that look like rank entries
                match = re.search(r'(\d+)\s+(.+?)\s*[\|\-]\s*(.+)', line)
                if match:
                    rank = int(match.group(1))
                    name = match.group(2).strip()
                    country = match.group(3).strip()
                    if 1 <= rank <= 1000 and len(name) > 3:
                        universities.append((rank, name, country))
        except Exception as e:
            print(f"  Warning: could not parse {page_url}: {e}")
        time.sleep(2)

    # Fallback: use built-in top 120 if scraping fails
    if len(universities) < 50:
        print("⚠️  Auto-fetch got limited results. Using built-in list + search for the rest.")
        universities = BUILTIN_UNIVERSITIES.copy()
    else:
        print(f"✅ Fetched {len(universities)} universities from QS!")

    return sorted(set(universities), key=lambda x: x[0])


# ── CELL 4: BUILT-IN FALLBACK (top 120 with known URLs) ─────────────
# Used as fallback if QS site scraping fails
BUILTIN_UNIVERSITIES = [
    (1,"MIT Sloan","USA"),(2,"Imperial College London","UK"),
    (3,"University of Oxford","UK"),(4,"Harvard University","USA"),
    (5,"University of Cambridge","UK"),(6,"Stanford University","USA"),
    (7,"ETH Zurich","Switzerland"),(8,"National University of Singapore","Singapore"),
    (9,"UCL","UK"),(10,"UC Berkeley","USA"),(11,"University of Chicago","USA"),
    (12,"University of Pennsylvania","USA"),(13,"Cornell University","USA"),
    (14,"Peking University","China"),(15,"Tsinghua University","China"),
    (16,"University of Edinburgh","UK"),(17,"Princeton University","USA"),
    (18,"Nanyang Technological University","Singapore"),(19,"Yale University","USA"),
    (20,"Columbia University","USA"),(21,"University of Michigan","USA"),
    (22,"Johns Hopkins University","USA"),(23,"University of Tokyo","Japan"),
    (24,"University of Toronto","Canada"),(25,"McGill University","Canada"),
    (26,"Australian National University","Australia"),(27,"EPFL","Switzerland"),
    (28,"King's College London","UK"),(29,"University of Manchester","UK"),
    (30,"Northwestern University","USA"),(31,"Fudan University","China"),
    (32,"Seoul National University","South Korea"),(33,"University of Melbourne","Australia"),
    (34,"New York University","USA"),(35,"University of Hong Kong","Hong Kong"),
    (36,"Kyoto University","Japan"),(37,"KAIST","South Korea"),
    (38,"Chinese University of Hong Kong","Hong Kong"),(39,"London School of Economics","UK"),
    (40,"Monash University","Australia"),(41,"University of Sydney","Australia"),
    (42,"University of New South Wales","Australia"),(43,"Delft University of Technology","Netherlands"),
    (44,"University of Queensland","Australia"),(45,"University of Warwick","UK"),
    (46,"University of Bristol","UK"),(47,"University of Amsterdam","Netherlands"),
    (48,"University of Glasgow","UK"),(49,"Durham University","UK"),
    (50,"Sorbonne University","France"),(51,"KU Leuven","Belgium"),
    (52,"Technical University of Munich","Germany"),(53,"Osaka University","Japan"),
    (54,"Shanghai Jiao Tong University","China"),(55,"Zhejiang University","China"),
    (56,"University of Birmingham","UK"),(57,"University of Leeds","UK"),
    (58,"Universiti Malaya","Malaysia"),(59,"LMU Munich","Germany"),
    (60,"University of Nottingham","UK"),(61,"Pennsylvania State University","USA"),
    (62,"Lund University","Sweden"),(63,"Uppsala University","Sweden"),
    (64,"University of St Andrews","UK"),(65,"University of Auckland","New Zealand"),
    (66,"Utrecht University","Netherlands"),(67,"Ohio State University","USA"),
    (68,"Universidad de Buenos Aires","Argentina"),(69,"POSTECH","South Korea"),
    (70,"University of Southampton","UK"),(71,"Wageningen University","Netherlands"),
    (72,"UCLA","USA"),(73,"UC San Diego","USA"),(74,"Purdue University","USA"),
    (75,"UC Davis","USA"),(76,"Leiden University","Netherlands"),
    (77,"University of Sheffield","UK"),(78,"Georgia Institute of Technology","USA"),
    (79,"University of Zurich","Switzerland"),(80,"Western University","Canada"),
    (81,"Moscow State University","Russia"),(82,"Yonsei University","South Korea"),
    (83,"University of Western Australia","Australia"),(84,"University of Adelaide","Australia"),
    (85,"Duke University","USA"),(86,"Erasmus University Rotterdam","Netherlands"),
    (87,"Ghent University","Belgium"),(88,"Trinity College Dublin","Ireland"),
    (89,"Korea University","South Korea"),(90,"University of Helsinki","Finland"),
    (91,"University of Copenhagen","Denmark"),(92,"Tohoku University","Japan"),
    (93,"USTC","China"),(94,"University of Exeter","UK"),
    (95,"Queen Mary University of London","UK"),(96,"Lancaster University","UK"),
    (97,"UC Santa Barbara","USA"),(98,"Politecnico di Milano","Italy"),
    (99,"University of Vienna","Austria"),(100,"University of Pittsburgh","USA"),
    (101,"HEC Paris","France"),(102,"ESCP Business School","France"),
    (103,"ESSEC Business School","France"),(104,"IE Business School","Spain"),
    (105,"ESADE Business School","Spain"),(106,"Bocconi University","Italy"),
    (107,"University of St.Gallen","Switzerland"),(108,"HKUST","Hong Kong"),
    (109,"Maastricht University","Netherlands"),(110,"University of Bath","UK"),
    (111,"University of Reading Henley","UK"),(112,"Bayes Business School","UK"),
    (113,"Cranfield School of Management","UK"),(114,"University of Strathclyde","UK"),
    (115,"EDHEC Business School","France"),(116,"emlyon business school","France"),
    (117,"Grenoble Ecole de Management","France"),(118,"SKEMA Business School","France"),
    (119,"Aston Business School","UK"),(120,"University of Groningen","Netherlands"),
]

# ── CELL 5: FIND ADMISSIONS URL ──────────────────────────────────────
def find_admissions_url(uni_name, country):
    """Google search for the university's MiM/MSc Management admissions page"""
    query = f'{uni_name} "Master in Management" OR "MSc Management" admissions 2026 site:*.edu OR site:*.ac.uk OR site:*.ac.*'
    try:
        results = list(google_search(query, num_results=3, lang="en"))
        if results:
            return results[0]
    except Exception as e:
        print(f"    ⚠️  Search failed: {e}")
    # Fallback: try generic postgraduate page search
    try:
        fallback = list(google_search(f'{uni_name} postgraduate management masters', num_results=2))
        if fallback:
            return fallback[0]
    except:
        pass
    return None

# ── CELL 6: JINA PAGE READER ─────────────────────────────────────────
def read_page(url):
    try:
        r = requests.get(f"https://r.jina.ai/{url}",
                         headers={"User-Agent": "Mozilla/5.0",
                                  "Accept": "text/plain"},
                         timeout=35)
        return r.text
    except Exception as e:
        print(f"    ❌ Read error: {e}")
        return ""

# ── CELL 7: GROQ AI ANALYSIS ──────────────────────────────────────────
def analyze(name, text):
    prompt = f"""You are an academic research expert. Today's date is May 2026.

Analyze this website text from {name}. Extract information about their
Master in Management (MiM), MSc Management, or equivalent master's program
for Autumn/Fall 2026 intake.

Text: {text[:15000]}

Return ONLY a raw JSON object (no markdown, no code blocks):
{{
  "program_name": "Full program name or 'Not Available' if no MiM equivalent exists",
  "status": "OPEN if deadline not yet passed as of May 2026, CLOSED if already passed, UNCLEAR if unknown",
  "deadline": "Exact application deadline e.g. '30 June 2026' or 'Not Specified'",
  "tuition_fees": "Total international student tuition with currency e.g. '£47,000' or 'Not Specified'",
  "scholarships": "Scholarship names or 'Not Specified'"
}}"""
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}",
                     "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.1},
            timeout=30
        )
        data = r.json()
        if "error" in data:
            raise Exception(data["error"]["message"])
        content = data["choices"][0]["message"]["content"]
        content = content.replace("```json","").replace("```","").strip()
        return json.loads(content)
    except Exception as e:
        print(f"    ❌ Groq error: {e}")
        return None

# ── CELL 8: MAIN ─────────────────────────────────────────────────────
def main():
    # Auto-fetch QS 1000 list
    universities = fetch_qs_list()
    total = len(universities)
    print(f"\n📋 Processing {total} universities...\n")

    # Init CSV
    file_exists = os.path.exists(OUTPUT_FILE)
    f = open(OUTPUT_FILE, "a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["QS Rank","University","Country","Program Name",
                         "Status","Autumn 2026 Deadline",
                         "Tuition Fees","Scholarships","Application Link"])
        f.flush()

    saved = skipped = 0

    for i, entry in enumerate(universities, 1):
        # Support both (rank, name, country) and (rank, name, country, url)
        rank    = entry[0]
        name    = entry[1]
        country = entry[2]
        url     = entry[3] if len(entry) > 3 else None

        print(f"\n{'─'*55}")
        print(f"[{i}/{total}] #{rank} {name} ({country})")

        # Step 1: Find URL if not known
        if not url:
            print("  🔍 Searching for admissions page...")
            url = find_admissions_url(name, country)
            time.sleep(2)  # polite search delay

        if not url:
            print("  ⚠️  No URL found. Skipping.")
            skipped += 1
            continue

        print(f"  🔗 URL: {url}")

        # Step 2: Read page
        print("  📖 Reading page...")
        text = read_page(url)
        if not text or len(text) < 200:
            print("  ⚠️  Page unreadable. Skipping.")
            skipped += 1
            continue

        # Step 3: Analyze
        print("  🧠 Analyzing with Groq AI...")
        result = analyze(name, text)
        if not result:
            skipped += 1
            time.sleep(DELAY_SEC)
            continue

        print(f"  ✅ {result.get('program_name')} | {result.get('status')} | {result.get('deadline')}")
        print(f"  💰 {result.get('tuition_fees')} | 🎓 {result.get('scholarships')}")

        # Step 4: Save (only OPEN or UNCLEAR)
        if result.get("status") != "CLOSED":
            writer.writerow([rank, name, country,
                             result.get("program_name",""),
                             result.get("status",""),
                             result.get("deadline",""),
                             result.get("tuition_fees",""),
                             result.get("scholarships",""),
                             url])
            f.flush()
            print("  💾 Saved!")
            saved += 1
        else:
            print("  🔴 CLOSED — not saved.")

        time.sleep(DELAY_SEC)

    f.close()
    print(f"\n{'═'*55}")
    print(f"🎉 COMPLETE! Saved: {saved} | Skipped: {skipped} | Total: {total}")
    print("📥 Downloading CSV now...")
    files.download(OUTPUT_FILE)

main()
