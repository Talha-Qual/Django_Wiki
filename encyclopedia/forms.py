from django import forms

class CreateForm(forms.Form):
  title = forms.CharField(label="Title")
  content = forms.CharField(label = "Contents", widget=forms.Textarea)

class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Contents", widget=forms.Textarea)

    def set_values(self, title, content):
      self.entry_title = title
      self.entry_content = content