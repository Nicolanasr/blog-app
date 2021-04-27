from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
import re

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter()
@stringfilter
def get_word(value, word):
    word_index = value.lower().find(word.lower())

    if word_index > 5:
        if word_index+len(word)+20 < len(value):
            return  "..." + value[word_index-5:word_index] + "<b><i>" + value[word_index:word_index+len(word)] + "</i></b>" + value[word_index+len(word):word_index+len(word)+20] + "..."
        else:
            return  "..." + value[word_index-5:word_index] + "<b><i>" + value[word_index:word_index+len(word)] + "</i></b>" + value[word_index+len(word):word_index+len(word)+20]
    else:
        if word_index+len(word)+20 < len(value):
            return  value[:word_index] + "<b><i>" + value[word_index:word_index+len(word)] + "</i></b>" + value[word_index+len(word):word_index+len(word)+20] + "..."
        else:
            return  value[:word_index] + "<b><i>" + value[word_index:word_index+len(word)] + "</i></b>" + value[word_index+len(word):word_index+len(word)+20]