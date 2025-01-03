n1=15
n2=20
if(n1>n2):
    i=n2
else :
    i=n1
check=1
for idx in range(1,i):
    if(n1%idx==0 and n2%idx==0):
        check=idx
print(check)