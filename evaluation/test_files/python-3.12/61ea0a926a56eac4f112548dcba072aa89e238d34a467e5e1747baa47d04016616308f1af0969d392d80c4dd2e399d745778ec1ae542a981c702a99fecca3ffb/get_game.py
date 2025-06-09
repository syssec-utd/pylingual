import win32gui

def get_game() -> dict:
    """
    注意，我们会获取所有1000*600的MacromediaFlashPlayerActiveX类子窗口句柄
    对于这些窗口是否能够成功截图或模拟操作，应该由您自己来确认
    因此，我们建议您使用流行的登陆器来执行游戏脚本
    """
    parent_hwnd_list, games = ([], {})
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), parent_hwnd_list)
    for parent_hwnd in parent_hwnd_list:
        if win32gui.IsWindowVisible(parent_hwnd):
            child_hwnd_list = []
            win32gui.EnumChildWindows(parent_hwnd, lambda hwnd, param: param.append(hwnd), child_hwnd_list)
            for child_hwnd in child_hwnd_list:
                class_name = win32gui.GetClassName(child_hwnd)
                if class_name == 'MacromediaFlashPlayerActiveX':
                    shape = win32gui.GetWindowRect(child_hwnd)
                    height = shape[3] - shape[1]
                    weight = shape[2] - shape[0]
                    if weight == 1000 and height == 600:
                        games[win32gui.GetWindowText(parent_hwnd)] = child_hwnd
    return games