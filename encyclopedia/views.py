from django.shortcuts import render,redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


from django.http import Http404

def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        raise Http404("Entry not found")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

# search function logic.
def search(request):
    # taking query. using GET.get
    query =  request.GET.get('q','').strip()

    if not query:
        return redirect('index')

    exact_match = util.get_entry(query)
    if exact_match:
        return redirect('entry',title=query)
    
    # not exact match
    all_entries =util.list_entries()
    results=[e for e in all_entries if query.lower() in e.lower()]

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })

# create new page 

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
    
        if not title or not content:
            return render(request, "encyclopedia/create_page.html", {
                "error": "Title and content cannot be empty",
                "title": title,
                "content": content
            })
    # Check if page already exists

        if util.get_entry(title):
            return render(request, "encyclopedia/create_page.html", {
                "error": "An entry with this title already exists",
                "title": title,
                "content": content
            })
    # Save new entry
        util.save_entry(title, content)

    # Redirect to newly created page
        return redirect('entry', title=title)

  # GET request → show empty form
    return render(request, "encyclopedia/create_page.html")

# ====================================
import random
# Random function.
def random_page(request):
    entries = util.list_entries()
    if not entries:
        # handle empty encyclopedia
        return redirect('index')
    random_title = random.choice(entries)  # pick a random entry
    return redirect('entry', title=random_title)  # redirect to that page
    