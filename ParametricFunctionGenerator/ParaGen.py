# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 08:32:38 2021

@author: DaveAstator
"""
import math
import numpy as np

#converts literals to dict calls.
def litToDict(st,dictName='vd'):
    if type(st) != str:
        st=str(st)

    st2= '_'+st+'_'
    res =''
    for i in range(len(st)):
        c= st2[i+1]
        if c.isalpha():
            if not (st2[i].isalpha() or st2[i+2].isalpha()):
               res = res + dictName+'["'+c+'"]' 
               continue
        res = res + c
    return res
        
#main function that uses iterator definitions
# for now it uses list of lists [var name, from, to, step]
def Iterate(iterList, output, trailIndex={}):
    selfIter=iterList[0]
    selfName=selfIter[0]
    
    if selfName not in output:
        output[selfName]=[]
    print(output)

    low = litToDict(selfIter[1],'trailIndex')
    high = litToDict(selfIter[2],'trailIndex')
    step = litToDict(selfIter[3],'trailIndex')
    print(low,high,step)
        
    low=eval(low)
    high=eval(high)
    step=eval(step)
    print(low,high,step)
    rng = high-low
    count = math.ceil(rng/step)

    
    if len(iterList) == 1:
        for itr in np.linspace(low,high,count):
            trailIndex[selfName]=itr
            print(trailIndex)       
            
            #write index since we are at final iterator
            print(trailIndex)
            for k in trailIndex.keys():
                output[k].append(trailIndex[k])
    
    # there are more nested iterators, so go in.
    else:
        for itr in np.linspace(low,high,count):
            trailIndex[selfName]=itr
            Iterate(iterList[1:],output,trailIndex)
        
def TEST_Iterate():
    construct=[
    ['u',1,5,0.3],
    ['v','u','u*2',0.3]]
    
    outp = {}
    outp['x']=[]
    Iterate(construct,outp)    
        
def CalculateFunctions(funcList,indexDict):
    for k in indexDict.keys():
        indexDict[k]=np.asarray(indexDict[k])
    for f in funcList:
        varname=f[0]
        func=f[1]
        indexDict[varname] = eval(litToDict(func,'indexDict'))
    return indexDict
        
def TEST_CalcFunc():
        CalculateFunctions([['z','1+x']],{"x":[1.2,4]})
        
def CreateIteratedValues(construct):
    iters=[]
    funcs=[]
    for e in construct:
        if len(e) >2:
            iters.append(e)
        else:
            funcs.append(e)
    indexes={}
    Iterate(iters,indexes)
    return CalculateFunctions(funcs,indexes)

    
def TEST_Construct():
    #Apparently this works!
    construct=[
        ['u',1,5,0.3],
        ['v','u','u*2',0.3],
        ['x','u+v'],
        ['y','x/4'],
        ['c','x*y']
        ]
    
    rr= CreateIteratedValues(construct)

def FullTEST():
    TEST_Iterate()
    TEST_CalcFunc()
    TEST_Construct()

FullTEST()