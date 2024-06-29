from functools import wraps

from django.http import JsonResponse


def post_method_required(view_f):
    """Decorator for views that requires POST HTTP request method,
    returning corresponding JsonResponse if necessary.
    """
    @wraps(view_f)
    def wrapper_view(request, *args, **kwds):
        if request.method != 'POST':
            return JsonResponse({'error': 'POST request required.'},
                                status=400)
        return view_f(request, *args, **kwds)
    return wrapper_view
