import random

def main():
	outfile = open('test.txt', 'w')

	for count in range(5000):

		num = random.randint(-9, 9)

		outfile.write(str(num) + " ")

main()