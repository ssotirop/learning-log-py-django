from django.shortcuts import render, get_object_or_404

# We import the class HttpResponseRedirect, which we will
# use to redirect the reader back to the topics page after
# they submit their topic.
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, DeleteEntryForm, DeleteTopicForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

# Make sure the user associated with a topic matches the
# currently logged-in user
def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

# @login_required is a decorator.
# A decorator is a directive placed just before a function
# definition that Python applies to the function before it
# runs to alter how the function code behaves.
# Here we restrict access to certain pages to logged-in users
@login_required
def topics(request):
    """Show all topics."""

    # Topic.objects.filter(owner=request.user) tells Django to retrieve
    # only the Topic objects from the database whose owner attribute
    # matches the current user.
    # Old code fragment: topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    #topic = Topic.objects.get(id=topic_id)
    topic = get_object_or_404(Topic, id=topic_id)

    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request)

    # Notice: the minus sign in front of date_added sorts the
    # results in reverse order, which will display the most
    # recent entries first.
    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            # Make sure that a new topic can be added by
            # associating new topics with a particular user
            # NOTE: We have access to the current user through
            # the request object, which is used to associate any
            # new topic with the current user
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            # The reverse() function determines the URL from a named
            # URL pattern, meaning that Django will generate the URL when
            # the page is requested.
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id = topic_id)

    # Make sure we do not add a new entry to a topic that does not
    # belong to the current user.
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    # The edit_entry pages have URLs in the form:
    #   http://localhost:8000/edit_entry/entry_id/,
    #       where the entry_id is a number
    # Make sure that no one can use the URL to gain access
    # to someone else’s entries.
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance = entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # The delete_entry pages have URLs in the form:
    #   http://localhost:8000/delete_entry/entry_id/,
    #       where the entry_id is a number
    # Make sure that no one can use the URL to gain access and
    # delete someone else’s entries.
    check_topic_owner(topic, request)

    entry_to_delete = get_object_or_404(Entry, id=entry_id)
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = DeleteEntryForm(instance=entry_to_delete)
    else:
        # POST data submitted; process data.
        form = DeleteEntryForm(instance=entry_to_delete, data=request.POST)
        if form.is_valid():
            entry_to_delete.delete()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/delete_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """Delete an existing topic."""
    topic = Topic.objects.get(id=topic_id)

    # Make sure that no one can delete someone else’s topics.
    check_topic_owner(topic, request)

    topic_to_delete = get_object_or_404(Topic, id=topic_id)
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = DeleteTopicForm(instance=topic_to_delete)
    else:
        # POST data submitted; process data.
        form = DeleteTopicForm(instance=topic_to_delete, data=request.POST)
        if form.is_valid():
            topic_to_delete.delete()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    #context = {'form': form}
    #context = {'topics': topics}
    context = {'topic': topic, 'form': form}
    #context = {'topics': topics, 'form': form}
    return render(request, 'learning_logs/delete_topic.html', context)
