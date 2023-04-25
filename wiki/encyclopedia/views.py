from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2


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
    return render(request, "encyclopedia/error.html")
    
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