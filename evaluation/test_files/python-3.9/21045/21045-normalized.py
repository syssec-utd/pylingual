def loop_qt4(kernel):
    """Start a kernel with PyQt4 event loop integration."""
    from IPython.external.qt_for_kernel import QtCore
    from IPython.lib.guisupport import get_app_qt4, start_event_loop_qt4
    kernel.app = get_app_qt4([' '])
    kernel.app.setQuitOnLastWindowClosed(False)
    kernel.timer = QtCore.QTimer()
    kernel.timer.timeout.connect(kernel.do_one_iteration)
    kernel.timer.start(1000 * kernel._poll_interval)
    start_event_loop_qt4(kernel.app)