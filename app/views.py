from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Tag, Snippet
from .forms import SnippetForm, TagForm

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

    if request.user != snippet.user:
        return HttpResponse('Unauthorized', status=401)
    
    resp = HttpResponse(snippet.code, content_type='text/plain')
    return resp

@login_required
def snippet_delete(request, pk):
    Snippet.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('app:snippets'))

@login_required
def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    
    if request.user != tag.user:
        return HttpResponse('Unauthorized', status=401)

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
    user = Tag.objects.filter(pk=pk).user
    if request.user != user:
        return HttpResponse('Unauthorized', status=401)

    Tag.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('app:tags'))

class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 10

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

@login_required
def snippet_add(request):
    form = SnippetForm(request.POST or None)
    user = request.user
    form.fields['tags'].queryset = Tag.objects.filter(user=user)

    if form.is_valid():
        snip = form.save(commit=False)
        snip.user = request.user
        snip.save()
    
        for tag in form.cleaned_data['tags']:
            snip.tags.add(tag)

        snip.save()
        return HttpResponseRedirect(reverse('app:snippets'))

    return render(request, 'app/snippet_form.html', {'form': form})

@login_required
def snippet_edit(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.user != snippet.user:
        return HttpResponse('Unauthorized', status=401)

    form = SnippetForm(request.POST or None)
    user = request.user
    form.fields['tags'].queryset = Tag.objects.filter(user=user)

    if form.is_valid():
        print(form.cleaned_data)
        
        # update the old snip with form data
        
        return HttpResponseRedirect(reverse('app:snippets'))

    return render(request, 'app/snippet_edit_form.html', {'form': form, 'pk': pk, 'snippet': snippet})

@login_required
def tag_add(request):
    form = TagForm(request.POST or None)

    if form.is_valid():
        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()
        return HttpResponseRedirect(reverse('app:tags'))

    return render(request, 'app/tag_form.html', {'form': form})