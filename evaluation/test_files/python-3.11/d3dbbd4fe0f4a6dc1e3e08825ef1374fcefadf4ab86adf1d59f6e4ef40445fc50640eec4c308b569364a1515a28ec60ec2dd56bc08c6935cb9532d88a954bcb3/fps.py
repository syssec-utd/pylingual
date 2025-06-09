import cv2
'\n計算及更改執行效率\n'

def get_fps(function):
    time1 = cv2.getTickCount()
    function()
    time2 = cv2.getTickCount()
    return (time2 - time1) / cv2.getTickFrequency()
'\nMany of the OpenCV functions are optimized using SSE2, AVX etc. \nIt contains unoptimized code also.\nSo if our system support these features, we should exploit them (almost all modern day processors support them).\nIt is enabled by default while compiling. So OpenCV runs the optimized code if it is enabled, else it runs the unoptimized code.\nYou can use cv2.useOptimized() to check if it is enabled/disabled and cv2.setUseOptimized() to enable/disable it.\nLet’s see a simple example.\n'

def set_optimized():
    cv2.setUseOptimized(not cv2.useOptimized())