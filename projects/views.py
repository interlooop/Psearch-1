from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Project,Tag,Category
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects,paginateProjects
from django.contrib import messages




def projects(request):
    
    categories=Category.objects.all()
    searchValue=''

    projects, search_query= searchProjects(request,searchValue)
    custom_range,projects=paginateProjects(request,projects,6)


    order = ['Data Science', 'Network Management', 'Software Development','System Administration','Other']
    categories = sorted(categories, key=lambda x: order.index(x.name))
    

    context={'projects':projects,'search_query':search_query,
     'custom_range':custom_range,'categories':categories}
    
    template_name = ['web/index.html', 'index.html']
    return render(request, 'projects/projects.html', context)



def projectsByCategory(request, category_slug):

    category=None
    categories=Category.objects.all()

    searchValue=request.GET.get('searchValue')

    if category_slug:
       
        category = get_object_or_404(Category,slug=category_slug)
        
        projects, search_query= searchProjects(request,searchValue,category)
        custom_range,projects=paginateProjects(request,projects,6)
    else:
        projects, search_query= searchProjects(request,searchValue)
        custom_range,projects=paginateProjects(request,projects,6)
    
   


    order = ['Data Science', 'Network Management', 'Software Development','System Administration','Other']
    categories = sorted(categories, key=lambda x: order.index(x.name))
    

    context={'projects':projects,'search_query':search_query,
     'custom_range':custom_range,'category':category,'categories':categories}
    
    return render(request, 'projects/projects-by-category.html', context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def singleProject(request, pk):

    try:
        projectObj=Project.objects.get(id=pk)
        form=ReviewForm()
    except:
        messages.error(request,'An error has occurred!')
        return redirect('projects')
    
    
    if request.method=='POST':
        try:
            form=ReviewForm(request.POST)
            review=form.save(commit=False)
            review.project=projectObj
            review.owner=request.user.profile
            review.save(update_fields=['project','owner'])

            projectObj.getVoteStats
        except:
            messages.error(request,'An error has occurred!')
            return redirect('project', pk=projectObj.id)

        
        
        messages.success(request, 'Review successfully submited!')
        return redirect('project', pk=projectObj.id)
    

    return render(request,'projects/single-project.html',{'project': projectObj,'form':form})



    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login-user")
def createProject (request):
    
    profile=request.user.profile 
    form=ProjectForm()
    

    if request.method=='POST':
        
            newtags=request.POST.get('newtags').replace(',', " ").split()
            form=ProjectForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    project= form.save(commit=False)
                except:
                    messages.error(request,'An error has occurred!')
                    return redirect('create-project')
                project.owner=profile
                project.save(update_fields=['owner'])
                for tag in newtags:
                    tag,created=Tag.objects.get_or_create(name=tag)
                    project.tag.add(tag)
                return redirect('account')
            else:
                messages.error(request,'An error has occurred!')
                return redirect('account')
                
        

    context={'form':form}
    return render (request, "projects/project-form.html",context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login-user")
def updateProject (request,pk):
    
    profile=request.user.profile
    try:
        project=profile.project_set.get(id=pk)
        form=ProjectForm(instance=project)
    except:
        messages.error(request,'An error has occurred!')
        return redirect('account')
   

    if request.method=='POST':
        
            newtags=request.POST.get('newtags').replace(',', " ").split()
            form=ProjectForm(request.POST, request.FILES ,instance=project)

            if form.is_valid():
                form.save()
                for tag in newtags:
                    tag,created=Tag.objects.get_or_create(name=tag)
                    project.tag.add(tag)

                return redirect('account')
            else:
                messages.error(request,'An error has occurred!')
                return redirect('account')
        
            
    context={'form':form,'project':project}
    return render (request, "projects/project-form.html",context)



@login_required(login_url="login-user")
def deleteProject(request,pk):
    
    profile=request.user.profile
    try:
        project=profile.project_set.get(id=pk)
    except:
        messages.error(request,'An error has occurred!')
        return redirect('account')
   

    if request.method=='POST':
        try:
            project.delete()
            return redirect ('account')
        except:
            messages.error(request,'An error has occurred!')
            return redirect('account')


    context={'object':project}
    return render(request,'delete-template.html',context)