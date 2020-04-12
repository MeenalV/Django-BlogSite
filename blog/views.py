from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from blog.forms import BlogFrom
from blog.models import Blog
# Create your views here.


def display_blog(request):
	blogs = Blog.objects.filter(published=True)
	my_blogs=None
	if request.user.is_authenticated:
		my_blogs = Blog.objects.filter(published=True)

	return render(request, 'blog/home.html', {'blogs': blogs, 'my_blogs':  my_blogs})


@login_required()
def blog_write(request):
	if request.user.is_superuser or request.user.is_writer:
		if request.method == 'POST':
			form = BlogFrom(request.POST)
			print(form)
			if form.is_valid():
				BlogFrom.save(form, request.user)
				return redirect('index')
			else:
				return render(request, 'blog/forms.html', {'form': form})
		else:
			form = BlogFrom()
			return render(request, 'blog/forms.html', {'form': form})
	raise PermissionDenied

