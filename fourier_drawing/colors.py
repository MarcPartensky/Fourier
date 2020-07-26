from collections import namedtuple
import random as rd
import math

Color=namedtuple('Color',['r','g','b'])

BLUE       = Color(  0,  0,255)
RED        = Color(255,  0,  0)
GREEN      = Color(  0,255,  0)
YELLOW     = Color(255,255,  0)
BLACK      = Color(  0,  0,  0)
WHITE      = Color(255,255,255)
GREY       = Color(100,100,100)
PURPLE     = Color(100,  0,100)
ORANGE     = Color(255,165,  0)
BROWN      = Color(160, 82, 45)
HALFGREY   = Color( 50, 50, 50)
DARKGREY   = Color( 20, 20, 20)
DARKRED    = Color( 10, 10, 10)
DARKGREEN  = Color(  0,100,  0)
DARKBLUE   = Color(  0,  0,100)
LIGHTRED   = Color(255,200,200)
LIGHTGREEN = Color(200,255,200)
LIGHTBLUE  = Color(200,200,255)
LIGHTBROWN = Color(229,219,222)
LIGHTGREY  = Color(200,200,200)
BEIGE      = Color(199,175,138)

sigmoid = s = lambda x:1/(1+math.exp(-x))
reverse_sigmoid = lambda x:math.log(x/(1-x))
#r=reverse_sigmoid()

bijection = lambda x,e,s:(x-e[0])/(e[1]-e[0])*(s[1]-s[0])+s[0]

random    = lambda :            Color(*[rd.randint(0,255)              for i in range(3)])
reverse   = lambda color:       Color(*[255-c                          for c in color])
darken    = lambda color,n=0:   Color(*[int(c*sigmoid(n/10))           for c in color])
lighten   = lambda color,n=0:   Color(*[int(255-(255-c)*sigmoid(n/10)) for c in color])
mix       = lambda cl1,cl2:     Color(*[(c1+c2)//2                     for (c1,c2) in zip(cl1,cl2)])
substract = lambda cl1,cl2:     Color(*[max(min(2*c1-c2,255),0)        for (c1,c2) in zip(cl1,cl2)])
increase  = lambda color,n=2:   Color(*[int(255*math.exp(n*math.log(c/255)))     for c in color])


def nuance(color1,color2,t,p=1/2):
    """Return a color between the two depending on the degree."""
    return Color(*[c1*(1-t**p)+c2*(t**p) for (c1,c2) in zip(color1,color2)])


def nuances(colors,t):
    """Does an interpolation between all the colors in order."""
    n=len(colors)
    int(t*n)

def ponderNuances(colors,t):
    """Does an interpolation between all the colors in order."""
    n=len(colors)
    int(t*n)





def getFromWavelength(wavelength):
    """Return a color using wavelength."""
    gamma,max_intensity=0.80,255
    def adjust(color, factor):
        if color==0: return 0
        else: return round(max_intensity*pow(color*factor,gamma))
    if 380<=wavelength<=440: r,g,b=-(wavelength-440)/(440-380),0,1
    elif 440<=wavelength<=490: r,g,b=0,(wavelength-440)/(490-440),1
    elif 490<=wavelength<=510: r,g,b=0,1,-(wavelength-510)/(510-490)
    elif 510<=wavelength<=580: r,g,b=(wavelength-510)/(580-510),1,0
    elif 580<=wavelength<=645: r,g,b=1,-(wavelength-645)/(645-580),0
    elif 645<=wavelength<=780: r,g,b=1,0,0
    else: r,g,b=0,0,0
    if 380<=wavelength<=420: factor=0.3+0.7*(wavelength-380)/(420-380)
    elif 420<=wavelength<=701: factor=1
    elif 701<=wavelength<=780: factor=0.3+0.7*(780-wavelength)/(780-700)
    else: factor=0
    r,g,b=adjust(r,factor),adjust(g,factor),adjust(b,factor)
    return Color(r,g,b)

def colorRange(t):
    bt=bijection(t,[0,1],[380,780])
    return getFromWavelength(bt)





if __name__=="__main__":
    print(darken(RED,10))
    print(mix(YELLOW,RED))
    print(reverse(LIGHTBROWN))
    print(substract(LIGHTBROWN,ORANGE))
    print(increase(LIGHTBROWN))
    print(nuance(YELLOW,RED,10))
    print("colorRange(0.5):",colorRange(0.1))
    print(BLUE.r)
    print("mycolors imported")
