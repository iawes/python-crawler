import os
import re

name = 'DRG/DIP概念'
print(name)

name2 = re.sub('([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u007a])', '', name)
print(name2)