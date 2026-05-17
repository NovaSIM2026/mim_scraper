import requests, json, csv, time, os
from ddgs import DDGS

GROQ_API_KEY = "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"
OUTPUT_FILE = "mim_programs.csv"

UNIVERSITIES = [
    (1,"MIT Sloan","USA","https://mitsloan.mit.edu/mba/program-overview"),
    (2,"Imperial College London","UK","https://www.imperial.ac.uk/business-school/masters/management/"),
    (3,"University of Oxford","UK","https://www.sbs.ox.ac.uk/programmes/mba"),
    (4,"Harvard Business School","USA","https://www.hbs.edu/mba/Pages/default.aspx"),
    (5,"University of Cambridge","UK","https://www.jbs.cam.ac.uk/programmes/mphil-management/"),
    (6,"Stanford GSB","USA","https://www.gsb.stanford.edu/programs/msx"),
    (7,"ETH Zurich","Switzerland","https://ethz.ch/en/studies/master/application.html"),
    (8,"NUS Business School","Singapore","https://bschool.nus.edu.sg/msc-management/"),
    (9,"UCL Management","UK","https://www.ucl.ac.uk/management/study/msc-management"),
    (10,"UC Berkeley Haas","USA","https://haas.berkeley.edu/mfe/"),
    (11,"University of Chicago Booth","USA","https://www.chicagobooth.edu/programs/full-time-mba"),
    (12,"Wharton UPenn","USA","https://mba.wharton.upenn.edu/"),
    (13,"Cornell SC Johnson","USA","https://www.johnson.cornell.edu/programs/two-year-mba/"),
    (14,"Peking University","China","https://english.phbs.pku.edu.cn/Admissions.htm"),
    (15,"Tsinghua SEM","China","https://www.sem.tsinghua.edu.cn/en/Programs/MBAPrograms.htm"),
    (16,"University of Edinburgh","UK","https://www.ed.ac.uk/studying/postgraduate/degrees/index.php?r=site/view&id=989"),
    (17,"Princeton BCF","USA","https://bcf.princeton.edu/master-in-finance/"),
    (18,"Nanyang Business School","Singapore","https://www.ntu.edu.sg/business/programmes/postgraduate/msc-management"),
    (19,"Yale SOM","USA","https://som.yale.edu/programs/mba"),
    (20,"Columbia Business School","USA","https://gsb.columbia.edu/programs/master-of-science/"),
    (21,"Michigan Ross","USA","https://michiganross.umich.edu/graduate/masters"),
    (22,"Johns Hopkins Carey","USA","https://carey.jhu.edu/programs/master-of-science-programs/ms-in-management"),
    (23,"University of Tokyo","Japan","https://www.u-tokyo.ac.jp/en/academics/grad_ms.html"),
    (24,"Rotman Toronto","Canada","https://www.rotman.utoronto.ca/Degrees/MastersPrograms/MasterofManagement"),
    (25,"McGill Desautels","Canada","https://www.mcgill.ca/desautels/programs/grad/mma"),
    (26,"ANU","Australia","https://www.anu.edu.au/study/find-a-course/master-of-management"),
    (27,"EPFL","Switzerland","https://www.epfl.ch/education/master/programs/management-technology-and-entrepreneurship/"),
    (28,"Kings College London","UK","https://www.kcl.ac.uk/study/postgraduate-taught/courses/management-msc"),
    (29,"Manchester Business School","UK","https://www.alliancembs.manchester.ac.uk/study/msc/management/"),
    (30,"Kellogg Northwestern","USA","https://www.kellogg.northwestern.edu/programs/full-time-mba.aspx"),
    (31,"Fudan Management","China","https://www.fdsm.fudan.edu.cn/en/index.aspx"),
    (32,"Seoul National University","South Korea","https://gsba.snu.ac.kr/en/"),
    (33,"University of Melbourne","Australia","https://study.unimelb.edu.au/find/courses/graduate/master-of-management/"),
    (34,"NYU Stern","USA","https://www.stern.nyu.edu/programs-admissions/ms-programs"),
    (35,"University of Hong Kong","Hong Kong","https://msc.hku.hk/"),
    (36,"Kyoto University GSM","Japan","https://www.gsm.kyoto-u.ac.jp/en/"),
    (37,"KAIST Business","South Korea","https://gsm.kaist.ac.kr/en/"),
    (38,"CUHK Business School","Hong Kong","https://www.bschool.cuhk.edu.hk/programs/master-programs/"),
    (39,"London School of Economics","UK","https://www.lse.ac.uk/management/study/msc-management"),
    (40,"Monash Business School","Australia","https://www.monash.edu/study/why-study-at-monash/courses/master-of-management"),
    (41,"University of Sydney","Australia","https://www.sydney.edu.au/courses/courses/pc/master-of-management.html"),
    (42,"UNSW Business","Australia","https://www.unsw.edu.au/study/postgraduate/master-of-management"),
    (43,"TU Delft","Netherlands","https://www.tudelft.nl/en/education/programmes/masters/"),
    (44,"UQ Business School","Australia","https://business.uq.edu.au/programs/postgraduate-coursework"),
    (45,"Warwick Business School","UK","https://warwick.ac.uk/study/postgraduate/courses/mscmanagement/"),
    (46,"University of Bristol","UK","https://www.bristol.ac.uk/study/postgraduate/2026/mgmt/msc-management/"),
    (47,"University of Amsterdam","Netherlands","https://www.uva.nl/en/programmes/masters/business-administration-management/msc-business-administration.html"),
    (48,"University of Glasgow","UK","https://www.gla.ac.uk/postgraduate/taught/management/"),
    (49,"Durham Business School","UK","https://www.durham.ac.uk/business/study-with-us/masters-programmes/management/"),
    (50,"Sorbonne University","France","https://www.sorbonne-universite.fr/en/education/courses-and-programs/masters"),
    (51,"KU Leuven","Belgium","https://www.kuleuven.be/english/education/programs/master-of-management"),
    (52,"TU Munich","Germany","https://www.tum.de/en/studies/degree-programs/detail/management-master-of-science-msc"),
    (53,"Osaka University","Japan","https://www.osaka-u.ac.jp/en/academics/graduate"),
    (54,"SJTU Antai","China","https://en.acem.sjtu.edu.cn/"),
    (55,"Zhejiang University","China","https://www.intl.zju.edu.cn/en/graduate"),
    (56,"Birmingham Business","UK","https://www.birmingham.ac.uk/postgraduate/courses/taught/business/management.aspx"),
    (57,"Leeds Business School","UK","https://business.leeds.ac.uk/masters/courses/course/120/msc-management"),
    (58,"Universiti Malaya","Malaysia","https://www.fba.um.edu.my/programme-master"),
    (59,"LMU Munich","Germany","https://www.lmu.de/en/study/all-degrees-and-programs/masters-programs/management/"),
    (60,"Nottingham Business","UK","https://www.nottingham.ac.uk/pgstudy/course/taught/management-msc"),
    (61,"HEC Paris","France","https://www.hec.edu/en/master-s-programs/grande-ecole-program-master-in-management"),
    (62,"ESCP Business School","France","https://escp.eu/programmes/master-in-management"),
    (63,"ESSEC Business School","France","https://www.essec.edu/en/programme/masters-programs/master-management/"),
    (64,"IE Business School","Spain","https://www.ie.edu/business-school/master-programs/master-in-management/"),
    (65,"ESADE Business School","Spain","https://www.esade.edu/en/programs/master-management"),
    (66,"Bocconi University","Italy","https://www.unibocconi.eu/wps/wcm/connect/bocconi/sitopubblico_en/navigation+tree/home/programs/master+of+science/management"),
    (67,"University of St Gallen","Switzerland","https://www.unisg.ch/en/studying/master/"),
    (68,"HKUST Business","Hong Kong","https://mba.hkust.edu.hk/"),
    (69,"Maastricht University","Netherlands","https://www.maastrichtuniversity.nl/education/master/master-international-business"),
    (70,"University of Bath","UK","https://www.bath.ac.uk/courses/postgraduate-2026/taught-postgraduate/management/"),
    (71,"Henley Business School","UK","https://www.henley.ac.uk/study/masters/msc-management"),
    (72,"Bayes Business School","UK","https://www.bayes.city.ac.uk/faculties-and-research/schools/school-of-management/masters-courses/msc-management"),
    (73,"Cranfield Management","UK","https://www.cranfield.ac.uk/som/masters-courses/management-and-corporate-sustainability"),
    (74,"University of Strathclyde","UK","https://www.strath.ac.uk/courses/postgraduatetaught/management/"),
    (75,"EDHEC Business School","France","https://master.edhec.edu/programs/master-in-management"),
    (76,"emlyon business school","France","https://em-lyon.com/en/programs/masters-in-management"),
    (77,"Grenoble EM","France","https://www.grenoble-em.com/en/programs/master-in-management"),
    (78,"SKEMA Business School","France","https://www.skema-bs.fr/programs/master-in-management"),
    (79,"Aston Business School","UK","https://www.aston.ac.uk/study/postgraduate/management-msc"),
    (80,"University of Exeter","UK","https://business.exeter.ac.uk/study/postgraduate-taught/courses/msc-management/"),
    (81,"Queen Mary London","UK","https://www.qmul.ac.uk/postgraduate/taught/coursefinder/courses/management-msc/"),
    (82,"Lancaster Management","UK","https://www.lancaster.ac.uk/lums/postgraduate/programmes/management/"),
    (83,"Politecnico di Milano","Italy","https://www.som.polimi.it/en/programs/master-of-science/"),
    (84,"WU Vienna","Austria","https://www.wu.ac.at/en/programs/master-s-programs/"),
    (85,"Trinity College Dublin","Ireland","https://www.tcd.ie/business/postgraduate/masters/msc-management/"),
    (86,"Erasmus Rotterdam","Netherlands","https://www.rsm.nl/master/msc-programmes/"),
    (87,"Ghent University","Belgium","https://www.ugent.be/eb/en/education/master-management.htm"),
    (88,"Copenhagen Business School","Denmark","https://www.cbs.dk/en/study/graduate/msc-in-management-of-creative-business-processes"),
    (89,"University of Helsinki","Finland","https://www.helsinki.fi/en/admissions-and-education/apply-masters-programme"),
    (90,"Korea University Business","South Korea","https://kubs.korea.ac.kr/en/"),
    (91,"Yonsei School of Business","South Korea","https://ysb.yonsei.ac.kr/en/academics"),
    (92,"Duke Fuqua MiM","USA","https://www.fuqua.duke.edu/programs/masters/management-mim"),
    (93,"Ivey Western University","Canada","https://www.ivey.uwo.ca/programs/msc-programs/mim/"),
    (94,"Southampton Business","UK","https://www.southampton.ac.uk/courses/management-masters-msc"),
    (95,"Sheffield Management","UK","https://www.sheffield.ac.uk/postgraduate/taught/courses/2026/management-msc"),
    (96,"St Andrews Management","UK","https://www.st-andrews.ac.uk/subjects/management/management-msc/"),
    (97,"University of Auckland","New Zealand","https://www.auckland.ac.nz/en/study/study-options/find-a-study-option/master-of-management.html"),
    (98,"Georgia Tech Scheller","USA","https://scheller.gatech.edu/degree-programs/ms-programs/ms-management.html"),
    (99,"Purdue Krannert","USA","https://krannert.purdue.edu/programs/masters/ms-management/"),
    (100,"University of Groningen","Netherlands","https://www.rug.nl/masters/international-business-and-management/"),
]

def analyze(name, search_results):
    snippets = ""
    for r in search_results:
        snippets += r.get("title", "") + ": " + r.get("body", "") + "\n"
        
    prompt = f"""You are an academic researcher. Analyze these search results for {name} Master in Management (MiM) program for Autumn/Fall 2026.
Search Snippets:
{snippets}
Return ONLY raw JSON (no markdown):
{{"program_name":"exact program name found or Not Available","status":"OPEN or CLOSED or UNCLEAR","deadline":"exact date or Not Specified","tuition_fees":"amount with currency or Not Specified","scholarships":"names or Not Specified"}}"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3-32b",
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
                    import re
                    match = re.search(r'try again in ([\d\.]+)s', err_msg)
                    wait_time = float(match.group(1)) + 1 if match else 20
                    print(f"    Rate limit hit. Waiting {wait_time:.1f}s...", flush=True)
                    time.sleep(wait_time)
                    continue
                raise Exception(err_msg)
                
            content = data["choices"][0]["message"]["content"].replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
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
        search_query = f"{name} Master in Management admissions deadline tuition fees scholarships 2026"
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

        time.sleep(2)
    print("\n=== COMPLETE ===", flush=True)

if __name__ == "__main__":
    main()
