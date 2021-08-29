from django import template

register = template.Library()


@register.simple_tag
def my_url(value , field_name , urlencode=None):
    if urlencode:
        url = f'{field_name}={value}'  # get current url (which is just a page number)
        querystring = urlencode.split('&')
        # get every element except the page number:
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name , querystring)
        # combine the elements with the current url:
        encoded_querystring = '&'.join(filtered_querystring)
        url = f'?{encoded_querystring}&{url}'
    else:
        url = f'?{field_name}={value}'

    return url
