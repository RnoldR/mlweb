from django.shortcuts import render
from django.views import generic

from .models import Conversation, Person, Uttering, Doc, DocInstance

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_conversations = Conversation.objects.all().count()
    num_docs = Doc.objects.all().count()
    num_instances = DocInstance.objects.all().count()

    # The 'all()' is implied by default.
    num_persons = Person.objects.count()

    context = {
        'num_persons': num_persons,
        'num_conversations': num_conversations,
        'num_docs': num_docs,
        'num_instances': num_instances,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

### index ###


class DocListView(generic.ListView):
    model = Doc
    """
    context_object_name = 'doc_list'   # your own name for the list as a template variable
    queryset = Doc.objects.all() # Get all documents
    # queryset = Doc.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'docs/doc_list.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        ''' Example function on how to add additional data to the context

        Returns:
            context: dictionary with additional context data
        '''
        # Call the base implementation first to get the context
        context = super(DocListView, self).get_context_data(**kwargs)

        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        
        return context
    
    ### get_context_data ###
    """
### Class: DocListView ###


class DocDetailView(generic.DetailView):
    model = Doc

### Class: DocDetailView ###