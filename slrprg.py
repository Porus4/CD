nt,t=[],[]
n=6
gram = ['E E+T', 'E T', 'T T*F', 'T F','F (E)','F i']
lhs,rhs={},{}
for i in range(1,n+1):
    lhs[i],rhs[i]=gram[i-1].split()
    if lhs[i] not in nt:
        nt.append(lhs[i])
    for val in rhs[i]:
        if val.isupper():
            if val not in nt:
                nt.append(val)
        else:
            if val not in t:
                t.append(val)
t.append('$')
action,goto={},{}
m=12
closures = ['- - S4 - S5 - 1 2 3',
'S6 - - - - Accept -1 -1 -1',
'R2 S7 - R2 - R2  -1 -1 -1',
'R4 R4 - R4 - R4 -1 -1 -1',
'- - S4 - S5 - 8 2 3',
'R6 R6 - R6 - R6 -1 -1 -1',
'- - S4 - S5 - -1 9 3',
'- - S4 - S5 - -1 -1 10',
'S6 - - S11 - - -1 -1 -1',
'R1 S7 - R1 - R1 -1 -1 -1',
'R3 R3 - R3 - R3 -1 -1 -1',
'R5 R5 - R5 - R5 -1 -1 -1']
for i in range(m):
    l=closures[i].split()
    j=0
    action[i],goto[i]={},{}
    for ter in t:
        action[i][ter]=l[j]
        j+=1
    for non in nt:
        goto[i][non]=int(l[j])
        j+=1
st='i+i*i$'
stack=[0]
inp1=0
while inp1<len(st):
    inp=st[inp1]
    top=stack[-1]
    a=action[top][inp]
    print(stack,a)
    if a[0]=='S':
        stack.append(inp)
        stack.append(int(a[1:]))
        inp1+=1
    elif a[0] == 'R':
        l=2*len(rhs[int(a[1:])])
        for i in range(l):
            stack.pop()
        top1 = stack[-1]
        stack.append(lhs[int(a[1:])])
        if goto[top1][stack[-1]] >= 0:
            stack.append(goto[top1][stack[-1]])
        else:
            print("Rejected")
            break;
    elif inp == "$" and action[stack[-1]][inp] == "Accept":
        print("Accepted")
        inp1+=1
    else:
        print("Rejected")
        break;