from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VehicleProfile, VehicleImage, Comment
from .forms import VehicleProfileForm, VehicleImageForm, CommentForm

@login_required
def create_vehicle_profile(request):
    if request.method == 'POST':
        form = VehicleProfileForm(request.POST)
        if form.is_valid():
            if request.user.vehicle_profiles.count() < 3:
                vehicle_profile = form.save(commit=False)
                vehicle_profile.owner = request.user
                vehicle_profile.save()
                return redirect('vehicle_profile_dashboard')
            else:
                form.add_error(None, "You can only create up to 3 profiles.")
    else:
        form = VehicleProfileForm()
    return render(request, 'vehicle_profiles/create_vehicle_profile.html', {'form': form})

@login_required
def edit_vehicle_profile(request, pk):
    vehicle_profile = get_object_or_404(VehicleProfile, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = VehicleProfileForm(request.POST, instance=vehicle_profile)
        if form.is_valid():
            form.save()
            return redirect('vehicle_profile_dashboard')
    else:
        form = VehicleProfileForm(instance=vehicle_profile)
    return render(request, 'vehicle_profiles/edit_vehicle_profile.html', {'form': form, 'vehicle_profile': vehicle_profile})

@login_required
def delete_vehicle_profile(request, pk):
    vehicle_profile = get_object_or_404(VehicleProfile, pk=pk, owner=request.user)
    if request.method == 'POST':
        vehicle_profile.delete()
        return redirect('vehicle_profile_dashboard')
    return render(request, 'vehicle_profiles/delete_vehicle_profile.html', {'vehicle_profile': vehicle_profile})

def vehicle_profile_detail(request, pk):
    vehicle_profile = get_object_or_404(VehicleProfile, pk=pk)
    comments = vehicle_profile.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.vehicle_profile = vehicle_profile
            comment.save()
            return redirect('vehicle_profile_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'vehicle_profiles/vehicle_profile_detail.html', {
        'vehicle_profile': vehicle_profile, 
        'comments': comments, 
        'comment_form': comment_form
    })

@login_required
def vehicle_profile_dashboard(request):
    vehicle_profiles = request.user.vehicle_profiles.all()
    return render(request, 'vehicle_profiles/vehicle_profile_dashboard.html', {'vehicle_profiles': vehicle_profiles})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    vehicle_profile_pk = comment.vehicle_profile.pk
    if comment.author == request.user or comment.vehicle_profile.owner == request.user:
        comment.delete()
    return redirect('vehicle_profile_detail', pk=vehicle_profile_pk)
