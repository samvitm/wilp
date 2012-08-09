from django import forms

class SettingsForm(forms.Form):
  access = forms. BooleanField(label = 'Enable access to BITS Coordinators',required = False,help_text='Check this box to allow BITS Coordinators to log into the site.')
  companies = forms. BooleanField(label = 'Allow BITS Coordinators to add/remove companies from their list',required = False,help_text='Check this box to allow BITS Coordinators to add or remove companies from their list. The Manager will be able to change even if this is disabled.')
  data = forms. BooleanField(label = 'Allow BITS Coordinators to enter data ',required = False,help_text='Check this box to allow BITS Coordinators to enter faculty, student and company coordinator details.')
  

class ImportForm(forms.Form):
  type = forms.ChoiceField(choices=(('faculty','Faculty'),('bitscoords','BITS Coordinators'),('companies','Companies & BITS Coords'),('companycoord','Company Coordinators')))
  file = forms.FileField()