from http.client import HTTPResponse
from .forms import CreateForm, EditForm
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
    entry_list = util.list_entries()
    if request.method == "POST":
        search = request.POST.get("q")
        if search is not None:
            search = search.lower().strip()
            for entry in entry_list:
                if search == entry.lower():
                    title = entry
                    return redirect("wiki:title", title)
            entry_list = list(filter(lambda x: search in x.lower(), entry_list))
            if entry_list:
                return render(request, "encyclopedia/error_page.html", {"entry_list": entry_list, "search": search})
            return render(request, "encyclopedia/error_page.html", {"errormsg": "Entry doesn't exist", "search": search})
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def error(request):
    return render(request, "encyclopedia/error_page.html")

def create_page(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                errmsg = f'An entry with the title {title} already exists; must be unique!'
                messages.error(request, errmsg)
                return redirect("wiki:error")
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("wiki:title", title = title)
        else:
            return render(request, "encyclopedia/create.html", {"form": form})
    return render(request, "encyclopedia/create.html", {"form": CreateForm()})

def edit_entry(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("wiki:title", title=title)
        content = util.get_entry(title)
        entry = EditForm(initial = {"content": content})
    else:
        contents = util.get_entry(title)
        edit_form = EditForm(initial={"content":contents})
        return render(request, "encyclopedia/update.html", {"form": edit_form, "title": title})
    # return render(request, "encyclopedia/update.html", {"entry": entry})


def entry_page(request, title):
    entry = title
    my_entry = util.get_entry(entry)
    # will probably use the bottom two lines when updating the page
    page_converted = markdowner.convert(my_entry)
    return render(request, "encyclopedia/show_links.html", {"page_converted":page_converted, "entry": entry})

def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:title", args=[entry]))
