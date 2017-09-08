import os
import time
import exceptions
class TypeError (Exception):
    pass
for f in os.listdir(os.curdir):
    os.utime(f,None)

# 将同目录下所有文件修改时间戳改为当前时间