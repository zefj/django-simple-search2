# http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:

            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)

    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            

            q = Q(**{"%s__icontains" % field_name: term})

            if or_query is None:
                or_query = q

            else:
                or_query = or_query | q

        if query is None:
            query = or_query

        else:
            """
            Change '|' to '&' for more strict search, for example 'foo bar' in the search
            bar will return records that contain BOTH words, instead of records that 
            contain at least one of them. 

            This is useful in some cases and is left for the admin to decide. For example,
            on a blog you might want to look up posts that contain the words Python or
            Django. This is when '|' is more suitable, because '&' would only return posts
            that contain both Python and Django, so you're missing out on Python posts.
            """
            query = query | or_query  

    return query


def search_handler(query_string, model_fields): 
    queries = {}

    if query_string:
        for model_name, fields in model_fields.iteritems():
            queries[model_name] = get_query(query_string, fields)
    else:
        return

    return queries
