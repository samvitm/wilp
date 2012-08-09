from django import forms
from wilp.coordinator.models import BitsCoordinator,CompanyCoordinator

class BitsCoordinatorForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(BitsCoordinatorForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'
  class Meta:
    model = BitsCoordinator
    widgets = {
            'password': forms.PasswordInput(),
        }
    exclude = ( 'is_superuser','last_login','date_joined','user_permissions','groups','semester','companies','password','is_staff','username','is_active')
    filter_horizontal = ['companies','semester']


class CompanyCoordinatorForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(CompanyCoordinatorForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      self.fields[field].widget.attrs['class'] = 'text'
  class Meta:
    model = CompanyCoordinator
    exclude = ('author','semester',)
