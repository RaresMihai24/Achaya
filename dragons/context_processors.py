def player_currencies(request):
    if request.user.is_authenticated:
        return {
            'gold_balance':     request.user.gold,
            'silver_balance':   request.user.silver,
            'diamond_balance':  request.user.diamonds,
        }
    return {}