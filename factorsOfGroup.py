def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def auxCheckT(a,b,i,x):
    count=0
    for m in a:
        for n in b:
            if (m+n)%x == i:
                count = count +1
    if count ==1 :
        return True
    else:
        return False
    

def findFactors(n):
    l=[]
    for i in range(n):
        l.append(i)
    y=[]
    for i in range(1 << n):
        y.append([l[j] for j in range(n) if (i & (1 << j))])
    isFactors=True
    result=[]
    for p in y:
        for q in y:
            isFactors=True
            for ele in l:
                if not (auxCheck(p,q,ele,n)) :
                    isFactors =False
                    break
            if isFactors:
                if not (0 in intersection(p,q)):
                    if (len(p) < n and len(q) < n):
                        result.append((p,q))       
    return result

def findTilings(n):
    l=[]
    for i in range(n):
        l.append(i)
    y=[]
    for i in range(1 << n):
        y.append([l[j] for j in range(n) if (i & (1 << j))])
    isFactors=True
    result=[]
    for p in y:
        for q in y:
            isFactors=True
            for ele in l:
                if not (auxCheck(p,q,ele,n)) :
                    isFactors =False
                    break
            if isFactors:
                if (0 in intersection(p,q)):
                    if (len(p) < n and len(q) < n):
                        result.append((p,q))       
    return result
               
    
for x in findFactors(12):
    print(x)
    
print(tilings)

for x in findTilings(12):
    print(x)
