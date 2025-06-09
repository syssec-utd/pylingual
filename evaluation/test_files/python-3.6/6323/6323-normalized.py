def wrap2cylinder(script, radius=1, pitch=0, taper=0, pitch_func=None, taper_func=None):
    """Deform mesh around cylinder of radius and axis z

    y = 0 will be on the surface of radius "radius"
    pitch != 0 will create a helix, with distance "pitch" traveled in z for each rotation
    taper = change in r over z. E.g. a value of 0.5 will shrink r by 0.5 for every z length of 1

    """
    "vert_function(s=s, x='(%s+y-taper)*sin(x/(%s+y))' % (radius, radius),\n                     y='(%s+y)*cos(x/(%s+y))' % (radius, radius),\n                     z='z-%s*x/(2*%s*(%s+y))' % (pitch, pi, radius))"
    if pitch_func is None:
        pitch_func = '-(pitch)*x/(2*pi*(radius))'
    pitch_func = pitch_func.replace('pitch', str(pitch)).replace('pi', str(math.pi)).replace('radius', str(radius))
    if taper_func is None:
        taper_func = '-(taper)*(pitch_func)'
    taper_func = taper_func.replace('taper', str(taper)).replace('pitch_func', str(pitch_func)).replace('pi', str(math.pi))
    x_func = '(y+(radius)+(taper_func))*sin(x/(radius))'.replace('radius', str(radius)).replace('taper_func', str(taper_func))
    y_func = '(y+(radius)+(taper_func))*cos(x/(radius))'.replace('radius', str(radius)).replace('taper_func', str(taper_func))
    z_func = 'z+(pitch_func)'.replace('pitch_func', str(pitch_func))
    vert_function(script, x_func, y_func, z_func)
    return None