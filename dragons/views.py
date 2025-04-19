from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from datetime import datetime

from .models import Dragon
from .forms import RegistrationForm, LoginForm

@login_required(login_url='auth')
def index(request):
    # Only dragons owned by the logged‑in user
    dragons = Dragon.objects.filter(owner=request.user)

    # Which dragon (if any) is selected?
    selected_dragon = None
    name = request.GET.get('name')
    if name:
        selected_dragon = get_object_or_404(Dragon, owner=request.user, name=name)

    # Compute total ability points
    total_points = 0
    if selected_dragon:
        total_points = sum([
            selected_dragon.ac_res, selected_dragon.ac_vit,
            selected_dragon.ac_dre, selected_dragon.ac_gal,
            selected_dragon.ac_tra, selected_dragon.ac_sar
        ])

    # Star‑calculation helper
    def calculate_stars(value):
        # cast to int immediately so all further math is integral
        v = int(value)
        if v < 100:
            return {
                "blue":  range(0),
                "green": range(0),
                "half":  False,
                "empty": range(10),
            }
        eff = v - 100         # now an integer
        steps = eff // 10 + 1 # total “green steps” beyond the first 100
        blue  = steps // 10
        green = steps % 10
        half  = (eff % 10) >= 5
        empty = 10 - (blue + green + (1 if half else 0))
        return {
            "blue":  range(blue),
            "green": range(green),
            "half":  half,
            "empty": range(empty),
        }


    # Build context
    context = {
        "dragons": dragons,
        "selected_dragon": selected_dragon,
        "total_points": total_points,
        "current_time": datetime.now().strftime("%H:%M %d/%m/%Y"),
    }

    if selected_dragon:
        # Basic fields
        context.update({
            "specie": selected_dragon.specie,
            "race":   selected_dragon.race,
            "sex":    selected_dragon.sex,
            "age":    selected_dragon.age,
            "height": selected_dragon.height,
            "weight": selected_dragon.weight,
            "born_on":  selected_dragon.born_on,
            "producer": selected_dragon.producer,
            "res":      selected_dragon.res,
            "vit":      selected_dragon.vit,
            "dre":      selected_dragon.dre,
            "gal":      selected_dragon.gal,
            "sar":      selected_dragon.sar,
            "tra":      selected_dragon.tra,
            "ac_res":   selected_dragon.ac_res,
            "ac_vit":   selected_dragon.ac_vit,
            "ac_dre":   selected_dragon.ac_dre,
            "ac_gal":   selected_dragon.ac_gal,
            "ac_tra":   selected_dragon.ac_tra,
            "ac_sar":   selected_dragon.ac_sar,
            "GP":       selected_dragon.GP,
            "BLUP":     selected_dragon.BLUP,
            "mother":   selected_dragon.mother or "Unknown",
            "father":   selected_dragon.father or "Unknown",
            "energy_mask": 100 - selected_dragon.energy,
            "moral_mask":  100 - selected_dragon.moral,
            "health_mask": 100 - selected_dragon.health,
        })

        # Star breakdowns
        traits = {
            "Attack":  selected_dragon.res,
            "Defence": selected_dragon.vit,
            "Speed":   selected_dragon.dre,
            "Magic":   selected_dragon.gal,
            "Intuity": selected_dragon.sar,
            "Harmony": selected_dragon.tra,
        }
        traits_stars     = {lbl: calculate_stars(val) for lbl, val in traits.items()}
        excellence_stars = sum((val - 100)//10 + 1 for val in traits.values() if val >= 100)
        ac_res_stars = calculate_stars(selected_dragon.ac_res)
        ac_vit_stars = calculate_stars(selected_dragon.ac_vit)
        ac_dre_stars = calculate_stars(selected_dragon.ac_dre)
        ac_gal_stars = calculate_stars(selected_dragon.ac_gal)
        ac_tra_stars = calculate_stars(selected_dragon.ac_tra)
        ac_sar_stars = calculate_stars(selected_dragon.ac_sar)

        context.update({
            "traits":           traits,
            "traits_stars":     traits_stars,
            "excellence_stars": excellence_stars,
            "ac_res_stars":     ac_res_stars,
            "ac_vit_stars":     ac_vit_stars,
            "ac_dre_stars":     ac_dre_stars,
            "ac_gal_stars":     ac_gal_stars,
            "ac_tra_stars":     ac_tra_stars,
            "ac_sar_stars":     ac_sar_stars,
        })

    return render(request, "index.html", context)


def auth_view(request):
    # Where to go after login
    next_url = request.GET.get("next", reverse("index"))

    reg_form   = RegistrationForm(prefix="reg")
    login_form = LoginForm(prefix="log")

    if request.method == "POST":
        if "reg-submit" in request.POST:
            reg_form = RegistrationForm(request.POST, prefix="reg")
            if reg_form.is_valid():
                reg_form.save()
                messages.success(request, "Account created! Please log in.")
                return redirect(reverse("auth"))
        elif "log-submit" in request.POST:
            login_form = LoginForm(request.POST, prefix="log")
            if login_form.is_valid():
                user = login_form.cleaned_data["user"]
                auth_login(request, user)
                return redirect(next_url)

    return render(request, "auth.html", {
        "reg_form":   reg_form,
        "login_form": login_form,
    })


@login_required(login_url='auth')
def dragon_list(request):
    dragons = Dragon.objects.filter(owner=request.user)
    return render(request, "dragon_list.html", { "dragons": dragons })


@login_required(login_url='auth')
def logout_view(request):
    auth_logout(request)
    return redirect("auth")

@login_required(login_url='auth')
def breed_dragon(request):
    if request.method == 'POST':
        messages.success(request, "Breeding process initiated!")
    return redirect('index')
    
@login_required(login_url='auth')    
def view_dragon(request, name):
    # Sidebar list
    dragons = Dragon.objects.filter(owner=request.user)
    # The one to show
    sd = get_object_or_404(Dragon, owner=request.user, name=name)

    # Helper to build star‑dicts
    def calculate_stars(value):
        # cast to int immediately so all further math is integral
        v = int(value)
        if v < 100:
            return {
                "blue":  range(0),
                "green": range(0),
                "half":  False,
                "empty": range(10),
            }
        eff = v - 100         # now an integer
        steps = eff // 10 + 1 # total “green steps” beyond the first 100
        blue  = steps // 10
        green = steps % 10
        half  = (eff % 10) >= 5
        empty = 10 - (blue + green + (1 if half else 0))
        return {
            "blue":  range(blue),
            "green": range(green),
            "half":  half,
            "empty": range(empty),
        }

    # Total ability points
    total_points = (
          sd.ac_res + sd.ac_vit + sd.ac_dre
        + sd.ac_gal + sd.ac_tra + sd.ac_sar
    )

    # Star dicts for each stat
    ac_res_stars = calculate_stars(sd.ac_res)
    ac_vit_stars = calculate_stars(sd.ac_vit)
    ac_dre_stars = calculate_stars(sd.ac_dre)
    ac_gal_stars = calculate_stars(sd.ac_gal)
    ac_tra_stars = calculate_stars(sd.ac_tra)
    ac_sar_stars = calculate_stars(sd.ac_sar)

    # Genetic potential “traits”
    traits = {
        "Attack":  sd.res,
        "Defence": sd.vit,
        "Speed":   sd.dre,
        "Magic":   sd.gal,
        "Intuity": sd.sar,
        "Harmony": sd.tra,
    }
    traits_stars     = {lbl: calculate_stars(val) for lbl, val in traits.items()}
    excellence_stars = sum((v - 100)//10 + 1 for v in traits.values() if v >= 100)

    # Action buttons
    actions = ['feed','water','play','groom','treat','sleep']

    # Build context, **including** your missing basic fields:
    context = {
        # sidebar + selection
        "dragons":         dragons,
        "selected_dragon": sd,

        # basic info you need in the template
        "specie":  sd.specie,
        "race":    sd.race,
        "sex":     sd.sex,
        "age":     sd.age,
        "height":  sd.height,
        "weight":  sd.weight,
        "born_on": sd.born_on,
        "producer": sd.producer,

        # totals & masks
        "total_points": total_points,
        "energy_mask":  100 - sd.energy,
        "moral_mask":   100 - sd.moral,
        "health_mask":  100 - sd.health,

        # ability stats & stars
        "ac_res_stars": ac_res_stars,
        "ac_vit_stars": ac_vit_stars,
        "ac_dre_stars": ac_dre_stars,
        "ac_gal_stars": ac_gal_stars,
        "ac_tra_stars": ac_tra_stars,
        "ac_sar_stars": ac_sar_stars,
        "res": sd.res,
        "vit": sd.vit,
        "dre": sd.dre,
        "gal": sd.gal,
        "sar": sd.sar,
        "tra": sd.tra,

        # genetic potential
        "GP":             sd.GP,
        "BLUP":           sd.BLUP,
        "traits":         traits,
        "traits_stars":   traits_stars,
        "excellence_stars": excellence_stars,

        # action buttons
        "actions": actions,

        # parent links, only render if not null
        "mother": sd.mother or None,
        "father": sd.father or None,
    }


    return render(request, "dragon_view.html", context)

@login_required(login_url='auth')
def action_dragon(request, action):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        # make sure it really belongs to the user!
        dragon = get_object_or_404(Dragon, owner=request.user, name=dragon_name)

        if action == 'feed':
            dragon.energy = min(100, dragon.energy + 8)
            messages.success(request, f"Fed {dragon.name}! Energy is now {dragon.energy}.")
        elif action == 'water':
            dragon.energy = min(100, dragon.energy + 2)
            dragon.moral  = min(100, dragon.moral  + 1)
            messages.success(request, f"Gave water to {dragon.name}! Energy: {dragon.energy}, Moral: {dragon.moral}.")
        elif action == 'play':
            dragon.energy = min(100, dragon.energy + 5)
            messages.success(request, f"Played with {dragon.name}! Energy is now {dragon.energy}.")
        elif action == 'groom':
            dragon.moral = min(100, dragon.moral + 3)
            messages.success(request, f"Groomed {dragon.name}! Moral is now {dragon.moral}.")
        elif action == 'treat':
            dragon.energy = min(100, dragon.energy + 10)
            messages.success(request, f"Given treat to {dragon.name}! Energy is now {dragon.energy}.")
        elif action == 'sleep':
            dragon.sleep = True
            messages.success(request, f"{dragon.name} is now sleeping.")
        else:
            messages.error(request, "Unknown action.")

        dragon.save()
        # Redirect back to the detail view for this dragon
        return redirect('view_dragon', dragon_name)

    # if not POST, just bounce back home
    return redirect('index')

@login_required(login_url='auth')
def feed_dragon(request):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        dragon = get_object_or_404(Dragon, name=dragon_name)
        dragon.energy = min(100, dragon.energy + 8)
        dragon.save()
        messages.success(request, f"Fed {dragon.name}! Energy is now {dragon.energy}.")
    return redirect('index')

@login_required(login_url='auth')
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
    return redirect('view_dragon', dragon_name)


@login_required(login_url='auth')
def claim_dragon(request, dragon_id):
    user = get_current_user(request)
    if not user:
        return redirect('auth')
    dragon = get_object_or_404(Dragon, pk=dragon_id)
    dragon.owner = user
    dragon.save()
    return redirect('my_dragons_list')

@login_required(login_url='auth')
def my_dragons_list(request):
    user = get_current_user(request)
    if not user:
        return redirect('auth')
    dragons = Dragon.objects.filter(owner=user)
    return render(request, 'my_dragons.html', { 'dragons': dragons })
