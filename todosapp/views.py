from django.shortcuts import redirect, render
from django.urls import is_valid_path
from django.views.generic import View
from todosapp.forms import LoginForm, RegistrationForm, TodoForm,TodoModelForm
from todosapp.models import Todos
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
# Create your views here.


class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoModelForm()
        return render(request,"addtodo.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TodoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'todo has been created')
            return redirect("todolist")
        
        else:
            messages.error(request,'todo has not been created')


class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todos.objects.all()
        return render(request,"todolist.html",{'todos':qs})
        


class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        todo=Todos.objects.filter(id=id)
        return render(request,"todo-details.html",{'todo':todo})

class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Todos.objects.filter(id=id).delete()
        messages.success(request,'todo has been deleted')
        return redirect("todolist")


class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        todo=Todos.objects.get(id=id)
        form=TodoModelForm(instance=todo)
        
        return render(request,"todo-update.html",{"form":form})
    def post(self,request,*args,**kwargs):

        id=kwargs.get("id")
        todo=Todos.objects.get(id=id)
        form=TodoModelForm(instance=todo,data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Todo has been updated')
            return redirect("todolist")

        else:
            messages.error(request,'Todo has not been created')


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Registered Successfully")
            return redirect("todolist")
        else:
            messages.error(request,"registration failed")
            return render(request,"registration.html",{"form":form})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                return redirect("todolist")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"login.html",{"form":form})


        