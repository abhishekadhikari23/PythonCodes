n = int(input("Enter number of rows : "))
k = 1
for i in range(1,n+1):
    s = ''
    for j in range(0,i):
        s = str(k) + ' ' + s
        k = k+1
    print(s)