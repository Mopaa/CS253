import webapp2
import cgi

form = """
<form method="post">
<textarea name="text" style="height: 100px; width: 400px;">
%(txt)s
</textarea>
<br>
<input type="submit">
</form>
"""

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

def encode(s):
	newS = ""
	for i in s:
		newS += chr(ROT(i))
	print newS

def escape_html(s):
    return cgi.escape(s, quote = True)


class MainHandler(webapp2.RequestHandler):
    def writeForm(self,txt="Hello"):
    	self.response.out.write(form % {'txt':txt})
    
    def get(self):
    	self.writeForm()

    def post(self):
    	myText = self.request.get('text')
    	my_text = encode(myText)
    	self.writeForm(my_text)


app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
