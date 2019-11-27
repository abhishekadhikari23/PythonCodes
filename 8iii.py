n = int(input("Enter number of rows : "))
s = (n-1)*2
for i in range(1, n+1):
    a = ''
    for j in range(0,s):
        a = a + ' '
    for j in range(0, (i*2)-1):
        a = a + '* '
    print(a)
    s = s-2
