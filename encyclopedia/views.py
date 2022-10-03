from http.client import HTTPResponse
from django.http import HttpResponseRedirect
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

def update_page(request, title):
    curr_title = title # current title of the page is passed in
    curr_content = util.get_entry(curr_title) # current contents of the page is passed in

    new_title = curr_title # Enter new title in the form in the html
    new_content = curr_content # Enter new content in the form in the html

    #context = {"new_title":new_title, "new_content": new_content}
    return render(request, "encyclopedia/update.html", {"new_content": new_content, "new_title": new_title})


def create_page(request, title = ""):
    context = {"config": "create"}
    previous_title = title
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        submit = request.POST.get("submit")
        hidden = request.POST.get("config")

        if submit is None:
            if "create" in hidden:
                return render(request, "encyclopedia/create.html", context)
            else:
                return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})
        elif not title or not content:
            error(msg= "Must add title and content to create entry")
            return render(request, "encyclopedia/create.html", context)

        action = "updated" if "edit" in hidden else "created"
        messages.success(request, f" Your entry was {action} succesfully!")
        util.save_entry(title=title, content=content)
        return HttpResponseRedirect(reverse("wiki:index"))
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
    return render(request, "encyclopedia/create.html", context)

def entry_page(request, title):
    entry = title
    my_entry = util.get_entry(entry)
    # will probably use the bottom two lines when updating the page
    page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"page_converted":page_converted, "entry": entry})

def random_page(request):
    entries = random.choice(util.list_entries())
    my_entry = util.get_entry(entries)
    random_page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"random_page_converted":random_page_converted, "entries": entries})
