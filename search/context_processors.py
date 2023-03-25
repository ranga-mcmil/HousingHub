from .forms import SearchForm

def base_data(request):
    data = {}
    data["search_form"] = SearchForm()
    return data

