from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title):
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    not_found = True
    return render(request, "encyclopedia/error.html", {
        "not_found": not_found
    })
    
def search(request):
    query = request.GET.get('q')
    if query:
        if util.get_entry(query):
            return HttpResponseRedirect(f"wiki/{query}")
        
        # if search field is not empty but there is no such page, find pages for which query is a substring
        filenames = util.list_entries()
        found = [filename for filename in filenames if filename.lower().find(query.lower()) != -1]
        return render(request, "encyclopedia/search.html", {
            "found": found
        })
    
    # if user submitted an empty search field
    return HttpResponseRedirect(reverse('index'))

def new(request):
    class NewEntryForm(forms.Form):
        title = forms.CharField(label="Title")
        text = forms.CharField(widget=forms.Textarea, label="Text")
    
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title in util.list_entries():
                exists = True
                return render(request, "encyclopedia/error.html", {
                    "exists": exists
                })
            with open(f"entries/{title}.md", "w") as f:
                f.write(text)
            return HttpResponseRedirect(reverse('new'))

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })