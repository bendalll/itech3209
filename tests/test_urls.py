from django.urls import resolve

# 
resolver = resolve('/cards/')
assert(resolver.func.func_name, 'cards')
