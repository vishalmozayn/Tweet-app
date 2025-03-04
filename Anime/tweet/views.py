from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,User_RegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import login
# Create your views here.

def index(request):
    return render(request,'index.html')

def Tweet_list(request):
   tweets = Tweet.objects.all().order_by('-created_at')
   return render(request,'Tweet_list.html',{'tweets': tweets})

@login_required
def Tweet_create(request):
    if request.method == "POST":
      form= TweetForm(request.POST, request.FILES)
      if form.is_valid():
       tweet= form.save(commit=False)
       tweet.user=request.user
       tweet.save()
       return redirect('Tweet_list')
    else:
       form= TweetForm()
    return render(request, 'tweet_form.html',{'form': form} )

@login_required
def Tweet_edit(request,tweet_id):
   tweet= get_object_or_404(Tweet, pk=tweet_id,user=request.user)
   if request.method== "POST":
     form= TweetForm(request.POST, request.FILES,instance=tweet)
     if form.is_valid():
        tweet= form.save(commit=False)
        tweet.user=request.user
        tweet.save()
        return redirect('Tweet_list')
   else:
     form=TweetForm(instance=tweet)
   return render(request, 'tweet_form.html',{'form': form} )
   
@login_required
def Tweet_delete(request,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
       tweet.delete()
       return redirect('Tweet_list')
    return render(request, 'tweet_confrim_delete.html',{'tweet': tweet} )

       
    
def register(request):
   if request.method=='POST':
     form= User_RegistrationForm(request.POST)
     if form.is_valid():
        user=form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request,user)
        return redirect('Tweet_list')
   
   
   else:
     form=User_RegistrationForm()
   
   return render(request, 'registration/register.html',{'form': form} )

