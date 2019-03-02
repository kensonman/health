from django.shortcuts import render

# Create your views here.
def dashboard(req):
   params=dict()
   return render(req, 'health/dashboard.html', params)
