from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import GenomicData
from .forms import GenomicDataForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def upload_data(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = GenomicDataForm(request.POST, request.FILES)
        if form.is_valid():
            genomic_data = form.save(commit=False)
            genomic_data.user = request.user
            genomic_data.save()
            return redirect('home')
    else:
        form = GenomicDataForm()
    return render(request, 'upload.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def data_detail(request, data_id):
    genomic_data = get_object_or_404(GenomicData, id=data_id)
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'data_detail.html', {'genomic_data': genomic_data, 'all_users': all_users})

from django.shortcuts import render, get_object_or_404, redirect
from .models import GenomicData
from django.contrib.auth.models import User

def share_data(request, data_id):
    # Récupérer l'objet GenomicData à partager
    genomic_data = get_object_or_404(GenomicData, id=data_id)

    # Gérer les requêtes POST (partage des données)
    if request.method == 'POST':
        # Récupérer les utilisateurs sélectionnés depuis le formulaire
        user_ids = request.POST.getlist('users')
        users = User.objects.filter(id__in=user_ids)  # Filtrer les utilisateurs sélectionnés
        genomic_data.shared_with.set(users)  # Associer les utilisateurs à l'objet GenomicData
        genomic_data.save()  # Sauvegarder les modifications

        # Rediriger vers la page de détails de la donnée après le partage
        return redirect('data_detail', data_id=data_id)

    # Gérer les requêtes GET (affichage du formulaire de partage)
    else:
        users = User.objects.all()  # Récupérer tous les utilisateurs
        return render(request, 'share_data.html', {
            'genomic_data': genomic_data,
            'users': users
        })


from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile

def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import GenomicData, User
from django.utils.html import strip_tags

def share_data(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_files = GenomicData.objects.filter(user=request.user)
    
    if request.method == 'POST':
        file_id = request.POST.get('file')
        user_ids = request.POST.getlist('users')
        
        if file_id and user_ids:
            genomic_data = get_object_or_404(GenomicData, id=file_id, user=request.user)
            users = User.objects.filter(id__in=user_ids)
            genomic_data.shared_with.add(*users)
            genomic_data.save()
            
            # Créer des notifications pour les utilisateurs
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f"{request.user.username} a partagé '{genomic_data.title}' avec vous.",
                    shared_file=genomic_data  # Ajouter le fichier partagé à la notification
                )
            
            return redirect('data_detail', data_id=genomic_data.id)
    
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'share_data.html', {
        'user_files': user_files,
        'all_users': all_users,
    })

def view_shared_file(request, file_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Vérifier que l'utilisateur a accès au fichier
    genomic_data = get_object_or_404(GenomicData, id=file_id, shared_with=request.user)
    
    return render(request, 'view_shared_file.html', {
        'genomic_data': genomic_data,
    })

import pandas as pd

import chardet

def analyze_data(request, data_id):
    genomic_data = get_object_or_404(GenomicData, id=data_id)
    
    # Récupérer le fichier des données génomiques
    file_path = genomic_data.data_file.path

    # Utiliser chardet pour détecter l'encodage du fichier
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    try:
        # Ouvrir le fichier avec l'encodage détecté
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
    except UnicodeDecodeError:
        # Si l'encodage détecté échoue, essayer d'autres encodages possibles
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()

    # Vous pouvez ajouter du code pour traiter le contenu du fichier ici
    return render(request, 'analyze_data.html', {'content': content})


def search_data(request):
    query = request.GET.get('q')
    if query:
        results = GenomicData.objects.filter(title__icontains=query) | GenomicData.objects.filter(description__icontains=query)
    else:
        results = GenomicData.objects.none()
    return render(request, 'search_data.html', {'results': results, 'query': query})

def visualize_data_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_data = GenomicData.objects.filter(user=request.user)
    return render(request, 'visualize_data_list.html', {'user_data': user_data})

def analyze_data_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_data = GenomicData.objects.filter(user=request.user)
    return render(request, 'analyze_data_list.html', {'user_data': user_data})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from .forms import UserSettingsForm

@login_required
def user_settings(request):
    user = request.user  # Récupérer l'utilisateur connecté

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            # Si un mot de passe est renseigné, on le met à jour
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            form.save()  # Sauvegarder les modifications
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('edit_profile')  # Rediriger vers la page de modification
    else:
        form = UserSettingsForm(instance=user)  # Afficher le formulaire pré-rempli avec les informations de l'utilisateur

    return render(request, 'user_settings.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_notifications.html', {'notifications': notifications})




