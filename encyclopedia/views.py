from django.shortcuts import render
import markdown2
markdowner = markdown2.Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create_page(request):
    pass

def entry_page(request, title):
    entry = title
    my_entry = util.get_entry(entry)
    page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"page_converted":page_converted, "entry": entry})
    # if request.method == 'POST':
    #     current_entries = request.POST.get('TITLE')
    #     my_entry = util.get_entry(current_entries)
    #     return render(request, "encyclopedia/links.html", {"my_entry":my_entry})
    # #return render(request, "encyclopedia/links.html")