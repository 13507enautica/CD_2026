class Complexo:
    def __init__(self, real=0, imaginary=0):
        self.real = real
        self.imaginary = imaginary

    def __str__(self):
        if self.imaginary != 0:
            return f"{self.real} + {self.imaginary}i"
        else:
            return f"{self.real}"

    def getReal(self):
        return self.real

    def getImaginary(self):
        return self.imaginary

    def addTo(self, number: Complexo) -> Complexo:
        return Complexo(self.real + number.getReal(), self.imaginary + number.getImaginary())

    def subtractTo(self, number: Complexo) -> Complexo:
        return Complexo(self.real - number.getReal(), self.imaginary - number.getImaginary())

    def multiplyBy(self, number: Complexo) -> Complexo:
        return Complexo((self.real*number.getReal() - self.imaginary*number.getImaginary()), (self.real*number.getImaginary() + self.imaginary*number.getReal()))