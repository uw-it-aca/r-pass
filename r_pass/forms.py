from django import forms

class ServiceForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    hosts = forms.CharField(widget=forms.Textarea, required=False)
    groups = forms.CharField(widget=forms.Textarea)

    access_name = forms.CharField(label="Access name - something like 'ssh' or 'mysql login'")
    access_description = forms.CharField(widget=forms.Textarea, label="How to use this access info", required=False)
    access_user = forms.CharField(required=False)
    access_token = forms.CharField(widget=forms.Textarea, label="This can be a password, ssh key, whatever")
    
