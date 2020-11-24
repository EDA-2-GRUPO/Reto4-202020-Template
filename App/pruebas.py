
def de(x,y,w):
    print(x,y,w,1)
    if w!=2:
     x-=1
     y-=1
     w+=1
     de(x,y,w)
     print(x,y,w,2)
    return(x,y)
de(10,2,0)