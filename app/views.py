from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Tag, Snippet

def index(request):
    return render(request, 'index.html')

class SnippetListView(LoginRequiredMixin, generic.ListView):
    model = Snippet
    paginate_by = 10

    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user)

class SnippetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Snippet

@login_required
def snippet_raw(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    resp = HttpResponse(snippet.code, content_type='text/plain')
    return resp

@login_required
def snippet_delete(request, pk):
    Snippet.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('app:snippets'))

@login_required
def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    
    snippets = Snippet.objects.filter(
        tags=tag,
        user=request.user
    ).distinct()

    context = {
        'tag': tag,
        'snippets': snippets
    }
    return render(request, 'app/tag_detail.html', context)

@login_required
def tag_delete(request, pk):
    Tag.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('app:tags'))

class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)