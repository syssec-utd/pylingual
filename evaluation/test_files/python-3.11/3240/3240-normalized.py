def then(self, success=None, failure=None):
    """
        This method takes two optional arguments.  The first argument
        is used if the "self promise" is fulfilled and the other is
        used if the "self promise" is rejected.  In either case, this
        method returns another promise that effectively represents
        the result of either the first of the second argument (in the
        case that the "self promise" is fulfilled or rejected,
        respectively).

        Each argument can be either:
          * None - Meaning no action is taken
          * A function - which will be called with either the value
                of the "self promise" or the reason for rejection of
                the "self promise".  The function may return:
                * A value - which will be used to fulfill the promise
                  returned by this method.
                * A promise - which, when fulfilled or rejected, will
                  cascade its value or reason to the promise returned
                  by this method.
          * A value - which will be assigned as either the value
                or the reason for the promise returned by this method
                when the "self promise" is either fulfilled or rejected,
                respectively.

        :type success: (object) -> object
        :type failure: (object) -> object
        :rtype : Promise
        """
    ret = self.create_next()

    def callAndFulfill(v):
        """
            A callback to be invoked if the "self promise"
            is fulfilled.
            """
        try:
            if aplus._isFunction(success):
                ret.fulfill(success(v))
            else:
                ret.fulfill(v)
        except Exception as e:
            Promise.last_exc_info = sys.exc_info()
            e.exc_info = sys.exc_info()
            ret.reject(e)

    def callAndReject(r):
        """
            A callback to be invoked if the "self promise"
            is rejected.
            """
        try:
            if aplus._isFunction(failure):
                ret.fulfill(failure(r))
            else:
                ret.reject(r)
        except Exception as e:
            Promise.last_exc_info = sys.exc_info()
            e.exc_info = sys.exc_info()
            ret.reject(e)
    self.done(callAndFulfill, callAndReject)
    return ret