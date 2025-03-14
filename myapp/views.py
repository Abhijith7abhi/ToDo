from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import User_form,Login_form

from myapp.models import User

from myapp.forms import Taskform

from myapp.models import TaskModel

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator



def is_user(fn):
    def wrapper(request, **kwargs):

        id=kwargs.get("pk")

        obj=TaskModel.objects.get(id=id)

        if obj.user_id==request.user:

            return fn(request,**kwargs)
        else:
            return redirect('login')
    return wrapper




class Registration(View):

    def get(self,request):

        form=User_form

        return render(request,"register.html",{"form":form})
    
    def post(self,request):

        form=User_form(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            User.objects.create_user(**form.cleaned_data)

            return redirect("login")
 


class Login(View):

    def get(self,request):

        form=Login_form

        return render(request,"login.html",{"form":form})
    
    def post(self,request):

        form=Login_form(request.POST)

        if form.is_valid():

            us_name=form.cleaned_data.get("username")

            pswd=form.cleaned_data.get("password")
            
            user=authenticate(request,username=us_name,password=pswd)

            if user:

                login(request,user)

                return redirect("create")

            else:

                return render(request,"login.html",{"form":form})
    


class TaskAdd(View):

    def get(self,request):

        form=Taskform

        data=TaskModel.objects.filter(user_id=request.user)

        return render(request,"task.html",{"form":form,"data":data})
    
    def post(self,request):

        form=Taskform(request.POST)

        if form.is_valid():
            
            TaskModel.objects.create(**form.cleaned_data,user_id=request.user)

        data=TaskModel.objects.filter(user_id=request.user)

        return render(request,"task.html",{"form":form,"data":data})
    

@method_decorator(decorator=is_user,name="dispatch")
class TaskDetail(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        data=TaskModel.objects.get(id=id)

        return render(request,"detail.html",{"data":data})





class Taskall(View):

    def get(self,request):

        data=TaskModel.objects.filter(user_id=request.user).order_by('is_completed','created_date')

        return render(request,"alltask.html",{"data":data})

        

class TaskDelete(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        data=TaskModel.objects.get(id=id)

        if data.user_id==request.user:

            data.delete()

            return redirect("all")

        else:

            print("get out")

            return redirect("login")




@method_decorator(decorator=is_user,name="dispatch")
class TaskUpdate(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        data=TaskModel.objects.get(id=id)

        form=Taskform(instance=data)

        return render(request,"taskupdate.html",{"form":form})
    
    def post(self,request,**kwargs):

        id=kwargs.get("pk")

        data=TaskModel.objects.get(id=id)

        form=Taskform(request.POST,instance=data)

        if form.is_valid():

         form.save()

        return redirect("all")

@method_decorator(decorator=is_user,name='dispatch')
class Taskedit(View):

    def get(self,request,**kwargs):

        id=kwargs.get("pk")

        data=TaskModel.objects.get(id=id)

        print(data)

        if data.is_completed==False:

            data.is_completed=True

            data.save()

        return redirect("all")
    

class CompletedView(View):

    def get(self,request):

        data=TaskModel.objects.filter(is_completed=True)

        return render(request,"completed.html",{"data":data})





        
class Signout(View):

    def get(self,request):

        logout(request)

        return redirect("login")




class UserdetailsView(View):

    def get(self,request):

        user=request.user

        total= TaskModel.objects.filter(user_id=request.user).count()

        incomplete=TaskModel.objects.filter(user_id=request.user,is_completed=False).count()

        complete=total-incomplete

        return render(request,"userdetails.html",{"total":total,"incomplete":incomplete,"complete":complete,"user":user})
    
