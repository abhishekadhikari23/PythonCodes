def pattern(n,n1):
    for i in range(1,n+1):
        s = ''
        for j in range(1,i+1):
            s = s + '* '
        print(s)
    for i in range(n1,0,-1):
        s = ''
        for j in range(1,i+1):
            s = s + '* '
        print(s)
n = int(input("Enter n : "))
if(n == 0):
    print("Nothing to show")
elif(n%2==0):
    n = int(n/2)
    n1 = n-1
    pattern(n,n1)
else:
    n = int(n/2) + 1
    n1 = n-1
    pattern(n,n1)

