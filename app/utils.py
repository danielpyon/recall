from .models import Tag, Snippet

def language_counts():
    counts = dict()
    for s in Snippet.objects.values_list('language'):
        lang = s[0]
        if lang in counts:
            counts[lang] += 1
        else:
            counts[lang] = 1
    return counts