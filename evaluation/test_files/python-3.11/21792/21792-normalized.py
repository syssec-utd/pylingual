def timed(limit):
    """Test must finish within specified time limit to pass.

    Example use::

      @timed(.1)
      def test_that_fails():
          time.sleep(.2)
    """

    def decorate(func):

        def newfunc(*arg, **kw):
            start = time.time()
            func(*arg, **kw)
            end = time.time()
            if end - start > limit:
                raise TimeExpired('Time limit (%s) exceeded' % limit)
        newfunc = make_decorator(func)(newfunc)
        return newfunc
    return decorate