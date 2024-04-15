from django.contrib import admin
from .models import Conversation, Person, Uttering, Doc, DocInstance

# Register your models here.

# admin.site.register(Person)
# admin.site.register(Conversation)
# admin.site.register(Uttering)
# admin.site.register(Doc)
# admin.site.register(DocInstance)

# define the admin class
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('llm_used', 'language', 'started')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Uttering)
class UtteringAdmin(admin.ModelAdmin):
    list_display = ('person', 'timestamp', 'type')

@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'url')

@admin.register(DocInstance)
class DocInstance(admin.ModelAdmin):
    list_display = ('embedding_model', 'chunk_size', 'chunk_overlap')
    