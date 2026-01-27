def ai_filter_candidates(candidates_list, requirements):
    """
    AI Filtering Logic:
    1. Calculate scores based on Skills match, CGPA, and Experience.
    2. Rural candidates get a priority weight.
    3. Social Category candidates (SC, ST, OBC, MBC) get a priority weight.
    4. Select top 5 candidates.
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
        
        # Social Category Priority Weight
        # "SC", "ST", "OBC", "MBC", "BC"
        social_category = cand.get('social_category', '').upper().replace('.', '')
        is_reserved = social_category in ['SC', 'ST', 'OBC', 'MBC', 'BC', 'MBC/DNC']
        if is_reserved:
            score += 20
            
        scored.append({'data': cand, 'score': score, 'is_rural': is_rural, 'is_reserved': is_reserved})

    # Sort by score
    scored_sorted = sorted(scored, key=lambda x: x['score'], reverse=True)
    
    # Selection algorithm: Select Top 5
    # Since we added weights for Rural and Social Category, they will naturally bubble up.
    # We strictly limit to 5 as per "5 offers" constraint.
    
    offer_limit = 5
    selected_entries = scored_sorted[:offer_limit]
    
    # Return the full structure so we can show scores in UI
    return selected_entries
