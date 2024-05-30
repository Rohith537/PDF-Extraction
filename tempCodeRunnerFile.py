def extract_director_detail(text):
    director_details = []
    director_patterns = r"\. (.+?) \(DIN: (\d+)\),\s+(.*?)\s+(?:Director|Directors)"
    director_pattern = r"(Mr\.|Mrs\.|Ms\.|Dr.\)\s+([A-Za-z]{2,})"
    din_pattern = r"DIN:\s(\d+)"
    independence_pattern = r"(?i)Independence"
    processed_directors = set()
    director_patterns=re.findall(director_patterns,text);
    director_matches = re.findall(director_pattern, text)
    din_matches = re.findall(din_pattern, text)
    independence_matches = re.findall(independence_pattern, text)
    
    for director_match, din_match, independence_match in zip(director_matches, din_matches, independence_matches):
        director_name = director_match[1]  # Using index 1 to get the name
        din_number = din_match  # No need for index, it's already a single match
        independence_status = "Independent" if independence_match else "Not independent"
        
        if director_name not in processed_directors:
            processed_directors.add(director_name)
            director_details.append({'director': director_name, 'din': din_number, 'independence': independence_status})
        director_details.extend(director_patterns)
    return director_details
