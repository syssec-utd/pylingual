import math

class math_fuction:

    def inch_change_cm(inch):
        cm = inch * 2.54
        return cm

    def cir_area(radius):
        return radius * radius * math.pi()

    def cir_circum(radius):
        return 2 * math.pi() * radius

    def gcd(x, y):
        if x > y:
            small = y
        else:
            small = x
        for i in range(1, small + 1):
            if x % i == 0 and y % i == 0:
                result = i
        return result