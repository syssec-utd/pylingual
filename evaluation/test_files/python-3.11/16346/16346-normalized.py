def cubic(a, b, c, d=None):
    """ x^3 + ax^2 + bx + c = 0  (or ax^3 + bx^2 + cx + d = 0)
    With substitution x = y-t and t = a/3, the cubic equation reduces to
        y^3 + py + q = 0,
    where p = b-3t^2 and q = c-bt+2t^3.  Then, one real root y1 = u+v can
    be determined by solving
        w^2 + qw - (p/3)^3 = 0
    where w = u^3, v^3.  From Vieta's theorem,
        y1 + y2 + y3 = 0
        y1 y2 + y1 y3 + y2 y3 = p
        y1 y2 y3 = -q,
    the other two (real or complex) roots can be obtained by solving
        y^2 + (y1)y + (p+y1^2) = 0

    """
    if d:
        a, b, c = (b / float(a), c / float(a), d / float(a))
    t = a / 3.0
    p, q = (b - 3 * t ** 2, c - b * t + 2 * t ** 3)
    u, v = quadratic(q, -(p / 3.0) ** 3)
    if type(u) == type(0j):
        r, w = polar(u.real, u.imag)
        y1 = 2 * cbrt(r) * cos(w / 3.0)
    else:
        y1 = cbrt(u) + cbrt(v)
    y2, y3 = quadratic(y1, p + y1 ** 2)
    return (y1 - t, y2 - t, y3 - t)