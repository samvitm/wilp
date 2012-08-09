from django import forms
from wilp.faculty.models import Faculty,FacultySem

class FacultyForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(FacultyForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'
  class Meta:
    model = Faculty
    widgets = {
            'expertise_area':forms.Textarea,
            'curr_aff':forms.Textarea,
        }

    exclude = ('author')


class FacultySemForm(forms.ModelForm):
  pan_no = forms.TimeField()
  def __init__(self, *args, **kwargs):
    super(FacultySemForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'

  class Meta:
    model = FacultySem
    fields = ('company','programme','course','pan_no')


class FacultySemForm2(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(FacultySemForm2, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'

  class Meta:
    model = FacultySem
    exclude = ('faculty','honorarium_final','semester')
    