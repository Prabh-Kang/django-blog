from django.shortcuts import render, redirect
from django.views.generic import (
	DetailView,
	ListView,
	CreateView,
	UpdateView,
	DeleteView,
	FormView
	)
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from account.models import Account
from .forms import CommentCreationForm
from account.forms import UserRegistrationForm, AccountUpdationForm
from django.contrib import messages
from .models import BlogPost, Comment
from django.http import JsonResponse
import json
from datetime import datetime





# Create your views here.
@login_required(login_url='login')
def homepage(request, *args, **kwargs):
	accounts = Account.objects.all()
	context = {
		'accounts': accounts,
	}
	query = ""
	if request.GET:
		query = request.GET['q']





	return render(request, 'blogapp/home.html', context)

def registerPage(request, *args, **kwargs):
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		messages.success(request, 'Account was created for ' + user.username)
		return redirect('login')

	context = {
		'form': form,
		'url' : 'login',
	}

	return render(request, 'blogapp/register.html', context)

def loginPage(request, *args, **kwargs):

	if request.method == "POST":
		email 		= request.POST.get("email")
		password 	= request.POST.get("password")
		user 		= authenticate(email=email, password=password)
		if user:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, "Email OR Password is not correct")
	context = {
		'url' : 'login',
	}
	return render(request, 'blogapp/login.html', context)

@login_required(login_url='login')
def logoutPage(request, *args, **kwargs):
	logout(request)
	return redirect("login")

@login_required(login_url='login')
def profilePage(request, *args, **kwargs):
	user = request.user
	pic = user.profile_pic.url
	form = AccountUpdationForm(request.POST or None, request.FILES or None, instance=user)

	if form.is_valid():
		form.save()
		return redirect('/')
	context = {
		'form': form,
		'pic': pic,
	}
	return render(request, 'blogapp/profile.html', context)

class BlogHomeView(ListView):
	model 			= BlogPost
	template_name 	= "blogapp/home.html"  #<appName>/<view>_<model>//
	# ordering = ['-date_posted']
	paginate_by 	= 10

	def get_queryset(self):
		query = self.request.GET.get('q', None)
		if query is not None:
			object_list = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(author__username__icontains=query)
				).order_by('-date_posted')
		else:
			object_list = self.model.objects.all().order_by('-date_posted')
		return object_list




class BlogDetailView(DetailView):
	model = BlogPost

	

class BlogCreateView(LoginRequiredMixin, CreateView):
	model = BlogPost
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = BlogPost
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = BlogPost
	success_url = '/'

	def test_func(self):
			post = self.get_object()
			if self.request.user == post.author:
				return True
			return False


class UserBlogListView(DetailView):
	
	model 				= Account
	template_name 		= "blogapp/user_profiles.html"
	paginate_by 		= 10


class MyBlogListView(LoginRequiredMixin, ListView):

	model 				= BlogPost
	template_name 		= "blogapp/my_blog_list.html"
	paginate_by 		= 10

	def get_queryset(self):

		user 			= self.request.user
		object_list 	= self.model.objects.filter(author=user).order_by('-date_posted')
		return object_list



def testpage(request, pk):

	verbal = Comment.objects.all().order_by('-date_posted')
	author = Account.objects.get(username=request.user)
	post = BlogPost.objects.get(pk=pk)

	if request.method == "POST":
		content = request.POST.get('content')
		print(request.POST)
		new_comment = Comment.objects.create(comment=content, author=author, post=post)
		responseObj = {
		'author': new_comment.author.username,
		'content':new_comment.comment,
		'date_posted':str(new_comment.date_posted),
		
		
		}
		new_comment.save()
		print('url is ', new_comment.author.profile_pic.url)
		return JsonResponse(json.dumps(responseObj), safe=False)

	
	context = {
	'post':post,
	'comments':verbal,
	}

	return render(request, 'blogapp/testpage.html', context)



def ajaxcomments(request):
	verbal = Comment.objects.all()
	author = Account.objects.get(pk=1)
	post = BlogPost.objects.get(pk=10)

	if request.method == "POST":
		content = request.POST.get('content')
		print(request.POST)
		new_comment = Comment.objects.create(comment=content, author=author, post=post)
		x = datetime(new_comment.date_posted).strftime("%d %B %Y")


		responseObj = {
		'author': new_comment.author.username,
		'content':new_comment.comment,
		'date_posted':str(x),
		'url':new_comment.author.profile_pic.url,
		
		}
		new_comment.save()
		print('url is', responseObj)
		return JsonResponse(json.dumps(responseObj), safe=False)

	context = {
	'comments':verbal,
	}

	return render(request, 'blogapp/ajaxcomments.html', context)