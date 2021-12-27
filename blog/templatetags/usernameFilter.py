from django import template


register = template.Library()


@register.filter(name="getFirstLetter")
def getFirstLetter(username):
    return username[:1].upper()


def getRestOfUsername(username):
    return usernname[1:]
