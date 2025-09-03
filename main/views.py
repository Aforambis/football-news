from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406421081',
        'name': 'Rusydan Mujtaba Ibnu Ramadhan',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)