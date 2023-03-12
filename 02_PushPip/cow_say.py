import cowsay
import argparse

def process_cowfile(args):
    if "/" in args.cowfile or args.cowfile[-4:] == ".cow":
        cow = "default"
        with open(args.cowfile) as file:
            cowfile = cowsay.read_dot_cow(file)
    else:
        cow = args.cowfile
        cowfile = None
    return cow, cowfile

parser = argparse.ArgumentParser()
parser.add_argument("-e", dest="eyes", default="oo", type=str)
parser.add_argument("-f", dest="cowfile", action="store", default="default", type=str)
parser.add_argument("-l", dest="list", action="store_true")
parser.add_argument("-n", dest="wrap_text", action="store_false")
parser.add_argument("-T", dest="tongue", default="  ", type=str)
parser.add_argument("-W", dest="width", type=int, default=40)
parser.add_argument("-b", dest="preset", action="append_const", const="b", default=[""])
parser.add_argument("-d", dest="preset", action="append_const", const="d", default=[""])
parser.add_argument("-g", dest="preset", action="append_const", const="g", default=[""])
parser.add_argument("-p", dest="preset", action="append_const", const="p", default=[""])
parser.add_argument("-s", dest="preset", action="append_const", const="s", default=[""])
parser.add_argument("-t", dest="preset", action="append_const", const="t", default=[""])
parser.add_argument("-w", dest="preset", action="append_const", const="w", default=[""])
parser.add_argument("-y", dest="preset", action="append_const", const="y", default=[""])
parser.add_argument("message", action="store", type=str, nargs='?', default="")

args = parser.parse_args()

args.eyes = args.eyes[:2]
args.tongue = args.tongue[:2]
args.cow, args.cowfile = process_cowfile(args)

if args.list:
    print(cowsay.list_cows())
else:
    print(cowsay.cowsay(args.message, cow=args.cow, preset=max(args.preset), eyes=args.eyes, tongue=args.tongue, width=args.width, wrap_text=True, cowfile=args.cowfile))