from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Tag, Snippet
from .forms import SnippetForm, TagForm
from .utils import language_counts, language_types

import json


def index(request):
    if request.user.is_authenticated:
        context = dict()

        counts = []
        for k, v in language_counts(request.user).items():
            counts.append([k, v])
        if len(counts) >= 1:
            context['counts'] = json.dumps(counts)

        most_recent = Snippet.objects.filter(user=request.user).order_by('-pub_date')[:6]
        if len(most_recent) >= 1:
            context['recent'] = most_recent
        
        most_recent_starred = Snippet.objects.filter(user=request.user, starred=True).order_by('-pub_date')[:6]
        if len(most_recent_starred) >= 1:
            context['starred'] = most_recent_starred

        return render(request, 'index.html', context)
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

class SnippetAdvancedSearchListView(LoginRequiredMixin, generic.ListView):
    model = Snippet
    paginate_by = 18

    def get_or_none(self, key):
        try:
            return self.request.GET[key]
        except:
            return None

    def get_queryset(self):
        query = ''
        if 'query' in self.kwargs:
            query = self.kwargs['query']

        start = self.get_or_none('from')
        end = self.get_or_none('to')
        sortby = self.get_or_none('sortby')
        starred = self.get_or_none('starred')
        languages = self.get_or_none('languages')

        args = {
            'user': self.request.user,
            'title__icontains': query,
        }
        if start is not None and end is not None:
            args['pub_date__range'] = [str(start), str(end)]
        if starred is not None:
            if starred == 'true':
                args['starred'] = True
            else:
                args['starred'] = False
        if languages is not None:
            args['language__in'] = languages.split(',')

        if sortby is not None:
            return Snippet.objects.filter(**args).order_by('-pub_date' if sortby == 'date' else 'title')
        else:
            return Snippet.objects.filter(**args)

@login_required
def languages(request):
    data = {
        'languages': language_types(request.user)
    }
    return JsonResponse(data)

class SnippetSearchListView(LoginRequiredMixin, generic.ListView):
    model = Snippet
    paginate_by = 18
    
    # NOTE: this uses the "snippet_list" template
    
    def get_queryset(self):
        if 'query' in self.kwargs:
            return Snippet.objects.filter(user=self.request.user, title__icontains=self.kwargs['query']).order_by('-pub_date')
        return Snippet.objects.filter(user=self.request.user)

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

    paginator = Paginator(snippets, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'snippets': snippets,
        'page_obj': page_obj
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
    paginate_by = 18

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('tag_type') # alphabetical

class TagSearchListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 18

    # NOTE: this uses the "tag_list" template

    def get_queryset(self):
        if 'query' in self.kwargs:
            return Tag.objects.filter(user=self.request.user, tag_type__icontains=self.kwargs['query']).order_by('tag_type')
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

    context = {
        'form': form,
        'pk': pk,
        'snippet': snippet,
        #'tags': json.dumps(list(map(lambda x: x.tag_type, snippet.tags.all()))),
        'language': json.dumps(snippet.language),
        'code': json.dumps(snippet.code),
    }
    return render(request, 'app/snippet_edit_form.html', context)

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