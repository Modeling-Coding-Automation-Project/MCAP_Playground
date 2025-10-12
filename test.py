import os
from helper.SIL.SIL_operator import SIL_Operator

current_dir = os.path.dirname(__file__)
generator = SIL_Operator("my_func.py", current_dir)
generator.build_SIL_code()
