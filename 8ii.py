s = 'A'
k = 0
n = int(input("Enter a number : "))
for i in range(1,n+1):
    a = ''
    for j in range(0,i):
        a = a + chr(ord(s)+k) + ' '
        k = k+1
    print(a)