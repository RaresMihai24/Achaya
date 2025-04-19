from django.contrib import messages

def change_currency(player, gold_delta=0, silver_delta=0, diamonds_delta=0, request=None):
    """
    Adjusts the player’s balances by the given deltas.
    Sends a Django message on failure if request is provided.
    Returns True iff the transaction succeeded.
    """
    # Check we’re not overdrawing
    if player.gold + gold_delta < 0 \
    or player.silver + silver_delta < 0 \
    or player.diamonds + diamonds_delta < 0:
        if request:
            messages.error(request, "Not enough funds.")
        return False

    player.gold     += gold_delta
    player.silver   += silver_delta
    player.diamonds += diamonds_delta
    player.save()
    return True