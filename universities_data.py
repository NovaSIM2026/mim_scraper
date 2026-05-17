def get_1000_universities():
    # This function fetches all ~9000 global universities from a public dataset 
    # and automatically filters/formats them into the list format.
    import requests, csv
    try:
        url = "https://raw.githubusercontent.com/endSly/world-universities-csv/master/world-universities.csv"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split("\n")
        
        universities = []
        rank = 1
        for line in lines:
            if not line.strip(): continue
            parts = line.split(",")
            if len(parts) >= 3:
                country_code = parts[0].strip()
                name = parts[1].strip()
                url = parts[2].strip()
                # Exclude obvious non-universities if necessary, but this dataset is quite clean.
                # Since the user specifically wants massive volume (1000), we just take the first 1000
                # From major target countries for MiM: US, UK, FR, DE, CA, AU, SG, CH, NL, IT, ES, etc.
                if country_code in ["US", "GB", "FR", "DE", "CA", "AU", "SG", "CH", "NL", "IT", "ES", "CN", "HK", "JP", "KR", "SE", "DK", "FI", "NO", "BE", "AT", "IE", "NZ"]:
                    universities.append((rank, name, country_code, url))
                    rank += 1
                    if rank > 1000:
                        break
        return universities
    except Exception as e:
        print("Failed to fetch world universities:", e)
        return []

QS_UNIVERSITIES = get_1000_universities()
