from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from random import random

def upload_location(instance, filename):
	file_path = f"blogapp/{instance.author.id}/{instance.title}-{filename}"
	return file_path

class BlogPost(models.Model):

	title 				= models.CharField(max_length=100, null=False, blank=False)
	content				= models.TextField(max_length=5000, null=False, blank=False)
	date_posted			= models.DateTimeField(auto_now_add=True, verbose_name='date posted')
	date_updated		= models.DateTimeField(auto_now=True, verbose_name='date updated')
	image				= models.ImageField(upload_to=upload_location, default='default-prof-pic.jpg' ,null=True, blank=True)
	author				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 				= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail-view', kwargs={'pk':self.pk})


@receiver(pre_save, sender=BlogPost)
def confirm_sluf_field(sender, instance, *args, **kwargs):
	if not instance.slug:
		randstr = str(random()*1000000)
		instance.slug = slugify(instance.author.username + '-' + instance.title + '-' + randstr)
		

@receiver(post_delete, sender=BlogPost)
def upon_deletion(sender, instance, **kwargs):
	instance.image.delete(False)

class Comment(models.Model):

	post 				= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	author				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	comment 			= models.TextField(max_length=500, null=False, blank=False)
	date_posted 		= models.DateTimeField(auto_now_add=True, verbose_name='date posted')

	def __str__(self):
		return self.author.username



	
	