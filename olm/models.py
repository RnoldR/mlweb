import uuid

from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

# Names of all ollama models
MODEL_NAMES = (
    ('Llama2', 'llama2'),
    ('Mistral', 'mistral'),
    ('Dolphin Phi', 'dolphin-phi'),
    ('Phi', 'phi'),
    ('Neural Chat', 'neural-chat'),
    ('Starling', 'starling'),
    ('Code Llama', 'codellama'),
    ('Llama2: uncensored', 'llama2-uncensored'),
    ('Llama: 13GB', 'llama2:13b'),
    ('Llama2: 7GB', 'llama2:7b'),
    ('Orca Mini', 'orca-mini'),
    ('Vicuna', 'vicuna'),
    ('Llava', 'llava'),
    ('Gemma: 2GB', 'gemma:2b'),
    ('Gemma: 7GB', 'gemma:7b'),
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
    ('Question', 'Question'),
    ('Response', 'Response'),
    ('Other', 'Some nifty type'),
)


class LLM(models.Model):
    name = models.CharField(
        max_length = 80,
        choices = MODEL_NAMES,
        default = 'Llama2',
        help_text = "Name of the Large Language Model",
    )


    class Meta:
        ordering = ['name']

    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('llm-detail-view', args=[str(self.id)])
    

    def __str__(self):
        return f'LLM: {self.name}'
    
### class: LLM ###


class TrainedLLM(models.Model):
    llm = models.ForeignKey(
        'LLM',
        on_delete = models.RESTRICT,
        null = False,
        help_text = "LLM used for the trained mLLM",
    )
    
   # ID of person having the conversation
    doc = models.ForeignKey(
        'Doc',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "Person uttering this statement",
    )
    
    name = models.CharField(
        max_length = 80,
        null = False,
        help_text = "Name of the trained model",
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
        ordering = ['name']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('trainedllm-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'Trained LLM: {self.name}'
    
### Class: TrainedLLM ###

    
class Doc(models.Model):
    title = models.CharField(
        max_length = 255,
        default = '',
        help_text = "Name of the document",
    )

    author = models.CharField(
        max_length = 80,
        default = '',
        help_text = "Author of the document",
    )   
    
    # language of the Conversation
    language = models.CharField(
        max_length = 2,
        choices = LANGUAGES,
        default = 'en',
        help_text = "Language of the document",
    )
    
    url = models.CharField(
        max_length = 256,
        null = False,
        help_text = "Link to the document",
    )
    
    class Meta:
        ordering = ['title']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('doc-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'Doc: {self.author}: {self.title}'
    
### class: Doc ###
    
    
class Person(models.Model):
    trained_llm = models.ForeignKey(
        'TrainedLLM',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "LLM trained on docs",
    )

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


class Conversation(models.Model):
   # ID of person having the conversation
    person_1 = models.ForeignKey(
        'Person',
        related_name = 'Conversator_1',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "First person in the conversation",
    )
    
   # ID of person having the conversation
    person_2 = models.ForeignKey(
        'Person',
        related_name = 'Conversator_2',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "Second person in the conversation",
    )
    
    # language of the Conversation
    language = models.CharField(
        max_length = 2,
        choices = LANGUAGES,
        default = 'en',
        help_text = "Language to use for conversation",
    )
    
    # Date and time the Conversation started
    timestamp = models.DateTimeField(
        null = False,
        blank = False,
        default = datetime.now(),
    )

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""

        return reverse('conversation-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.timestamp}: {self.llm}'
    
### class: Conversation ###


class Statement(models.Model):
    # ID of the conversation
    conversation = models.ForeignKey(
        'Conversation',
        on_delete = models.RESTRICT,
        null = False,
        help_text = "Conversation id of the statement",
    )
    
   # ID of person having the conversation
    person = models.ForeignKey(
        'Person',
        on_delete = models.RESTRICT,
        null = True,
        help_text = "Person uttering this statement",
    )
    
    # Date and time of this uttering
    timestamp = models.DateTimeField(
        null = False,
        blank = False,
        default = datetime.now(),
        help_text = 'Date and time when the statement was made',
    )
    
    # Type of the Uttering
    type = models.CharField(
        max_length = 10,
        choices = UTR_TYPES,
        default = 'en',
        help_text = "Type of uttering",
    )
    
    # the contents of this uttering
    words = models.TextField(help_text = "Uttered text")
    
    class Meta:
        ordering = ['person', 'conversation', 'timestamp']


    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('statement-detail-view', args=[str(self.id)])


    def __str__(self):
        return f'{self.person}: {self.timestamp}'
    
### class: Statement ###
