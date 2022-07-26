import os
import os.path
import argparse

def main(arg):
	img_list = []
	img_list += arg.get('FILE')
	for img_p in img_list:
		try:
			open(img_p, "r")
			print("\nFILE				: " + img_p + "\n")
			print("EXIF metadata:\n")
			os.system("exiftool " + img_p)
			print("\n//---------------------------------")
		except: 
			print("Failed to open " + img_p + ".")

def parse():
	parser = argparse.ArgumentParser(
		prog = 'python3 scorpion.py', 
		description = 'Display image metadata'
	)
	parser.add_argument('FILE', nargs='*')
	args = parser.parse_args()
	return args.__dict__

if __name__ == "__main__":
	arg = parse()
	main(arg)