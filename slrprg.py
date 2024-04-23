nt=list(map(str,input("Enter non-terminals:\n").split()))
t=list(map(str,input("Enter terminals:\n").split()))
t.append("$")
n=int(input("Enter no. of productions\n"))
print("Enter production give space bw lhs and rhs ")
lhs,rhs={},{}
for i in range(1,n+1):
    lhs[i],rhs[i]=input().split()
action,goto={},{}
m=int(input("Enter no. of closures: "))
print("enter action and goto entries: give - and -1 for action and goto entries respectively if they are empty")
print("The order for terminals and non terminal: ")
print(*t," ",*nt)
for i in range(m):
    l=list(map(str,input().split()))
    j=0
    action[i],goto[i]={},{}
    for ter in t:
        action[i][ter]=l[j]
        j+=1
    for non in nt:
        goto[i][non]=int(l[j])
        j+=1
st=input("Enter string:\n")
stack=[0]
inp1=0
while inp1<len(st):
    inp=st[inp1]
    top=stack[-1]
    print(stack)
    a=action[top][inp]
    if a[0]=='S':
        stack.append(inp)
        stack.append(int(a[1:]))
        inp1+=1
    elif action[top][inp][0] == 'R':
        l=2*len(rhs[int(a[1:])-1])
        for i in range(l):
            stack.pop()
        top1 = stack[-1]
        stack.append(lhs[int(a[1:])-1])
        if goto[top1][stack[-1]] >= 0:
            stack.append(goto[top1][stack[-1]])
        else:
            print("Rejected")
            break;
    elif inp == "$" and action[stack[-1]][inp] == "Accept":
        print("Accepted")
        inp+=1
    else:
        print("Rejected")
        break;