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
def print_tree(tree, level=0):
    if isinstance(tree, list):
        print_tree(tree[2], level + 1)
        print('    ' * level + str(tree[0]))
        print_tree(tree[1], level + 1)
    else:
        if tree:
            print('    ' * level + str(tree))
def lexical(ids,ops,i = 1,ind=0,d={}):
    ref = {}
    s=''
    for k,id in enumerate(ids):
        if id in d:
            if re.match(r"[0-9]+",id) or re.match(r"[0-9]+\.[0-9]+",id):
                ref[d[id]] = id
            if ind < len(ops):
                if k+1 < len(ids):
                    if ids[k+1] == ')':
                        s += f"{d[id]} ) {ops[ind]} "
                    else:
                        s += f"{d[id]} {ops[ind]} "
                else:
                    s += f"{d[id]} {ops[ind]} "
            else:
                s += f"{d[id]} "
            ind += 1
            continue
        if re.match(r"[0-9]+",id) or re.match(r"[0-9]+\.[0-9]+",id):
            ref[f"id{i}"] = id
            d[id] = f"id{i}"
        if id == ')':
            if k == len(ids)-1:
                s += ' )'
            continue
        if id == '(':
            s += id+" "
            i-=1
            ind-=1
        elif ind < len(ops):
            if k+1 < len(ids):
                if ids[k+1] == ')':
                    s += f"id{i} ) {ops[ind]} "
                else:
                    s += f"id{i} {ops[ind]} "
            else:
                s += f"id{i} {ops[ind]} "
            d[id] = f"id{i}"
        else:
            s += f"id{i}"
            d[id] = f"id{i}"
        
        i+=1
        ind+=1
    return s,ref,i-1,d;
def syntax(pos_s):
    stack = []
    for token in pos_s:
        if re.match(r"[a-zA-Z0-9]+", token):
            stack.append(token)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append([token, operand1, operand2])
    return print_tree(stack.pop())
def semantic(pos_ssem ,ref):
    pos_s = pos_ssem[::]
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
            if j == '=':
                df['Opnd'].append(op[j])
                df['arg1'].append(b)
                df['arg2'].append('')
                df['res'].append(a)
                continue;
            temp = f'temp{i}'
            df['Opnd'].append(op[j])
            df['arg1'].append(a)
            df['arg2'].append(b)
            df['res'].append(temp)
            stk.append(temp)
            i+=1
    return df,i;    
""" def targetcode(pos_ss,refe):
    d={}
    df = {'Opnd':list(),'arg1':list(),'arg2':list()}
    k = 0
    for j,pos_s in enumerate(pos_ss):
        print(pos_s)
        for i in range(len(pos_s)):
            if pos_s[i] in refe[j]:
                pos_s[i] = '#'+refe[j][pos_s[i]]
        
        stk = []
        op = {'+':'Add','-':'Sub','*':'Mul','/':'Div','^':'Pow','=':'Eq'}
        for l in pos_s:
            if re.match(r"[a-zA-Z0-9]+",l) or l[0] == '#':
                stk.append(l)
            else:
                b = stk.pop()
                a = stk.pop()
                if a not in d:
                    df['Opnd'].append('LDA')
                    df['arg1'].append(f"R{k}")
                    df['arg2'].append(a)
                    d[a]=f'R{k}'
                a = d[a]
                if b in d:
                    b = d[b]
                k+=1
                if l == '=':
                    df['Opnd'].append(op[l])
                    df['arg1'].append(b)
                    df['arg2'].append(a)
                    continue;
                temp = f'R{k}'
                df['Opnd'].append(op[l])
                df['arg1'].append(a)
                df['arg2'].append(b)
                stk.append(temp)
    df = pd.DataFrame(df)
    print(df)
 """

if __name__ == "__main__":
    lexi = []
    refe = []
    idx = 0
    ind = -1
    d = {}
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
            if re.match("[a-zA-Z0-9]+",i) or (i == '(' or i == ')'):
                ids.append(i)
        lex_out, ref, idx,d = lexical(ids,ops,idx+1,0,d=d)
        lexi.append(lex_out)
        refe.append(ref)
    print("After Lexical Analysis:\n")
    for lexo in lexi:
        print(lexo)
    print("After Syntax Analysis:\n")
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
        print()
    print("After Semantic Analysis:\n")
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
    if len(df['Opnd'])>0:
        print(pd.DataFrame(df))
    else:
        print(pd.DataFrame(df1))
    """ 
    print("Target code:")
    targetcode(pos_ss,refe) """