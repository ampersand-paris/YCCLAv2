from django import forms 

from test_kitchen.models import TestKitchenPost

class TestKitchenPostCreate(forms.ModelForm):

    class Meta:
        model = TestKitchenPost
        fields = ('title', 'post', 'user')

class TestKitchenPostUpdateForm(forms.ModelForm):

    class Meta:
        model = TestKitchenPost
        fields = ('title', 'post', 'user')

    def save(self, commit=True):
        post = super(TestKitchenPostUpdateForm, self).save(commit=False)
        post.title = self.cleaned_data['title']
        post.post = self.cleaned_data['post']
        post.user = self.cleaned_data['user']
        if commit:
            post.save()
        return post