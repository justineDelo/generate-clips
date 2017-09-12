import argparse

parser = argparse.ArgumentParser()

parser.add_argument("a")
parser.add_argument("b", nargs='?', default="0")
parser.add_argument("c", nargs='?', default="0")
args = parser.parse_args()

print (args.a)
print (args.b)
print(int(args.a))
print(int(args.b))
print(int(args.c))
if int(args.b)==1 :
	print("oui")
