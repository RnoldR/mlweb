from django.shortcuts import render
from django.views import generic

from .models import LLM, TrainedLLM, Doc, Person, Statement, Conversation

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_llms = LLM.objects.all().count()
    num_docs = Doc.objects.all().count()
    num_instances = TrainedLLM.objects.all().count()
    num_persons = Person.objects.count()
    num_conversations = Conversation.objects.all().count()
    num_statements = Statement.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_llms': num_llms,
        'num_persons': num_persons,
        'num_conversations': num_conversations,
        'num_docs': num_docs,
        'num_instances': num_instances,
        'num_statements': num_statements,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context = context)

### index ###


class LLMListView(generic.ListView):
    model = LLM

### Class: LLMListView ###


class LLMDetailView(generic.ListView):
    model = LLM

### Class: LLMDetailView ###


class DocListView(generic.ListView):
    model = Doc

### Class: DocListView ###


class DocDetailView(generic.DetailView):
    model = Doc

### Class: DocDetailView ###


class TrainedLLMListView(generic.ListView):
    model = TrainedLLM

### Class: LLMListView ###


class TrainedLLMDetailView(generic.ListView):
    model = TrainedLLM

### Class: LLMDetailView ###


class ConversationListView(generic.ListView):
    model = Conversation

### Class: ConversationListView ###


class ConversationDetailView(generic.DetailView):
    model = Conversation

### Class: ConversationDetailView ###


class PersonListView(generic.ListView):
    model = Person

### Class: PersonListView ###


class PersonDetailView(generic.DetailView):
    model = Person

### Class: PersonDetailView ###

class StatementListView(generic.ListView):
    model = Statement

### Class: StatementListView ###


class StatementDetailView(generic.DetailView):
    model = Statement

### Class: StatementDetailView ###
