

x=int(input("Enter a number 'x': "))
y=int(input("Enter a number 'y': "))
print('x**y: ',x**y)
logresult=0
while x>=2:
    x=x/2
    logresult+=1
print('log(x): ',logresult)
