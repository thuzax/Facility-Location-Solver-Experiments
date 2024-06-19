import sys
from main import run

def solve_relaxation(args):
    run(args, True)
if __name__=="__main__":
    solve_relaxation(sys.argv[1:])
    