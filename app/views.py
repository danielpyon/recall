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
    paginate_by = 18

    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user).order_by('-pub_date')

class SnippetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Snippet
    
    def get(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return HttpResponse('Unauthorized', status=401)

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('app:index'))

        return super(SnippetDetailView, self).get(request, *args, **kwargs)

class SnippetSearchListView(LoginRequiredMixin, generic.ListView):
    model = Snippet
    paginate_by = 18
    
    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user, title__icontains=self.kwargs['query']).order_by('-pub_date')

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
    user = Tag.objects.get(pk=pk).user
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
        # update the old snip with form data
        snippet.code = form.cleaned_data['code']
        snippet.language = form.cleaned_data['language']
        snippet.title = form.cleaned_data['title']
        snippet.starred = form.cleaned_data['starred']
        snippet.description = form.cleaned_data['description']
        
        snippet.tags.clear()

        for tag in form.cleaned_data['tags']:
            snippet.tags.add(tag)
        
        snippet.save()
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

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.user != tag.user:
        return HttpResponse('Unauthorized', status=401)

    form = TagForm(request.POST or None)
    user = request.user

    if form.is_valid():
        tag.tag_type = form.cleaned_data['tag_type']
        tag.save()
        return HttpResponseRedirect(reverse('app:tags'))

    return render(request, 'app/tag_edit_form.html', {'form': form, 'pk': pk, 'tag': tag})


@login_required
def settings_view(request):
    if request.method == 'POST':
        # delete account
        request.user.delete()
        return HttpResponseRedirect(reverse('logout'))
    else:
        return render(request, 'app/settings.html', { 'user': request.user })