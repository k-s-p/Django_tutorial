from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# Create your views here.
def index(request):
    #return HttpResponse("Hello World! このページは投稿のインデックスです")
    posts = Post.objects.order_by('-published')
    return render(request, 'posts/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_detail.html',{'post':post})
