from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.forms import BooksModelForm,RegistrationModelForm,LoginForm
from myapp.models import Books
from django.contrib.auth import authenticate,login,logout


# -----------------method_decorator----convert function(fn) decorator into a method decorator------------------
from django.utils.decorators import method_decorator

#----------messages----------------
from django.contrib import messages

# -----------signup----------------
from django.contrib.auth.models import User

# ------------login--------------------------
from django.contrib.auth import authenticate,login,logout


# -----------signin--decorators------------------
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'invalid session')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)    
    return wrapper
# ---------------end decorators-----------------------------------

# Create your views here.
#-----------------create books view------------------- 
@method_decorator(signin_required,name='dispatch')
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BooksModelForm()
        return render(request,'books_add.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=BooksModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"successfully created")
            print('created')
            return render(request,'books_add.html',{'form':form})
        else:
            messages.error(request,"Error to create book")
            return render(request,'books_add.html',{'form':form})

#-----------------list books view------------------- 
@method_decorator(signin_required,name='dispatch')
class BookListView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            qs=Books.objects.all()
            # -------------------------------
            if "book price" in request.GET:
                bk_prc=request.GET.get("book price")
                qs=qs.filter(book_price=bk_prc)
            #------------------------------------
            authers=Books.objects.all().values_list("auther_name",flat=True).distinct()
            print(authers)
    
            if "auther name" in request.GET:
                authr_nme=request.GET.get("auther name")
                qs=qs.filter(auther_name__iexact=authr_nme) #__iexact  =>case nokathe wrk cheyan   
            return render(request,'books_list.html',{'data':qs,'authers':authers})
        # -------------------------------------------
        else:
            messages.error(request,'Invalid Session')
            return  redirect('signin')
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")  #box is a name of html input name
        qs=Books.objects.filter(book_name__icontains=name) #__icontains >exact name kanikkan
        
        return render(request,"books_list.html",{'data':qs})
    
#-----------------book details view------------------- 
@method_decorator(signin_required,name='dispatch')
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Books.objects.get(id=id)
        return render(request,'book_details.html',{'data':qs})
    
#------------------delete book view------------------------------
@method_decorator(signin_required,name='dispatch')
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Books.objects.get(id=id).delete()
        messages.success(request,"successfully deleted book")
        return redirect('book-all')
#------------------update book view------------------------------
@method_decorator(signin_required,name='dispatch')
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Books.objects.get(id=id)
        form=BooksModelForm(instance=obj)
        return render(request,'book_edit.html',{'form':form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        obj=Books.objects.get(id=id)
        form=BooksModelForm(request.POST,instance=obj,files=request.FILES)   #  edutha id details text box ellm fill ayi kidakan
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully updated book details")
            # return redirect('book-all') 
            return redirect('book-detail',pk=id)
        else:
            messages.error(request,"Not updated book details")
            return render(request,'book_edit.html',{'form':form})
# ------------signup view-----------------
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationModelForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationModelForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data) #orm query
            messages.success(request,'Successfully Created')
            return render(request,'register.html',{'form':form})
        else:
            messages.error(request,'Failed to Create')
            return render(request,'register.html',{'form':form})
# ------------signup view-----------------
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'signin.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(request.user,"before")

            # print(form.cleaned_data)
            user_name=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            # print(user_name,pwd)
            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid credential")
            
                login(request,user_obj)
                print(request.user,"after") #to identify user
                messages.error(request,'Successfully logined your account')
                return redirect('book-all')
        messages.error(request,'Invalid credential please try again')
        return render(request,"signin.html",{'form':form})
# ----------------logout-----------------------
@method_decorator(signin_required,name='dispatch')
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')

