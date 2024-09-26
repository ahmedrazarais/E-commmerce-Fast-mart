from django.shortcuts import render
from signup.models import History,Accounts_Table, Cart
from django.shortcuts import render, redirect
from django.contrib import messages




# METHOD TO FETCH THE HISTORY OF THE USER
def user_history(request):
    # Get the user's email from the session or user model
    username = request.session.get('username')  # Assuming you store username in the session
    user = Accounts_Table.objects.get(username=username)  # Fetch the user instance
    user_history = History.objects.filter(user=user)  # Fetch user's history items
    
    if not user_history.exists():
        messages.error(request, "You have no purchase history.")
        return redirect('home')  # Redirect to home page if empty
    
    return render(request, "history/history.html", {'items': user_history})


