import requests, json, csv, time, os
from ddgs import DDGS
from universities_data import QS_UNIVERSITIES as UNIVERSITIES

GROQ_API_KEY = "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"
OUTPUT_FILE = "mim_programs.csv"

def analyze(name, search_results):
    snippets = ""
    for r in search_results:
        snippets += r.get("title", "") + ": " + r.get("body", "") + "\n"
        
    prompt = f"""You are an academic researcher. Analyze these search results for {name} Master in Management (MiM) program for Autumn/Fall 2026.
If snippets are in another language, translate them internally.
Search Snippets:
{snippets}

CRITICAL INSTRUCTION: If the exact tuition fees or deadlines are missing from the snippets, YOU MUST USE YOUR OWN INTERNAL KNOWLEDGE BASE to provide the historically accurate estimated tuition fees and application deadline months for this specific university. DO NOT output "Not Specified" unless you genuinely have no knowledge of this university.

Return ONLY raw JSON (no markdown):
{{"program_name":"exact program name","status":"OPEN or CLOSED or UNCLEAR","deadline":"exact date or typical months","tuition_fees":"amount with currency","scholarships":"names or Not Specified"}}"""
    
    models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "qwen/qwen3-32b"]
    max_retries = 100
    current_model_idx = 0
    
    for attempt in range(max_retries):
        model_name = models[current_model_idx % len(models)]
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "response_format": {"type": "json_object"}
                },
                timeout=30
            )
            data = r.json()
            if "error" in data:
                err_msg = str(data["error"].get("message", data["error"]))
                if "Rate limit" in err_msg or "Please try again in" in err_msg:
                    wait_time = 20.0
                    import re
                    # Example formats: "try again in 14.3s", "try again in 1m20s", "try again in 2h3m"
                    h_match = re.search(r'([\d\.]+)h', err_msg)
                    m_match = re.search(r'([\d\.]+)m', err_msg)
                    s_match = re.search(r'([\d\.]+)s', err_msg)
                    
                    if h_match or m_match or s_match:
                        wait_time = 0.0
                        if h_match: wait_time += float(h_match.group(1)) * 3600
                        if m_match: wait_time += float(m_match.group(1)) * 60
                        if s_match: wait_time += float(s_match.group(1))
                        wait_time += 2.0 # buffer
                        
                    if wait_time > 60.0:
                        print(f"    Daily limit hit on {model_name}. Switching models...", flush=True)
                        current_model_idx += 1
                        continue
                        
                    print(f"    Rate limit hit. Waiting {wait_time:.1f}s...", flush=True)
                    time.sleep(wait_time)
                    continue
                
                # if another error happens, just switch models
                print(f"    API Error: {err_msg}. Switching models...", flush=True)
                current_model_idx += 1
                continue
                
            content = data["choices"][0]["message"]["content"].replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            if isinstance(parsed, list) and len(parsed) > 0:
                parsed = parsed[0]
            if not isinstance(parsed, dict):
                raise Exception("JSON is not a dictionary")
            return parsed
        except Exception as e:
            if attempt < max_retries - 1:
                # network error or parsing error, fallback model
                current_model_idx += 1
                time.sleep(2)
            else:
                return None

def main():
    print("=== RESUMING SCRAPER ===", flush=True)
    
    saved_urls = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                next(reader)
                for row in reader:
                    if len(row) > 8:
                        saved_urls.add(row[8])
            except: pass
    else:
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["QS Rank", "University", "Country", "Program Name", "Status", "Autumn 2026 Deadline", "Tuition Fees", "Scholarships", "Application Link"])

    for rank, name, country, default_url in UNIVERSITIES:
        if default_url in saved_urls:
            continue
            
        print(f"\n[{rank}/{len(UNIVERSITIES)}] {name} ({country})", flush=True)
        
        # 1. Search for the exact admissions/deadline page using DuckDuckGo
        search_query = f"{name} official Master in Management admissions deadline tuition fees"
        target_url = default_url
        search_results = []
        try:
            search_results = DDGS().text(search_query, max_results=4)
            if search_results and len(search_results) > 0:
                target_url = search_results[0]['href']
                print(f"  Found Admissions URL: {target_url}", flush=True)
        except Exception as e:
            print(f"  Search error: {e}.", flush=True)
            
        if not search_results:
            print("  SKIPPED - search failed", flush=True)
            continue

        try:
            result = analyze(name, search_results)
            if not result:
                time.sleep(1)
                continue

            status = result.get("status", "UNCLEAR")
            program = result.get("program_name", "")
            deadline = result.get("deadline", "")
            fees = result.get("tuition_fees", "")
            scholarships = result.get("scholarships", "")

            print(f"  Program  : {program}", flush=True)
            print(f"  Status   : {status} | Deadline: {deadline}", flush=True)
            print(f"  Fees     : {fees}", flush=True)

            if status != "CLOSED":
                with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([rank, name, country, program, status, deadline, fees, scholarships, target_url])
                print("  >>> SAVED TO CSV <<<", flush=True)
        except Exception as e:
            print(f"  CRITICAL ERROR processing {name}: {e}", flush=True)

        time.sleep(2)
    print("\n=== COMPLETE ===", flush=True)

if __name__ == "__main__":
    main()
