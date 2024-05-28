import re
import pandas as pd
def prec(i):
    if i=='^':
        return 3;
    if i == '*' or i == '/':
        return 2;
    if i == '+' or i == '-':
        return 1;
    else:
        return -1;
def assoc(c):
    if c == '^':
        return 'R'
    return 'L'
def inftopost(s):
    stk = []
    pos_s = []
    j = 0
    n = len(s)
    ops = ['=','+','-','*','/','^']
    for j in range(n):
        i = s[j]
        if i in ops:
            if not stk:
                stk.append(i)
            else:
                while stk and (prec(i) < prec(stk[-1]) or (prec(i) == prec(stk[-1]) and assoc(i) == 'L')):
                    pos_s.append(stk.pop())
                stk.append(i)
        elif i == '(':
            stk.append(i)
        elif i == ')':
            while stk and stk[-1] != '(':
                pos_s.append(stk.pop())
            stk.pop()  

        else:
            pos_s.append(i)
            
    while stk:
        pos_s+=stk.pop()
    return pos_s;
def recur(l):
    if isinstance(l,list):
        a = []
        for i in l:
            a.extend(recur(i))
        return a;
    else:
        return [l]
def post_to_pre(pos_s):
    stack = []
    ops = {'=','+', '-', '*', '/', '^'}

    for token in pos_s:
        if token not in ops:  
            stack.append(token)
        else:  
            op2 = stack.pop()
            op1 = stack.pop()
            expression = [token ,op1, op2]
            stack.append(expression)
    return recur(stack.pop())
def lexical(ids,ops,i = 1,ind=0):
    ref = {}
    s=''
    for id in ids:
        if ind < len(ops):
            s+=f"id{i} {ops[ind]} "
        else:
            s+=f"id{i}"
        if re.match(r"[0-9]+",id[1]) or re.match(r"[0-9]+\.[0-9]+",id[1]):
            ref[f"id{i}"] = id[1]
        i+=1
        ind+=1
    return s,ref,i-1;
def syntax(pos_s):
    pre_s = post_to_pre(pos_s)
    ops = ['=','+','-','*','/','^']
    j = 0
    i = 1
    print(pre_s)
    print('\t',pre_s[0])
    while i < len(pre_s):
        if i > 2:
            if (pre_s[i-2] in ops or pre_s[i-1] in ops) and pre_s[i] not in ops:
                print('\t'*(j-2),pre_s[i],'\t\t',pre_s[i+1])
            else:
                print('\t'*(j),pre_s[i],'\t\t',pre_s[i+1])
        else:
            print('\t'*(j),pre_s[i],'\t\t',pre_s[i+1])
        j+=1
        i+=2
    print()
def semantic(pos_s,ref):
    for i in range(len(pos_s)):
        if pos_s[i] in ref:
            pos_s[i] = ref[pos_s[i]] 
    return syntax(pos_s);
def Intermediate(pos_s,i = 0,df = {'Opnd':list(),'arg1':list(),'arg2':list(),'res':list()}):
    stk = []
    op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
    for j in pos_s:
        if re.match(r"[a-zA-Z0-9]+",j) or j[0] == '#':
            stk.append(j)
        else:
            b = stk.pop()
            a = stk.pop()
            temp = f'temp{i}'
            df['Opnd'].append(op[j])
            df['arg1'].append(a)
            df['arg2'].append(b)
            df['res'].append(temp)
            stk.append(temp)
            i+=1
    return df,i;    
if __name__ == "__main__":
    lexi = []
    refe = []
    idx = 0
    j = 0
    ind = -1
    while (True):
        inp = input()
        if inp == '-1':
            break;
        a = list(map(str,inp.split(" ")))
        op = {'=':'equ','+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow'}
        ids = []
        ops = []
        for i in a:
            if i in op:
                ops.append(i)
                a.remove(i)
        for i in a:
            if re.match("[a-zA-Z0-9]+",i):
                ids.append((j,i))
                j+=1
        lex_out, ref, idx = lexical(ids,ops,idx+1,0)
        lexi.append(lex_out)
        refe.append(ref)
    print("After Lexical analysis:\n")
    for lexo in lexi:
        print(lexo)
    print("After Syntax analyser:\n")
    pos_ss = []
    for lexo in lexi:
        flag = 0
        s = lexo.split(" ")
        if '=' in lexo:
            lhs,s = map(str,lexo.split("="))
            lhs,s = lhs.strip(),s.strip().split(" ")
            flag = 1
        pos_s= inftopost(s)
        op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
        df = {'Opnd':[],'arg1':[],'arg2':[],'res':[]}
        if flag:
            pos_s.insert(0,lhs)
            pos_s.append('=')
        pos_ss.append(pos_s)
        syntax(pos_s)
        print()
    print("After Semantic Analyser:\n")
    for i, pos_s in enumerate(pos_ss):
        semantic(pos_s,refe[i])
        print()
    print("After Intermediate Code Generation:\n")
    for j,pos_s in enumerate(pos_ss):
        for i in range(len(pos_s)):
            if pos_s[i] in refe[j]:
                pos_s[i] = '#'+refe[j][pos_s[i]]
        if j == 0:
            df1,ind = Intermediate(pos_s)
        else:
            df,ind1 = Intermediate(pos_s,i=ind,df=df1) 
            ind = ind1
            df1 = df
    print(pd.DataFrame(df))

