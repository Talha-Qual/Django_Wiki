import re
from distutils.log import error
from django.shortcuts import render, redirect
import random
from django.urls import reverse
from django.contrib import messages
import markdown2
markdowner = markdown2.Markdown()

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# def save(request, **kwargs):
#     title = kwargs.get("title", "")
#     content = kwargs.get("content", "")
#     if content and title:
#         title = title.strip()
#         entry = util.save_entry(title.strip(), str(content).strip())
#         return redirect(reverse(index), title=title)

def create_page(request, title = ""):
    previous_title = title
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submit = request.POST.get("submit")
        hidden = request.POST.get("config")

        action = "updated" if "edit" in hidden else "created"
        messages.success(request, f" Your entry was {action} succesfully!")
        util.save_entry(title=title, content=content)
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries()} )
    else:
        context = {"config": "create"}
        if title:
            entry = util.get_entry(title)
            if not entry or entry is None:
                return error(msg="Page Not Found")
            context["entry"] = entry
            context["config"] = "edit"

        context.update(
            {
                "title": title, "unavailable_entry": util.list_entries()
            }
        )
    return render(request, "encyclopedia/create_edit.html", context)

def entry_page(request, title):
    entry = title
    my_entry = util.get_entry(entry)
    page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"page_converted":page_converted, "entry": entry})

def random_page(request):
    entries = random.choice(util.list_entries())
    my_entry = util.get_entry(entries)
    random_page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"random_page_converted":random_page_converted, "entries": entries})
