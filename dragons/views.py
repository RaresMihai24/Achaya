from django.shortcuts import render, redirect, get_object_or_404
from .models import Dragon, Player
from django.contrib import messages
from datetime import datetime
from .forms import RegistrationForm, LoginForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def get_current_user(request):
    """Helper to retrieve the logged-in Player from session."""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return Player.objects.get(id=user_id)
    except Player.DoesNotExist:
        return None


def index(request):
    # require login via session
    user = get_current_user(request)
    if not user:
        return redirect('auth')

    # Query only dragons owned by this user
    dragons = Dragon.objects.filter(owner=user)

    # Handle selection via GET parameter
    selected_dragon = None
    name = request.GET.get('name')
    if name:
        selected_dragon = get_object_or_404(Dragon, owner=user, name=name)

    # Calculate total ability points if a dragon is selected
    total_points = 0
    if selected_dragon:
        total_points = (
            selected_dragon.ac_res +
            selected_dragon.ac_vit +
            selected_dragon.ac_dre +
            selected_dragon.ac_gal +
            selected_dragon.ac_tra +
            selected_dragon.ac_sar
        )

    # Utility to compute star breakdowns
    def calculate_stars(value):
        if value < 100:
            return {"blue": [], "green": [], "half": False, "empty": range(10)}
        effective = value - 100
        total_green = effective // 10 + 1
        blue = total_green // 10
        green = total_green % 10
        half = effective % 10 >= 5
        empty = 10 - (blue + green + (1 if half else 0))
        return {
            "blue": range(int(blue)),
            "green": range(int(green)),
            "half": half,
            "empty": range(int(empty))
        }

    # Prepare context
    context = {
        'dragons':        dragons,
        'selected_dragon': selected_dragon,
        'total_points':    total_points,
        'current_time':    datetime.now().strftime("%H:%M %d/%m/%Y"),
    }

    if selected_dragon:
        # Basic fields
        context.update({
            'specie': selected_dragon.specie,
            'race':   selected_dragon.race,
            'sex':    selected_dragon.sex,
            'age':    selected_dragon.age,
            'height': selected_dragon.height,
            'weight': selected_dragon.weight,
            'born_on':  selected_dragon.born_on,
            'producer': selected_dragon.producer,
            'res':      selected_dragon.res,
            'vit':      selected_dragon.vit,
            'dre':      selected_dragon.dre,
            'gal':      selected_dragon.gal,
            'sar':      selected_dragon.sar,
            'tra':      selected_dragon.tra,
            'ac_res':   selected_dragon.ac_res,
            'ac_vit':   selected_dragon.ac_vit,
            'ac_dre':   selected_dragon.ac_dre,
            'ac_gal':   selected_dragon.ac_gal,
            'ac_tra':   selected_dragon.ac_tra,
            'ac_sar':   selected_dragon.ac_sar,
            'GP':       selected_dragon.GP,
            'BLUP':     selected_dragon.BLUP,
            'mother':   selected_dragon.mother or 'Unknown',
            'father':   selected_dragon.father or 'Unknown',
        })

        # Stats bars masks
        context.update({
            'energy_mask': 100 - selected_dragon.energy,
            'moral_mask':  100 - selected_dragon.moral,
            'health_mask': 100 - selected_dragon.health,
        })

        # Stars for ability points
        traits = {
            'Attack':  selected_dragon.res,
            'Defence': selected_dragon.vit,
            'Speed':   selected_dragon.dre,
            'Magic':   selected_dragon.gal,
            'Intuity': selected_dragon.sar,
            'Harmony': selected_dragon.tra,
        }
        traits_stars = {lbl: calculate_stars(val) for lbl, val in traits.items()}
        excellence_stars = sum((val - 100)//10 + 1 for val in traits.values() if val >= 100)

        # Stars for bars
        ac_res_stars = calculate_stars(selected_dragon.ac_res)
        ac_vit_stars = calculate_stars(selected_dragon.ac_vit)
        ac_dre_stars = calculate_stars(selected_dragon.ac_dre)
        ac_gal_stars = calculate_stars(selected_dragon.ac_gal)
        ac_tra_stars = calculate_stars(selected_dragon.ac_tra)
        ac_sar_stars = calculate_stars(selected_dragon.ac_sar)

        context.update({
            'traits':           traits,
            'traits_stars':     traits_stars,
            'excellence_stars': excellence_stars,
            'ac_res_stars':     ac_res_stars,
            'ac_vit_stars':     ac_vit_stars,
            'ac_dre_stars':     ac_dre_stars,
            'ac_gal_stars':     ac_gal_stars,
            'ac_tra_stars':     ac_tra_stars,
            'ac_sar_stars':     ac_sar_stars,
        })

    return render(request, 'index.html', context)


def feed_dragon(request):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        dragon = get_object_or_404(Dragon, name=dragon_name)
        dragon.energy = min(100, dragon.energy + 8)
        dragon.save()
        messages.success(request, f"Fed {dragon.name}! Energy is now {dragon.energy}.")
    return redirect('index')


def breed_dragon(request):
    if request.method == 'POST':
        messages.success(request, "Breeding process initiated!")
    return redirect('index')


def view_dragon(request, name):
    dragon = get_object_or_404(Dragon, name=name)
    return render(request, 'dragons/view_dragon.html', {'dragon': dragon})


def action_dragon(request, action):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        dragon = get_object_or_404(Dragon, name=dragon_name)
        # ... actions omitted for brevity ...
        dragon.save()
        return redirect(f"/?name={dragon_name}")
    return redirect('index')


def rename_dragon(request):
    if request.method == 'POST':
        dragon_id = request.POST.get('dragon_id')
        new_name = request.POST.get('new_name').strip()
        dragon = get_object_or_404(Dragon, id=dragon_id)
        if new_name:
            dragon.name = new_name
            dragon.save()
            messages.success(request, "Dragon renamed successfully!")
        else:
            messages.error(request, "Name cannot be empty.")
        return redirect(f"/?name={new_name}")
    return redirect('index')


def auth_view(request):
    reg_form = RegistrationForm(prefix='reg')
    login_form = LoginForm(prefix='log')
    if request.method == 'POST':
        if 'reg-submit' in request.POST:
            reg_form = RegistrationForm(request.POST, prefix='reg')
            if reg_form.is_valid():
                reg_form.save()
                messages.success(request, "Account created! Please log in below.")
                return redirect(reverse('auth'))
        elif 'log-submit' in request.POST:
            login_form = LoginForm(request.POST, prefix='log')
            if login_form.is_valid():
                user = login_form.cleaned_data['user']
                # THIS LINE tells Django “this request is now authenticated as that user”:
                auth_login(request, user)
                return redirect('index')
    return render(request, 'auth.html', {
        'reg_form': reg_form,
        'login_form': login_form,
    })


def claim_dragon(request, dragon_id):
    user = get_current_user(request)
    if not user:
        return redirect('auth')
    dragon = get_object_or_404(Dragon, pk=dragon_id)
    dragon.owner = user
    dragon.save()
    return redirect('my_dragons_list')


def my_dragons_list(request):
    user = get_current_user(request)
    if not user:
        return redirect('auth')
    dragons = Dragon.objects.filter(owner=user)
    return render(request, 'my_dragons.html', { 'dragons': dragons })

def logout_view(request):
    request.session.flush()    # removes all session data
    return redirect('auth')    # or wherever you want to send them
	
@login_required
def dragon_list(request):
    dragons = Dragon.objects.filter(owner=request.user)
    return render(request, 'dragon_list.html', { 'dragons': dragons })

