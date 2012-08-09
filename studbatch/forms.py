from django import forms
from wilp.studbatch.models import StudentBatch

class StudbatchForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(StudbatchForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'
  class Meta:
    model = StudentBatch
  