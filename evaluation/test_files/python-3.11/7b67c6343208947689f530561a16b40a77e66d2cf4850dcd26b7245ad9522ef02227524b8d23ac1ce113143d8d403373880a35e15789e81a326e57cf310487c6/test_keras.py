import os
import sys
from functools import partial
thisfile = os.path.abspath(__file__)
modulepath = os.path.dirname(os.path.dirname(thisfile))
sys.path.insert(0, modulepath)
import numpy as np
import tensorflow as tf
import tensorcircuit as tc
dtype = np.complex128
tfdtype = tf.complex128
ii = np.eye(4, dtype=dtype)
iir = tf.constant(ii.reshape([2, 2, 2, 2]))
zz = np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], dtype=dtype)
zzr = tf.constant(zz.reshape([2, 2, 2, 2]))

def tfi_energy(c, j=1.0, h=-1.0):
    e = 0.0
    n = c._nqubits
    for i in range(n):
        e += h * c.expectation((tc.gates.x(), [i]))
    for i in range(n - 1):
        e += j * c.expectation((tc.gates.z(), [i]), (tc.gates.z(), [(i + 1) % n]))
    return e

def vqe_f2(inputs, xweights, zzweights, nlayers, n):
    c = tc.Circuit(n)
    paramx = tf.cast(xweights, tfdtype)
    paramzz = tf.cast(zzweights, tfdtype)
    for i in range(n):
        c.H(i)
    for j in range(nlayers):
        for i in range(n - 1):
            c.any(i, i + 1, unitary=tf.math.cos(paramzz[j, i]) * iir + tf.math.sin(paramzz[j, i]) * 1j * zzr)
        for i in range(n):
            c.rx(i, theta=paramx[j, i])
    e = tfi_energy(c)
    e = tf.math.real(e)
    return e

def test_vqe_layer2(tfb, highp):
    vqe_fp = partial(vqe_f2, nlayers=3, n=6)
    vqe_layer = tc.KerasLayer(vqe_fp, [(3, 6), (3, 6)])
    inputs = np.zeros([1])
    with tf.GradientTape() as tape:
        e = vqe_layer(inputs)
    print(e, tape.gradient(e, vqe_layer.variables))
    model = tf.keras.Sequential([vqe_layer])
    model.compile(loss=tc.keras.output_asis_loss, optimizer=tf.keras.optimizers.Adam(0.01))
    model.fit(np.zeros([1, 1]), np.zeros([1]), batch_size=1, epochs=300)

def vqe_f(inputs, weights, nlayers, n):
    c = tc.Circuit(n)
    paramc = tf.cast(weights, tfdtype)
    for i in range(n):
        c.H(i)
    for j in range(nlayers):
        for i in range(n - 1):
            c.any(i, i + 1, unitary=tf.math.cos(paramc[2 * j, i]) * iir + tf.math.sin(paramc[2 * j, i]) * 1j * zzr)
        for i in range(n):
            c.rx(i, theta=paramc[2 * j + 1, i])
    e = tfi_energy(c)
    e = tf.math.real(e)
    return e

def test_vqe_layer(tfb, highp):
    vqe_fp = partial(vqe_f, nlayers=6, n=6)
    vqe_layer = tc.keras.QuantumLayer(vqe_fp, (6 * 2, 6))
    inputs = np.zeros([1])
    inputs = tf.constant(inputs)
    model = tf.keras.Sequential([vqe_layer])
    model.compile(loss=tc.keras.output_asis_loss, optimizer=tf.keras.optimizers.Adam(0.01))
    model.fit(np.zeros([2, 1]), np.zeros([2, 1]), batch_size=2, epochs=500)
    np.testing.assert_allclose(model.predict(np.zeros([1])), -7.27, atol=0.05)

def test_function_io(tfb, tmp_path, highp):
    vqe_f_p = partial(vqe_f, inputs=tf.ones([1]))
    vqe_f_p = tf.function(vqe_f_p)
    vqe_f_p(weights=tf.ones([6, 6], dtype=tf.float64), nlayers=3, n=6)
    tc.keras.save_func(vqe_f_p, str(tmp_path))
    loaded = tc.keras.load_func(str(tmp_path), fallback=vqe_f_p)
    print(loaded(weights=tf.ones([6, 6], dtype=tf.float64), nlayers=3, n=6))
    print(loaded(weights=tf.ones([6, 6], dtype=tf.float64), nlayers=3, n=6))

def test_keras_layer_inputs_dict(tfb):
    n = 3
    p = 0.1
    K = tc.backend

    def f(inputs, weights):
        state = inputs['state']
        noise = inputs['noise']
        c = tc.Circuit(n, inputs=state)
        for i in range(n):
            c.rz(i, theta=weights[i])
        for i in range(n):
            c.depolarizing(i, px=p, py=p, pz=p, status=noise[i])
        return K.real(c.expectation_ps(x=[0]))
    layer = tc.KerasLayer(f, [n])
    v = {'state': K.ones([1, 2 ** n]) / 2 ** (n / 2), 'noise': 0.2 * K.ones([1, n])}
    with tf.GradientTape() as tape:
        l = layer(v)
    g1 = tape.gradient(l, layer.trainable_variables)
    v = {'state': K.ones([2 ** n]) / 2 ** (n / 2), 'noise': 0.2 * K.ones([n])}
    with tf.GradientTape() as tape:
        l = layer(v)
    g2 = tape.gradient(l, layer.trainable_variables)
    np.testing.assert_allclose(g1[0], g2[0], atol=1e-05)