def ai_filter_candidates(candidates_list, requirements):
    """
    AI Filtering Logic:
    1. Calculate scores based on Skills match, CGPA, and Experience.
    2. Rural candidates get a priority weight.
    3. Social Category candidates (SC, ST, OBC, MBC) get a priority weight.
    4. Return ALL candidates sorted by score (not just top 5)
    """
    scored = []
    
    for cand in candidates_list:
        score = 0
        
        # Handle potential None values for strings
        skills_raw = cand.get('skills') or ''
        social_cat_raw = cand.get('social_category') or ''
        rural_raw = cand.get('rural') or ''
        rural_urban_raw = cand.get('rural_urban') or ''
        experience_raw = cand.get('experience') or ''
        
        # Skill Match Score (assuming comma separated)
        cand_skills = set(s.strip().lower() for s in skills_raw.split(','))
        req_skills = set(s.strip().lower() for s in requirements.get('skills', '').split(','))
        match_count = len(cand_skills.intersection(req_skills))
        score += match_count * 15
        
        # CGPA Score (Max 10)
        cgpa = cand.get('cgpa') or 0.0
        score += (float(cgpa) * 5) # Up to 50 points
        
        # Experience weight
        if len(experience_raw) > 10:
            score += 10
            
        # Rural Priority Weight
        is_rural = rural_raw == 'Yes' or rural_urban_raw == 'Rural'
        if is_rural:
            score += 20
        
        # Social Category Priority Weight
        # "SC", "ST", "OBC", "MBC", "BC"
        social_category = social_cat_raw.upper().replace('.', '')
        is_reserved = social_category in ['SC', 'ST', 'OBC', 'MBC', 'BC', 'MBC/DNC']
        if is_reserved:
            score += 20
            
        scored.append({'data': cand, 'score': score, 'is_rural': is_rural, 'is_reserved': is_reserved})

    # Sort by score (highest first)
    scored_sorted = sorted(scored, key=lambda x: x['score'], reverse=True)
    
    # Return ALL candidates sorted by score
    return scored_sorted


def get_top_candidates(all_candidates, limit=5):
    """Get top N candidates from the sorted list"""
    return all_candidates[:limit]
