from django import forms 

from test_kitchen.models import TestKitchenPost

class TestKitchenPostCreate(forms.ModelForm):

    class Meta:
        model = TestKitchenPost
        fields = ('title', 'post', 'user')
