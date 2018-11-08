import modules
tb=modules.module('movies')
print(tb.exe('select id,片名 from movies'))
print(tb.exe('desc movies'))