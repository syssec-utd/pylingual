def _first_glimpse_sensor(self, x_t):
    """
        Compute first glimpse position using down-sampled image.
        """
    downsampled_img = theano.tensor.signal.downsample.max_pool_2d(x_t, (4, 4))
    downsampled_img = downsampled_img.flatten()
    first_l = T.dot(downsampled_img, self.W_f)
    if self.disable_reinforce:
        wf_grad = self.W_f
        if self.random_glimpse:
            first_l = self.srng.uniform((2,), low=-1.7, high=1.7)
    else:
        sampled_l_t = self._sample_gaussian(first_l, self.cov)
        sampled_pdf = self._multi_gaussian_pdf(disconnected_grad(sampled_l_t), first_l)
        wf_grad = T.grad(T.log(sampled_pdf), self.W_f)
        first_l = sampled_l_t
    return (first_l, wf_grad)