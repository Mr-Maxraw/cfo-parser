a = {1: 'asd', 2: 'qwe'}

print(a[1])
print(a[2])
a['qweiuer'] = 1
print(a['qweiuer'])
print(a)

x = 1
y = 2
print(type(x), type(a))
x, y = y, x
print(x , y)
z = x, y
print(type(z))
print(z)
y, x = z
print(f'z is: {z[0]}, {z[1]}')
print(x, y)