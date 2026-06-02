import collections

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


def extract_skills_from_text(text, rake_instance, skill_search_instance, skill_entities, skill_normalizer):
    if text:
        print('extracting skills from ad text')
        text_keywords = rake_instance.apply(text)
        # print('text_keywords:')
        # print(text_keywords)
        skills_normalized = []
        for keyword in text_keywords:
            # if keyword[1] >= 1.5:
            # skill_search_instance is rake_instance
            if 'cleaning procedures' not in keyword[0]:
                skill_found = normalize_raw_skill(keyword[0].lower(), skill_search_instance, skill_entities,
                                                  skill_normalizer)
                if skill_found:
                    skills_normalized.append(skill_found)
            if skills_normalized:
                frequency_order_count = collections.Counter(skills_normalized)
                frequency_ordered_skills = sorted(skills_normalized, key=lambda x: -frequency_order_count[x])
                deduped_normalized_skills = list(set(frequency_ordered_skills))
                return deduped_normalized_skills
            else:
                return None
    else:
        return None


def extract_hard_skills_from_text(text, rake_instance, hard_skill_search):
    hard_skills = []
    if text:
        print('extracting hard skills from ad text')
        text_keywords = rake_instance.apply(text)
        for keyword in text_keywords:
            # if keyword[1] >= 1.5:
            # skill_search_instance is rake_instance
            if 'cleaning procedures' not in keyword[0]:
                skills_found = hard_skill_search.search(keyword[0].lower(), 0.92)
                if skills_found:
                    hard_skills.append(skills_found[0])
                else:
                    if '/' in keyword[0]:
                        _skills_found = hard_skill_search.search(keyword[0].lower(), 0.92)
                        if _skills_found:
                            hard_skills.append(_skills_found[0])
                        else:
                            keyword_split = keyword[0].split('/')
                            for __keyword in keyword_split:
                                __skills_found = hard_skill_search.search(__keyword.lower(), 0.92)
                                if __skills_found:
                                    hard_skills.append(__skills_found[0])
        text_split = text.strip('').replace('\n', ' ').replace('\n\n', ' ').replace('/', ' ').split(' ')
        for word in text_split:
            skills_found = hard_skill_search.search(word.lower(), 0.92)
            if skills_found:
                if skills_found[0].lower() not in hard_skills and skills_found[0].lower() not in stopwords:
                    hard_skills.append(skills_found[0])
            else:
                if '(' in word or ')' in word:
                    parsed_keyword = word.replace('(', '').replace(')', '')
                    _skills_found = hard_skill_search.search(parsed_keyword.lower(), 0.92)
                    if _skills_found:
                        if _skills_found[0].lower() not in hard_skills and _skills_found[0].lower() not in stopwords:
                            hard_skills.append(_skills_found[0])
    return hard_skills


def find_closest_representation_of_raw_skill(skill, hard_skill_search_instance):
    skills = hard_skill_search_instance.search(skill.lower(), 0.92)
    skill = None
    if skills:
        if len(skills) > 1:
            skill = skills[0]
    return skill


def normalize_raw_skill(skill, skill_search_instance, skill_entities, skill_normalizer):
    if skill:
        skills_found = skill_search_instance.search(skill, 0.92)
    else:
        skills_found = None

    if skills_found:
        if len(skills_found) < 2:
            # print('skill found:')
            # print(skills_found)
            skill = skills_found[0]
            skill_index = skill_entities.index(skill)
            skill_normalized = skill_normalizer[skill_index]
            return skill_normalized
        else:
            return None
    else:
        return None


def find_normalized_skill_type(skill, skill_categories, skill_cat_types):
    if skill in skill_categories:
        skill_cat_index = skill_categories.index(skill)
        skill_type = skill_cat_types[skill_cat_index]
        skill_and_skill_type = (skill, skill_type)
        # print(skill_and_skill_type)
        return skill_and_skill_type
    else:
        return None
