from django.shortcuts import render, redirect, get_object_or_404
from .models import Dragon
from django.contrib import messages
from django.db.models import F
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Dragon

def index(request):
    # Retrieve all dragons for the selection list
    dragons = Dragon.objects.all()

    # Get the selected dragon by its name from the query parameter.
    name = request.GET.get('name')
    selected_dragon = None
    if name:
        selected_dragon = get_object_or_404(Dragon, name=name)

    # You can compute any additional values here if needed.
    # For example, if you want to pre-compute the total points,
    # you might do it as follows:
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

    # Pass all needed variables via the context.
    context = {
        'dragons': dragons,
        'selected_dragon': selected_dragon,
        'total_points': total_points,
        # You can also pass specific fields if you prefer:
        'specie': selected_dragon.specie if selected_dragon else '',
        'race': selected_dragon.race if selected_dragon else '',
        'sex': selected_dragon.sex if selected_dragon else '',
        'age': selected_dragon.age if selected_dragon else '',
        'height': selected_dragon.height if selected_dragon else '',
        'weight': selected_dragon.weight if selected_dragon else '',
        'born_on': selected_dragon.born_on if selected_dragon else '',
        'breed_by': selected_dragon.producer if selected_dragon else '',
		'res': selected_dragon.res if selected_dragon else '',
		'vit': selected_dragon.vit if selected_dragon else '',
		'dre': selected_dragon.dre if selected_dragon else '',
		'gal': selected_dragon.gal if selected_dragon else '',
		'sar': selected_dragon.sar if selected_dragon else '',
		'tra': selected_dragon.tra if selected_dragon else '',
		'ac_res': selected_dragon.ac_res if selected_dragon else '',
		'ac_vit': selected_dragon.ac_vit if selected_dragon else '',
		'ac_dre': selected_dragon.ac_dre if selected_dragon else '',
		'ac_gal': selected_dragon.ac_gal if selected_dragon else '',
		'ac_sar': selected_dragon.ac_sar if selected_dragon else '',
		'ac_tra': selected_dragon.ac_tra if selected_dragon else '',
		'GP': selected_dragon.GP if selected_dragon else '',
		'BLUP': selected_dragon.BLUP if selected_dragon else '',
		'mother': selected_dragon.mother or 'Unknown' if selected_dragon else '',
		'father': selected_dragon.father or 'Unknown' if selected_dragon else '',
		'current_time' : datetime.now().strftime("%H:%M %d/%m/%Y")
        # Add any other computed fields here (for example, masks for the bars)
    }
	
    if selected_dragon:
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

        traits = {
            "Attack": selected_dragon.res,
            "Defence": selected_dragon.vit,
            "Speed": selected_dragon.dre,
            "Magic": selected_dragon.gal,
            "Intuity": selected_dragon.sar,
            "Harmony": selected_dragon.tra,
        }

        traits_stars = {label: calculate_stars(value) for label, value in traits.items()}

        excellence_stars = sum(
            (value - 100) // 10 + 1 for value in traits.values() if value >= 100
        )

        ac_res_stars = calculate_stars(selected_dragon.ac_res)
        ac_vit_stars = calculate_stars(selected_dragon.ac_vit)
        ac_dre_stars = calculate_stars(selected_dragon.ac_dre)
        ac_gal_stars = calculate_stars(selected_dragon.ac_gal)
        ac_tra_stars = calculate_stars(selected_dragon.ac_tra)
        ac_sar_stars = calculate_stars(selected_dragon.ac_sar)


        context.update({
            "traits": traits,
            "traits_stars": traits_stars,
            "excellence_stars": excellence_stars,
            "ac_res_stars": ac_res_stars,
            "ac_vit_stars": ac_vit_stars,
            "ac_dre_stars": ac_dre_stars,
            "ac_gal_stars": ac_gal_stars,
            "ac_tra_stars": ac_tra_stars,
            "ac_sar_stars": ac_sar_stars,
        })
	

    return render(request, 'index.html', context)
	
def feed_dragon(request):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        dragon = get_object_or_404(Dragon, name=dragon_name)
        # Increase energy by 8, without exceeding 100
        dragon.energy = min(100, dragon.energy + 8)
        dragon.save()
        messages.success(request, f"Fed {dragon.name}! Energy is now {dragon.energy}.")
        return redirect('index')  # You'll set up this route in urls.py
		
def breed_dragon(request):
    if request.method == 'POST':
        # Process form data for breeding here
        # For demonstration, we'll just show a success message
        messages.success(request, "Breeding process initiated!")
        return redirect('index')
    else:
        # If someone tries to access via GET, redirect to index or render another template
        return redirect('index')
		
def view_dragon(request, name):
    # Retrieve the dragon by name
    dragon = get_object_or_404(Dragon, name=name)
    context = {
        'dragon': dragon,
    }
    return render(request, 'dragons/view_dragon.html', context)
	
def action_dragon(request, action):
    if request.method == 'POST':
        dragon_name = request.POST.get('dragon_name')
        dragon = get_object_or_404(Dragon, name=dragon_name)

        if action == 'feed':
            dragon.energy = min(100, dragon.energy + 8)
            messages.success(request, f"Fed {dragon_name}!")
        elif action == 'water':
            dragon.energy = min(100, dragon.energy + 2)
            dragon.moral = min(100, dragon.moral + 1)
            messages.success(request, f"Gave water to {dragon_name}!")
        elif action == 'play':
            dragon.energy = min(100, dragon.energy + 5)
            messages.success(request, f"Played with {dragon_name}!")
        elif action == 'groom':
            dragon.moral = min(100, dragon.moral + 3)
            messages.success(request, f"Groomed {dragon_name}!")
        elif action == 'treat':
            dragon.energy = min(100, dragon.energy + 10)
            messages.success(request, f"Given treat to {dragon_name}!")
        elif action == 'sleep':
            dragon.sleep = True  # ✅ make sure it's a boolean
            messages.success(request, f"Sent {dragon_name} to sleep!")
        else:
            messages.error(request, "Unknown action.")
            return redirect('index')

        dragon.save()
        return redirect(f"/?name={dragon_name}")
    else:
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
