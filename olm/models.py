import uuid

from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

# Names of all ollama models
MODEL_NAMES = (
    (1, 'llama2'),
    (2, 'mistral'),
    (3, 'dolphin-phi'),
    (4, 'phi'),
    (5, 'neural-chat'),
    (6, 'starling'),
    (7, 'codellama'),
    (8, 'llama2-uncensored'),
    (9, 'llama2:13b'),
    (10, 'llama2:7b'),
    (11, 'orca-mini'),
    (12, 'vicuna'),
    (13, 'llava'),
    (14, 'gemma:2b'),
    (15, 'gemma:7b'),
)

EMBEDDING_MODELS = (
    ('net', 'nomic-embed-text'),
)

# Allowed langusages
LANGUAGES = (
    ('nl', 'Nederlands'),
    ('en', 'English'),
)

# Type of utterings
UTR_TYPES = (
    ('q', 'Question'),
    ('r', 'Response'),
    ('d', 'Some nifty type'),
)

class Conversation(models.Model):
    # Unique ID
    # name of llm being used for this Conversation
    llm_used = models.IntegerField(
        choices = MODEL_NAMES,
        default = 1,
        help_text = "Large Language Model used for conversation",
    )
    
    # language of the Conversation
    language = models.CharField(
        max_length = 2,
        choices = LANGUAGES,
        default = 'en',
        help_text = "Language to use for conversation",
    )
    
    # Dat and time the Conversation started
    started = models.DateTimeField(
        null = False,
        blank = False,
        default = datetime.now(),
    )

    class Meta:
        ordering = ['llm_used', 'started']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('conversation-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.llm_used} ({self.language}) @ {self.started}'
    
### Class: Conversation ###
    

class Person(models.Model):
    name = models.CharField(
        max_length = 20,
        help_text = "Name of person",
    )
    
    class Meta:
        ordering = ['name']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('person-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.name}'
    
### class: Person ###

    
class Doc(models.Model):
    title = models.CharField(
        max_length = 255,
        default = '',
        help_text = "Name of the person",
    )

    author = models.CharField(
        max_length = 80,
        default = '',
        help_text = "Author of the person",
    )   
    
    url = models.CharField(
        max_length = 256,
        null = False,
        help_text = "Link to the person",
    )
    
    class Meta:
        ordering = ['title']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('doc-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.author}:   {self.title}'
    
### class: Doc ###
    
    
class DocInstance(models.Model):
    # ID of person having the conversation
    conversation_id = models.ForeignKey(
        'Conversation',
        on_delete = models.RESTRICT,
        null = False,
        help_text = "Conversation id of the DocInstance",
    )
    
    doc_id = models.ForeignKey(
        'Doc',
        on_delete = models.RESTRICT,
        null = False,
        help_text = "Document id of the DocInstance",
    )

    embedding_model = models.CharField(
        max_length = 3,
        choices = EMBEDDING_MODELS,
        null = False,
        help_text = "Embedding model used"
    )

    chunk_size = models.IntegerField(
        default = 200,
        null = False,
        help_text = "Chunksize of embedding model"
    )

    chunk_overlap = models.IntegerField(
        default = 0,
        null = False,
        help_text = "Chunk overlap of embedding model",
    )

    class Meta:
        ordering = ['conversation_id']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('docinstance-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.conversation_id}:   {self.doc_id}'
    
### class: DocInstance ###


class Uttering(models.Model):
    # ID of person having the conversation
    person = models.ForeignKey(
        'Person',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "Person uttering this uttering",
    )
    
    # Date and time of this uttering
    timestamp = models.DateTimeField(
        null = False,
        blank = False,
        default = datetime.now(),
        help_text = 'Date and time of the uttering',
    )
    
    # Type of the Uttering
    type = models.CharField(
        max_length = 2,
        choices = UTR_TYPES,
        default = 'en',
        help_text = "Type of uttering",
    )
    
    # the contents of this uttering
    words = models.TextField(help_text = "Uttered text")
    
    class Meta:
        ordering = ['person', 'timestamp']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('uttering-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.person}:   {self.timestamp}'
    
### class: Uttering ###
