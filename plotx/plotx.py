# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:01:39 2021

@author: DaveAstator
"""

import matplotlib.pyplot as plt;
import numpy as np;

# ------------------ data conversion -----------------
# cupher format 
# p:xy indexing over list of points [x,y], outputting indexes into p and [x,y] values into x and y lists
# -:z indexing over array of z values, discaridng their indexes (as marke by -)
# *z shorthand form of -:z
# x,z outputs lists into corresponding names.
def toPlotData(data, cypher):
    valDict = {}
    bins = cypher.split(',')
    if len(bins) == 1:
        addNestedToData(data,cypher,valDict)
    else:
        row = 0
        for b in bins:
            addNestedToData(data[row],b,valDict)
            row = row + 1
    return valDict


#new list cypher snytax: i:xyi:z
# for example [1,2,[3,4,5]] -:xy-:z

def addNestedToData(nest,cypher,valDict = {},trailNames='',trailVals=[]):
    cypher = cypher.replace('*','-:')
    
    for c in cypher.replace(':',''):
        if c not in valDict:
            valDict[c]=[]
    
    split = cypher.find(':')
    if (split < 1): # there is no more indexes
        nestSemantic = cypher
        
        if len(nestSemantic) == 1: # our nest is value
            valDict[nestSemantic].append(nest)
                
        else: #nest is list of values
            for n,v in zip(nestSemantic,nest):
                valDict[n].append(v)
        
        #write trailing values
        for n,v in zip(trailNames,trailVals):
            valDict[n].append(v)
        
    else: #we have index with props
        propSemantic = cypher[:split-1]
        idxSemantic = cypher[split-1]
        nestSemantic = cypher[split+1:]
        splitIndex = len(propSemantic)
        
        if splitIndex>0:  # add inner props to index and continue
            propValues = nest[:splitIndex]        
            nextNest = nest[splitIndex]
            
            newTrailNames = trailNames + propSemantic    
            newTrailVals = trailVals + propValues
            addNestedToData(nextNest,
                            idxSemantic+':'+nestSemantic,
                            valDict,
                            newTrailNames,
                            newTrailVals)

        else: # iterate over index
            newTrailNames = trailNames + idxSemantic            
            idx = 0    
            for egg in nest:
                newTrailVals = trailVals + [idx]
                idx = idx + 1
                nextNest = egg
                addNestedToData(nextNest, nestSemantic, valDict, newTrailNames, newTrailVals)
    return valDict

# ---------- PLOTTING ---------------
            
def UniformDots2D(x,y):
    low = np.min(np.concatenate((x,y)))
    high = np.max(np.concatenate((x,y)))
    plt.xlim(low, high)
    plt.ylim(low, high)
    plt.scatter(x,y)
    
def UniformLine2D(x,y):
    low = np.min(np.concatenate((x,y)))
    high = np.max(np.concatenate((x,y)))
    plt.xlim(low, high)
    plt.ylim(low, high)
    plt.plot(x,y)
    
def ValOrNone(key,dic):
    if key in dic:
        return dic[key]
    else:
        return None
    
def UniformDots3D_p(plotData):
    c = ValOrNone('c' , plotData);
    s = ValOrNone('s' , plotData);
    x = ValOrNone('x' , plotData);
    y = ValOrNone('y' , plotData);
    z = ValOrNone('z' , plotData);
    a = ValOrNone('a' , plotData);
    UniformDots3D(x,y,z,c,s,a)

def UniformLine3D_p(plotData):
    c = ValOrNone('c' , plotData);
    s = ValOrNone('s' , plotData);
    x = ValOrNone('x' , plotData);
    y = ValOrNone('y' , plotData);
    z = ValOrNone('z' , plotData);
    a = ValOrNone('a' , plotData);
    UniformLine3D(x,y,z,c,s,a)
    
def UniformDots3D(x,y,z,c = None, s = None, a = 1):
    print('3d point plot',s)
    
    if s == None:
        s = plt.rcParams['lines.markersize'] ** 2
        
    if a == None:
        a = 1
        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    low = np.min(np.concatenate((x,y,z)))
    high = np.max(np.concatenate((x,y,z)))
    
    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
    ax.set_zlim(low, high)
    ax.set_box_aspect((1, 1, 1)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.scatter(x,y,z, c=c, s=s, alpha = a)
    plt.show()  
    
def UniformLine3D(x,y,z,c = None, s = None, a = 1):
    print('3d point plot',s)
        
    if a == None:
        a = 1
        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    low = np.min(np.concatenate((x,y,z)))
    high = np.max(np.concatenate((x,y,z)))
    
    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
    ax.set_zlim(low, high)
    ax.set_box_aspect((1, 1, 1)) 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.plot(x,y,z, c=c, alpha = a)
    plt.show()


def create2dFigure():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_aspect('equal')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    return ax;

def create3dFigure():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_box_aspect((1, 1, 1)) 

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ax;

def plotLine3DLambda(ax, valDict):
    if 'a' not in valDict:
        a = 1
    if 'c' not in valDict:
        c = None
    return lambda: ax.plot(x,y,z, c=c, a = a)

def lines1d(valDicts):
    axes = create2dFigure()   
    low = valDicts[0]['x'][0]
    high = valDicts[0]['x'][0]
    for vd in valDicts:
        print(vd['x'])
        flatvals = vd['x']
        axes.plot(vd['x'])

        low = min(low,np.min(flatvals))
        high = max(high,np.max(flatvals))

    ax.set_xlim(low, high)
    ax.set_ylim(low, high)
        
    plt.show()
   
def lines2d(valDicts):
    actions=[]
    axes = create2dFigure()   
    low = valDicts[0]['x'][0]
    high = valDicts[0]['x'][0]
    for vd in valDicts:
        flatvals = np.concatenate(vd['x'],vd['y'])
        axes.plot(vd['x'],vd['y'])
        
        low = min(low,np.min(flatvals))
        high = max(high,np.max(flatvals))

    ax.set_xlim(low, high)
    ax.set_ylim(low, high)

    plt.show()

def lines3d(valDicts):
    axes = create3dFigure()   
    low = valDicts[0]['x'][0]
    high = valDicts[0]['x'][0]
    for vd in valDicts:
        flatvals = np.concatenate(vd['x'],vd['y'],vd['z'])
        plotLine3DLambda(axes,vd)
        low = min(low,np.min(flatvals))
        high = max(high,np.max(flatvals))

    ax.set_xlim(low, high)
    ax.set_ylim(low, high)

    plt.show()
    

# ------------ PUBLIC API -------------
def lines(array, cypher):
    valDicts=[]
    for ldata in array:
        valDicts.append(toPlotData(ldata,cypher))

    ndim = int('x' in cypher) + int('y' in cypher) + int('z' in cypher)
    if ndim ==1:
        lines1d(valDicts)
    if ndim ==2:
        lines2d(valDicts)  
    if ndim ==3:
        lines3d(valDicts)  

def dots(data, cypher):
    valDict = toPlotData(data,cypher)
    
    ndim = int('x' in cypher) + int('y' in cypher) + int('z' in cypher)

    if ndim <= 1:
        plt.plot(valDict['x'])
    if ndim == 2:
        UniformDots2D(valDict['x'],valDict['y'])
    if ndim == 3:
        UniformDots3D_p(valDict)

def line(data,cypher):
    lines([data],cypher)
    
    
# ---------- TESTING -----------

import math
pt = []
for z in range (0,100):
    pt.append([math.cos(z)*5,math.sin(z)*10,z])

pt=[]
for u in range (0,5):
    for v in range (0,10):
        for w in range (0,10):
            pt.append([u+math.sin(w),v+math.cos(u),w+v*0.1,u])

a=[[1,2,5],[3,4,5],[7,6,4]]
lines(a,'*x')

d=np.array([[1, 2, 3], [4, 5, 6]], np.int32)
dots(d,'*x,*y')

data = [[[1,2,3],[2,3,20],[5,5,11]],[0.1,0.2,0.8],8]
#dots(data,'zxy,c,s')
#line(data,'xyz,-,s')
dots(pt,'xyz1')
dots(pt,'xyz1')




addNestedToData([[11,21,31],[41,51,61]],'x:y:h',{})    

data=[
 [1,2,[-5,-6]],
 [11,12,[-15,-16]]
 ]

addNestedToData(data,'p:xyk:s',{})







            
    