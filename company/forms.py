from django import forms
from semester.models import Semester
from wilp.company.models import Company
from wilp.coordinator.models import CoordManaged

class CompanyForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
      super(CompanyForm, self).__init__(*args, **kwargs)
      self.fields['companies'].help_text = ''
      self.fields['companies'].widget.attrs['class'] = 'multiselect'
      self.fields['companies'].widget.attrs['style'] = 'width:700px;min-height:300px'
      self.fields['semester'].queryset = Semester.objects.filter(current = True)

  class Meta:
    model = CoordManaged
    exclude = ('coord',)
  #company = forms.ModelMultipleChoiceField(queryset=Company.objects.all())
  