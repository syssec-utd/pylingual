import matplotlib.pyplot as plt

def raise_window():
    wm = plt.get_current_fig_manager()
    wm.canvas.get_tk_widget().focus_force()
    wm.window.lift()