def ROT(s):
	if(ord(s)>ord('Z')):
		if(ord(s)+13 > ord('z')):
			return ord(s)-13
		else:
			return ord(s)+13
	else:
		if(ord(s)+13 > ord('Z')):
			return ord(s)-13
		else:
			return ord(s)+13

def encode(s="Hello"):
	newS = ""
	for i in s:
		newS += chr(ROT(i))
	print newS
encode()