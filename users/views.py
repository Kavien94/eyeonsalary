from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from users.forms import CustomUserCreationForm

from plotly.offline import plot
from plotly.graph_objs import Scatter

# Create your views here.

def dashboard(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    return render(request, "users/dashboard.html", context={'plot_div': plot_div})

def register(request):

    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )

    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))