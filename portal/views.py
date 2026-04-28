
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Company, Application, Profile, Review
from django.db.models import Q, Avg

def job_list(request):
    jobs = Job.objects.all()
    query = request.GET.get('q')
    location = request.GET.get('location')
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(requirements__icontains=query))
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    job_type = request.GET.get('job_type')
    exp = request.GET.get('experience_level')
    if job_type: jobs = jobs.filter(job_type=job_type)
    if exp: jobs = jobs.filter(experience_level=exp)

    sort = request.GET.get('sort')
    if sort == 'date':
        jobs = jobs.order_by('-created_at')
    
    return render(request, 'portal/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'portal/job_detail.html', {'job': job})

def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    profile = request.user.profile
    Application.objects.create(job=job, jobseeker=request.user, resume=profile.resume)
    return redirect('job_list')

def employer_dashboard(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'portal/employer_dashboard.html', {'jobs': jobs})

def salary_insights(request):
    insights = Job.objects.values('title', 'location').annotate(avg_salary=Avg('salary'))
    return render(request, 'portal/salary_insights.html', {'insights': insights})

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'portal/company_detail.html', {'company': company})
