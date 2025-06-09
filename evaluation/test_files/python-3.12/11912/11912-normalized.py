def _getJacobian(self, phi, theta):
    """
        Calculates the Jacobian for the transformation of the position errors and proper motion errors
        between coordinate systems. This Jacobian is also the rotation matrix for the transformation of
        proper motions. See section 1.5.3 of the Hipparcos Explanatory Volume 1 (equation 1.5.20). This
        matrix has the following form:

            |  c  s |
        J = |       |
            | -s  c |

        Parameters
        ----------

        phi       - The longitude-like angle of the position of the source (radians).
        theta     - The latitude-like angle of the position of the source (radians).

        Returns
        -------

        c, s - The Jacobian matrix elements c and s corresponding to (phi, theta) and the currently
               desired coordinate system transformation.
        """
    p, q, r = normalTriad(phi, theta)
    zRot = self.rotationMatrix[2, :]
    if p.ndim == 2:
        zRotAll = tile(zRot, p.shape[1]).reshape(p.shape[1], 3)
        pRot = cross(zRotAll, r.T)
        normPRot = norm(pRot, axis=1)
        for i in range(pRot.shape[0]):
            pRot[i] = pRot[i] / normPRot[i]
        c = zeros(pRot.shape[0])
        s = zeros(pRot.shape[0])
        for i in range(pRot.shape[0]):
            c[i] = dot(pRot[i], p.T[i])
            s[i] = dot(pRot[i], q.T[i])
        return (c, s)
    else:
        pRot = cross(zRot, r.T)
        pRot = pRot / norm(pRot)
        return (dot(pRot, p), dot(pRot, q))