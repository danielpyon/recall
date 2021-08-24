from .models import Tag, Snippet

def language_counts(user):
    counts = dict()
    for s in Snippet.objects.filter(user=user).values_list('language'):
        lang = s[0]
        if lang in counts:
            counts[lang] += 1
        else:
            counts[lang] = 1
    return counts

def language_types(user):
    return list(map(lambda x: x[0], list(set(Snippet.objects.filter(user=user).values_list('language')))))