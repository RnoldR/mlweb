from django.contrib import admin
from .models import LLM, TrainedLLM, Doc, Conversation, Person, Statement

# Register your models here.

# admin.site.register(Person)
# admin.site.register(Conversation)
# admin.site.register(Uttering)
# admin.site.register(Doc)
# admin.site.register(DocInstance)

# define the admin class
@admin.register(LLM)
class LLMAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(TrainedLLM)
class TrainedLLMAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc', 'embedding_model', 'chunk_size', 'chunk_overlap')

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'language')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('person_1', 'person_2', 'language', 'timestamp')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'trained_llm']

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('person', 'conversation', 'timestamp', 'type')
