n = int(input("Enter number of rows : "))
for i in range(1,n+1):
    s = ''
    l = 0
    for j in range(1,i+1):
        s = s + str(j) + ' '
        l = j-1
    for j in range(1,i):
        s = s + str(l) + ' '
        l = l-1
    print(s)
    