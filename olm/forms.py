from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TrainLLMForm(forms.Form):
    # renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    # user_name = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True
    # )

    llm_name = forms.CharField(
        max_length = 20,
        min_length = 1,
        strip = True,
        help_text = 'Enter name of the trained LLM',
    )

    def clean_llm_name(self):
        name =  self.cleaned_data['llm_name']

        if name == 'hi':
            raise ValidationError('hi not allowed')

        return name
    
