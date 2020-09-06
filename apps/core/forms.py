from django import forms
from django.core.exceptions import ValidationError


class CustomForm(forms.Form):
    error_css_class = 'is-invalid'

    def clean(self):
        cleaned_data = super(CustomForm, self).clean()

        if 'password1' in self.changed_data and 'password2' in self.changed_data:
            if cleaned_data.get('password1') == cleaned_data.get('password2'):
                return cleaned_data
            else:
                self.add_error('password1', ValidationError("As senhas não coicidem!"))
                self.add_error('password2', ValidationError("As senhas não coicidem!"))

        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' is-invalid'

        return cleaned_data


class CustomModelForm(forms.ModelForm):
    error_css_class = 'is-invalid'

    def clean(self):
        cleaned_data = super(CustomModelForm, self).clean()

        if 'password1' in self.changed_data and 'password2' in self.changed_data:
            if cleaned_data.get('password1') == cleaned_data.get('password2'):
                return cleaned_data
            else:
                self.add_error('password1', ValidationError("As senhas não coicidem!"))
                self.add_error('password2', ValidationError("As senhas não coicidem!"))

        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' is-invalid'

        return cleaned_data
