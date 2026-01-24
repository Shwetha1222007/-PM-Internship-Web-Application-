def ai_filter_candidates(candidates_list, requirements):
    """
    AI Filtering Logic:
    1. Calculate scores based on Skills match, CGPA, and Experience.
    2. Rural candidates get a priority weight.
    3. Ensure at least 20% representation for Rural candidates in the result.
    """
    scored = []
    
    for cand in candidates_list:
        score = 0
        
        # Skill Match Score (assuming comma separated)
        cand_skills = set(s.strip().lower() for s in cand.get('skills', '').split(','))
        req_skills = set(s.strip().lower() for s in requirements.get('skills', '').split(','))
        match_count = len(cand_skills.intersection(req_skills))
        score += match_count * 15
        
        # CGPA Score (Max 10)
        cgpa = cand.get('cgpa', 0)
        score += (cgpa * 5) # Up to 50 points
        
        # Experience weight
        if cand.get('experience') and len(cand.get('experience')) > 10:
            score += 10
            
        # Rural Priority Weight
        is_rural = cand.get('rural') == 'Yes' or cand.get('rural_urban') == 'Rural'
        if is_rural:
            score += 20
            
        scored.append({'data': cand, 'score': score, 'is_rural': is_rural})

    # Sort by score
    scored_sorted = sorted(scored, key=lambda x: x['score'], reverse=True)
    
    # Selection algorithm with quota logic
    shortlisted = []
    rural_count = 0
    quota_needed = 2 if len(candidates_list) >= 10 else 1
    
    # First pass: take top scores naturally
    preliminary = scored_sorted[:max(quota_needed, 5)]
    for item in preliminary:
        shortlisted.append(item['data'])
        if item['is_rural']:
            rural_count += 1
            
    # Second pass: ensure rural quota if not met
    if rural_count < quota_needed:
        remaining_rural = [x for x in scored_sorted[len(shortlisted):] if x['is_rural']]
        for i in range(min(len(remaining_rural), quota_needed - rural_count)):
            shortlisted.append(remaining_rural[i]['data'])
            
    return shortlisted
