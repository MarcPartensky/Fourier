"""
Features:
1:COMPLETED: print #renvoie str
2:COMPLETED: addition #renvoie Polynomial
3:COMPLETED: multiplication #renvoie Polynomial
4:COMPLETED: derive #renvoie un Polynomial
5:COMPLETED: division #renvoie couple de Polynomial
6:COMPLETED: pgcd #renvoie Polynomial
7:COMPLETED: ppcm #renvoie Polynomial
8:COMPLETED: taylor #renvoie Polynomial
9: factoriser #renvoie str ou liste de liste des coefficients "pareil"
10: racines reelles #renvoie liste des racines reelles
11: racines complexes #renvoie liste des racines complexes
12: Decomposition en éléments simples
12: show #Affiche le polynome sur une fenetre pygame, pyglet ou matplotlib
"""

from copy import deepcopy
# import matplotlib.pyplot as plt #Old way to show the polynomials on screen. Not very nice though...

# from mygrapher.grapher import Grapher #Used to show the polynome on screen with the ability to move within it.

import random  # Used only to generate random polynomials.
import functools

# Changing the type of the coefficients
#from decimal import Decimal
#from numpy import float128

# p=Polynomial.createFromInterpolation(x,y)


def prod(l): return functools.reduce(lambda a, b: a * b, l)


class Polynomial:
    def null():
        """Return the null polynomial."""
        return Polynomial([0])

    def sum(ps):
        """Sum polynomials between themselves."""
        v = Polynomial([0])  # Addition neutral
        for p in ps:
            v += p
        return v

    def prod(ps):
        """Multiply polynomials between themselves."""
        v = Polynomial([1])  # Multiplication neutral
        for p in ps:
            v *= p
        return v

    def createFromInterpolation(x, y):
        """Create a polynomial using the lagrangian interpolation."""
        n = max(len(x), len(y))
        p = Polynomial.sum([Polynomial([y[j]]) * Polynomial.prod([Polynomial([-x[i] / (
            x[j] - x[i]), 1 / (x[j] - x[i])]) for i in range(n) if x[i] != x[j]]) for j in range(n)])
        return Polynomial(p.coefficients)

    def __init__(self, coefficients, definition=[-10**20, 10**20]):
        """Create a polynomial using its coefficients."""
        self.coefficients = coefficients
        self.definition = definition

    def make(self, f):
        """Transform all the coefficients into a decimal type."""
        self.coefficients = [f(c) for c in self.coefficients]
        self.definition = [f(d) for d in self.definition]

    def __str__(self):
        """Return the usual representation of a polynomial."""
        if self.coefficients == []:
            return "0"
        liste = []
        if self.coefficients[0] != 0:
            liste.append(str(self.coefficients[0]))
        for degre, coefficient in enumerate(self.coefficients[1:], 1):
            if coefficient != 0:
                liste.append(str(coefficient) + "X^" + str(degre))
        liste.reverse()
        text = "+".join(liste)
        text = text.replace("^1", "").replace("+-", "-").replace("1X", "X")
        return text

    def adapt(coefficients, size):
        """Add zeros to the coefficients using coefficients and size."""
        return coefficients + [0] * (size - len(coefficients))

    def __eq__(self, other):
        """Determine if two polynomials are equals by checking if the coefficients
        are the same."""
        return self.coefficients == other.coefficients

    def __add__(self, other):
        """Add 2 polynomials together by adding their coefficients."""
        maxdegree = max(self.degree + 1, other.degree + 1)
        cA = Polynomial.adapt(self.coefficients, maxdegree)
        cB = Polynomial.adapt(other.coefficients, maxdegree)
        coefficients = [a + b for (a, b) in zip(cA, cB)]
        A = Polynomial(coefficients)
        A.correct()
        return A

    def __sub__(self, other):
        """Substract 2 polynomials together by multiplying the second polynomial by -1 and adding it to the first using add method."""
        return self + other * Polynomial([-1])

    def __mul__(self, other):
        """Multiply 2 polynomials together using the formula for the coefficients."""
        degree = len(self.coefficients) + len(other.coefficients)
        A = self.coefficients + [0] * (degree - len(self.coefficients) + 1)
        B = other.coefficients + [0] * (degree - len(other.coefficients) + 1)
        newcoefficients = []
        for k in range(degree + 1):
            coeff = 0
            for i in range(k + 1):
                coeff += A[i] * B[k - i]
            newcoefficients.append(coeff)
        C = Polynomial(newcoefficients)
        C.correct()
        return C

    def __pow__(self, n):
        """Does an ~exponentiation of the polynomial."""
        return Polynomial.mul([self for i in range(n)])

    def correct(self):
        """Correct the coefficients of the polynomial by deleting useless zeros at the end,"""
        while len(self.coefficients) > 1:
            if self.coefficients[-1] == 0:
                del self.coefficients[-1]
            else:
                break
        if self.coefficients == [0]:
            self.coefficients = []
        """and then replace float coefficients by int coefficients if possible."""
        for i in range(len(self.coefficients)):
            if self.coefficients[i] == int(self.coefficients[i]):
                self.coefficients[i] = int(self.coefficients[i])

    def __len__(self):
        """Return the number of coefficients.
        It is important to notice that it is not the degree due to the fact that
        the polynomial might have a degree of -inf and the len method must have positive values.
        In such a case this method will raise an error.
        It is why it is better to use the degree method in the general case."""
        A = deepcopy(self)
        A.correct()
        return len(A.coefficients) - 1

    def getDegree(self):
        """Return the degree of a polynomial.
        It will return -1 if the degree is -inf to be computer friendly."""
        A = deepcopy(self)
        A.correct()
        return len(A.coefficients) - 1

    def __getitem__(self, index):
        """Return a coefficient of the polynomial."""
        return self.coefficients[index]

    def __setitem__(self, index, value):
        """Change a coefficient of the polynomial."""
        self.coefficients[index] = value

    def __delitem__(self, index):
        """Delete a coefficient of the polynomial."""
        del self.coefficients[index]

    def derivate(self):
        """Derivate the polynomial."""
        self.coefficients = [i * c for (i, c) in enumerate(self.coefficients)]
        del self.coefficients[0]

    def derivative(self):
        """Return the derivative polynomial."""
        newcoefficients = [i * c for (i, c) in enumerate(self.coefficients)]
        del newcoefficients[0]
        return Polynomial(newcoefficients)

    def unit(self):
        """Return the polynomial unit form."""
        k = self.coefficients[-1]
        newcoefficients = []
        for i in range(len(self.coefficients)):
            newcoefficients.append(self.coefficients[i] / k)
        A = Polynomial(newcoefficients)
        A.correct()
        return A

    def unitarize(self):
        """Convert the polynomial into its unit form."""
        self.coefficients = self.unit().coefficients

    def __xor__(self, other):
        """Return the HCF (PGCD  en francais) of self and other by Euclide algorithm. Make use of "^" operator."""
        R0 = deepcopy(self)
        R1 = deepcopy(other)
        R0.correct()
        R1.correct()
        listR = [R0, R1]
        while listR[-1].degree > 0:
            R, Q = listR[-2] / listR[-1]
            listR.append(R)
        return listR[-2]

        # Resultat d'une enorme galere de 2h...
        # Algorithme d'Euclide:
        # a=b*q0+r0
        # b=r*q1+r1
        # r=r1*q2+r2
        # r1=r2*q3+r3
        # ...
        # ri=r(i-1)*q(i-1)+1+0

    def __or__(self, other):
        """Return the LCM (PPCM en francais) using "i have absolutely no clue how to do this so figure it out!" Make use of "|" operator."""
        # On sent la (tres) grosse fatigue apres minuit.
        return "Figure it out!"

    def __truediv__(self, other):
        """Return the division of 2 polynomials."""
        R = deepcopy(self)
        B = deepcopy(other)
        R.correct()
        B.correct()
        Q = Polynomial([])
        while R.degree >= B.degree:
            d = R.degree - B.degree + 1
            C = Polynomial([0 for i in range(d)])
            C[-1] = R[-1] / B[-1]
            R = R - B * C
            Q = Q + C
        return [R, Q]

        # Ce que j'ai du faire pour trouver l'implementation...
        # On a: A=BQ+R
        # [3,2,4,5,1]/[1,4,1]
        # [3,2,3,1,0]=[3,2,4,5,1]-[0,0,1]*[1,4,1] #[0,0,1,4,1]
        # [3,1,-1,0]=[3,2,3,1]-[0,1]*[1,4,1] #[0,1,4,1]
        # [4,5,0]=[3,1,-1]-[-1]*[1,4,1] #[-1,-4,-1]
        # [4,5]

        # 5=8*0+5 cas particulier de la division euclidienne

    def isDivisible(self, other):
        """Determine if the polynomial is divisible by other."""
        q, r = self / other
        return r == Polynomial.zero

    def __call__(self, x):
        """Evaluate the polynomial given an x value."""
        return sum([c * x**n for (n, c) in enumerate(self.coefficients)])

    def getFactoredForm(self):
        """Return the list of the factors of the factored form of the polynomial."""
        return

    def allDerivatives(self):
        """Return the list of all derivatives of the polynome until the zero polynome."""
        B = deepcopy(self)
        derivatives = [deepcopy(self)]
        while B.degree > 1:
            B.derivate()
            derivatives.append(deepcopy(B))
        return derivatives

    def getRootsByDichotomy(self, precision=1e-15):
        """Return the list of all the roots of the polynomial."""
        """Does that by finding where all the derivates cancel, to find new extrema and applying tvi."""
        roots = []
        derivatives = self.allDerivatives()
        derivatives.reverse()
        old_extrema = []
        for derivative in derivatives:
            new_extrema = []
            neglim = self.definition[0]
            poslim = self.definition[1]
            extrema = [neglim] + old_extrema + [poslim]
            for i in range(len(extrema) - 1):
                if derivative(extrema[i]) * derivative(extrema[i + 1]) <= 0:
                    new_extrema.append(derivative.dichotomy(
                        extrema[i], extrema[i + 1], precision))
            old_extrema = new_extrema[:]
        return new_extrema

    def dichotomy(self, xa, xb, precision=1e-15):
        """Return a float value x between a and b for which the polynomial canceled itself.
        Does that based on theoreme of intermediate value with dichotomy."""
        if self(xa) * self(xb) > 0:
            raise Exception(
                "The polynomial cannot cancel itself within this interval.")
        a = min(xa, xb)
        b = max(xa, xb)
        x = (a + b) / 2
        while abs(self(x)) > precision:
            print(x, self(x), abs(self(x)), precision)
            if self(x) * self(b) > 0:
                b = x
            if self(x) * self(a) > 0:
                a = x
            x = (a + b) / 2
        return x

    def getRoots(self, precision=1e-15):
        """
        Return the roots of the polynomial by doing the best possible calculation
        that combines precision and efficiency.
        """
        degree = self.degree  # There are less calculations by selecting the degree
        if degree == 0:
            if self.coefficients[0] == 0:
                raise Exception("Every number is a root of p.")
            else:
                return []
        elif self.degree == 1:
            b, a = self.coefficients
            return [-b / a]  # a cannot be null
        elif self.degree == 2:
            c, b, a = self.coefficients
            discriminant = b**2 - 4 * a * c
            x1 = (-b - discriminant**(1 / 2)) / (2 * a)  # a cannot be null
            x2 = (-b + discriminant**(1 / 2)) / (2 * a)  # a cannot be null
            return [x1, x2]
        else:
            return self.getRootsByDichotomy(precision)

    def getMultiplicity(self, root):
        """Return the multiplicity of a root."""
        b = self
        n = 0
        while b.coefficients != [1]:
            q, b = b / Polynomial([-root, 1])
            n += 1
        return n

    def getRootsWithMultiplicity(self):
        """Return a list of couples of roots with their multiplicity associated.
        Example: [(r1,m1),(r2,m2),...] """
        return [(r, self.getMultiplicity(r)) for r in list(set(self.roots))]

    def __floordiv__(self, other):
        """Return a rational function of numerator the polynomial, and the denominator the other."""
        return RationalFunction(self, other)

    def show(self):
        """Show the polynomial with grapher."""
        Grapher([self])()  # Instance Grapher only takes the list of the functions in parameter and can be called to display them.

    def matplotlibShow(self, zone=[-5, 5], precision=0.1):
        """Show the polynomial with matplotlib using optional zone and precision."""
        z, Z = zone
        X = list(
            [precision * x for x in range(int(z / precision), int(Z / precision))])
        Y = list([self(x) for x in X])
        plt.plot(X, Y, label="Polynomial")
        plt.show()

    degree = property(getDegree)
    roots = property(getRoots)


class FactoredPolynomial(Polynomial):
    """For factored of a polynomial."""

    def __init__(self, roots_and_multiplicity):
        """Define the factored polynomial with its roots."""
        self.roots = roots

    def __str__(self):
        """Return a string representation of the factored polynomial."""

    def getCoefficients(self):
        """Return the coefficients of the polynomial."""


class RationalFunction:
    """Wikipedia: In algebra, the partial fraction decomposition or partial
    fraction expansion of a rational function (that is, a fraction such that the
    numerator and the denominator are both polynomials) is an operation that
    consists of expressing the fraction as a sum of a polynomial (possibly zero)
    and one or several fractions with a simpler denominator"""

    def __init__(self, p, q):
        """Define a rational function using two polynomials p: the numerator
        and q: the denominator."""
        self.p = p
        self.q = q

    def __str__(self):
        """String representation of a rational function."""
        return "(" + str(self.p) + ")/(" + str(self.q) + ")"

    def __call__(self, x):
        """Evaluate in x the rational function."""
        return self.p(x) / self.q(x)

    def __add__(self, other):
        """Add two rational functions."""
        p = self.p * other.q + other.p * self.q
        q = self.q * other.q
        return RationalFunction(p, q)

    def __sub__(self, other):
        """Substract two rational functions."""
        p = self.p * other.q - other.p * self.q
        q = self.q * other.q
        return RationalFunction(p, q)

    def __mul__(self, other):
        """Multiply two rational functions."""
        p = self.p * other.p
        q = self.q * other.q
        return RationalFunction(p, q)

    def __invert__(self, other):
        """Return the inverse of the rational function. (This operation is optional.)"""
        return RationalFunction(self.q, self.p)

    def __truediv__(self, other):
        """Divide a rational function by another."""
        p = self.p * other.q
        q = self.q * other.p
        return RationalFunction(p, q)

    def getDegree(self):
        """Return the degree of the rational function."""
        return self.p.degree - self.q.degree

    def getPoles(self):
        """Return the poles of the rational function."""
        return self.q.roots

    def getRoots(self):
        """Return the roots of the rational function."""
        return self.p.roots

    def decompose(self):  # Not implemented
        """Return the partial fraction decomposition."""
        # Note this method is supposed to work with complexes
        # So it is not always valid and needs a more general case
        e, r = self.p / self.q
        roots = self.q.getRoots()
        l = [e]
        for (j, xj) in enumerate(roots):
            p = Polynomial([self.p(xj) / self.q.derivative(xj)])
            q = Polynomial([-xj, 1])
            fp = RationalFunction(p, q)
            l.append(fp)
        return l

    def getWholePart(self):  # Not finished
        """Return the whole part of the fraction."""
        e, r = self.p / self.q
        return e

    def getFractionalPart(self):  # Not finished
        """Return the fractional part of the fraction."""
        e, r = self.p / self.q
        return r

    degree = property(getDegree)
    poles = property(getPoles)


class PartialFraction(RationalFunction):  # This is just an idea
    """The only difference with the rational function is that the denominator is
    of the form: [a,b] which corresponds to q=(x-a)**b."""
    # It might not be a good idea.

    def __init__(self, p, q):
        """Define a rational function using two polynomials p: the numerator
        and q: the denominator."""
        self.p = p
        self.q = q


if __name__ == "__main__":
    # suite_random = [random.randint(0,10) for i in range(10)] #Create polynome as big as needed.
    # X=Polynomial(suite_random)
    # t=float128
    suite1 = [3, 2, 4, 5, 1]
    suite2 = [1, -2, 1]
    suite3 = [4, 5]
    A = Polynomial(suite1)
    B = Polynomial(suite2)
    C = Polynomial(suite3)
    FP = RationalFunction(A, B)
    print("A =", A)
    print("B =", B)
    print("C =", C)
    print("A+B =", A + B)
    print("A*B =", A * B)
    print("Derivative of A =", A.derivative())
    print("A/B :", A / B)
    print("A//B:", A // B)
    print("Unit polynomial of C =", C.unit())
    print("HCF (PGCD en francais) of A and B (written A^B) =", A ^ B)
    print("LCM (PPCM en francais) of A and B (written A|B) =", A | B)
    print("Roots of B:", B.roots)
    print("Multiplicity of the root 2 of B:", B.getMultiplicity(2))
    print("Roots with multiplicities of B:", B.getRootsWithMultiplicity())
    #print("Show A on screen:")
    # C=Polynomial.createFromInterpolation([1,2,-4,-6,4],[1,-3,-2,5,-2])
    print(C.coefficients)
    print(FP.decompose())
    # C.show()
