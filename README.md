# django-simple-search2

Search functionality for your Django app simplified.

This module enables simple-to-use search functionality for small to medium applications, that don't require big, complex search engines. ``django-simple-search2`` provides the minimum needed for having a search feature on your website, while at the same time leaving a loot of room for customization, such as implementing search on multiple models, in various views, or adding additional filters before performing the search.

This module is based on an article by Julien Phalip:

http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

# Usage

1. Install the module:

``pip install git+https://github.com/zefj/django-simple-search2``

2. Add ``django_simple_search2`` to your ``INSTALLED_APPS``.

3. Put the import statement at the top of your views.py

``from django_simple_search2 import search_handler``


``django_simple_search2.search_handler(query_string, model_fields)``
	This function takes two arguments and returns a dictionary with queries. It is the only function of this module you need to perform a search.

	Arguments:
		``query_string``
			The query string from an input field on your website, preferably ``request.GET['q']``, if your input field name parameter is ``name="q"``.

		``model_fields``
			A dictionary of model fields to perform search on, defined like so: 

			``model_fields = {
			    'Post': ['title', 'text', 'tags__name'],
			    'Tag': ['name']
			}``

			The keys should be verbose (preferably model names, but you can set whatever you like), you will be looking the object returned by ``search_handler`` up.

	Returns:
		``queries``
			A dictionary of keys provided in model_fields and corresponding queries in values, ready to put into `model.object.filter()` call. If an empty ``query_string`` is passed, the function returns ``None``. 

4. Write your views!

# Example search views utilising this module

```python
def search(request, template_name='mainsite/search_results.html'):

    model_fields = {
        'Post': ['title', 'text', 'tags__name'],
    }

    query_string = request.GET['q']
    queries = search_handler(query_string, model_fields)

    if queries:
        found_post_entries = Post.objects.filter(queries['Post']).distinct()

    else:
        found_post_entries = None

    return render_to_response(template_name,
                              {'query_string': query_string,
                              'search_results': found_post_entries,
                              },
                              context_instance=RequestContext(request))
```

This is an example of performing a single model search. The most important line is this: ``queries = search_handler(query_string, model_fields)``, whatever else you do in the view is up to you. This enables you to customize your view however you like. You can chain additional filters, perform search on many models and create a separate variable for every one of them, or throw them into a dictionary and pass it to the context as one. For example, here's a bit more complex view:

```python
def search(request, template_name='search_results.html'):

	model_fields = {
		'Contact': ['url', 'email'],
	}

    query_string = request.GET['q']
 	queries = search_handler(query_string, model_fields)

 	if queries:
        if request.user.is_superuser:
            found_entries = Contact.objects.select_related().filter(
                queries['Contact'])
        else:
            found_entries = Contact.objects.select_related().filter(
                queries['Contact'], added_by_admin=False)

        paginated_contacts = paginator(found_entries, request.GET.get('page'))

    else:
    	paginated_contacts = None

    return render_to_response('clovercrm/search_results.html',
                              {'query_string': query_string,
                               'search_results': paginated_contacts,
                              },
                              context_instance=RequestContext(request))
```                              

As you can see, this view has an additional conditional statement that changes the query appropriately. In this case, if the user performing the search is not authorised to view some records, they will not be included in search results. It also uses pagination to display results.

Here's an example of a view that utilises multiple model search, as well as pagination for one of them and ``distinct()`` method to make sure there are no duplicates:

```python
def search(request, template_name='search_results.html'):

    model_fields = {
        'Post': ['title', 'text', 'tags__name'],
        'Tag': ['name']
    }

    query_string = request.GET['q']
    queries = search_handler(query_string, model_fields)
    
    if queries:

        found_post_entries = Post.objects.filter(queries['Post']).distinct()
		found_tag_entries = Tag.objects.filter(queries['Tag']).distinct()
        
        paginated_found_post_entries = paginator(found_post_entries, request.GET.get('page'))

    else:
        paginated_found_post_entries = None

    return render_to_response(template_name,
                              {'query_string': query_string,
                              'search_post_results': paginated_found_post_entries,
                              'search_tag_results': found_tag_entries,
                              },
                              context_instance=RequestContext(request))
```

This view performs a search on two models, and allows the template to display results separately for both of them. This is perfect for a blog, where a user might want to get results both for posts and tags with one search. If you are not fond of your context growing bigger, you can put everything into a dictionary and pass it as a whole. Once again - it's all up to you.

# TODO's

* Setting to give control over multi-word query string search accuracy (return records that contain all words, or at least one of them).