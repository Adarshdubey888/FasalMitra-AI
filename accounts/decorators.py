from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

def farmer_required(view_func):

    @never_cache
    def wrapper(request, *args, **kwargs):

        if request.session.get('farmer_phone'):

            return view_func(request, *args, **kwargs)

        return redirect('/login/')

    return wrapper