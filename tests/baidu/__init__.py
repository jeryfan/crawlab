import os,sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_dir)
sys.path.append(project_dir)