from django import forms
from blog.models import Category, Blog

# table for blogs : 1. blog id , writer id, writer username , title of blog, content of blog ,
# topic related to , date of writing
# date of uploading , date of deleting , date of content updating , active/inactive
#  2. interaction id , blog id , interaction type , writer/reader id, date of interaction


class BlogFrom(forms.Form):
    title = forms.CharField(max_length=100, required=True,
                            widget=forms.TextInput(
                                attrs=({'class': 'form-control',
                                        'placeholder': 'Enter the Title for your Blog'})))
    # category = forms.ChoiceField(choices=[(category.id, category.name)for category in Category.objects.all()],
    #                              required=True,
    #                              widget=forms.Select(attrs={'class': 'form-control',
    #                                                         'placeholder': 'Let''s start writing!!!'}))
    category = forms.ChoiceField(choices=[(category.id, category.name)for category in Category.objects.all()],
                                 required=False,
                                 widget=forms.Select(attrs={'class': 'form-control',
                                                            'placeholder': 'Let''s start writing!!!'}))
    content = forms.CharField(widget=forms.Textarea(attrs=({'class': 'form-control',
                                                            'placeholder': 'Let''s start writing!!!'})), required=True)
    # blog_category = Category.objects.all()
    # blog_category_choices = [(category.id, category.name) for category in blog_category]

    # def __init__(self, *args, **kwargs):
    #     super(BlogFrom, self).__init__(*args, **kwargs)
    #     blog_category = Category.objects.all()
    #     blog_category_choices = [(category.id, category.name) for category in blog_category]
    #     blog_category_choices.insert(0, (u"", u"Choose blog category"))
    #     self.fields['category'] = forms.ChoiceField(choices=blog_category_choices,
    #                                                 required=True,
    #                                                 widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, user):
        data = self.cleaned_data
        blog = Blog(
            title=data['title'],
            category_id=data['category'],
            content=data['content'],
            by=user
        )
        blog.save()
        return blog
