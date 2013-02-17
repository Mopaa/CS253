import webapp2
import cgi, re

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


signup = """
<h2>Signup</h2>
<form method="post">
	<label> Username:
		<input type="text" name="username" value="%(user)s">
		<div>%(e_one)s</div>
	</label>
	<br>
	<label> Password:
		<input type="password" name="f_pass" value="%(f_pass)s">
		<div>%(e_two)s</div>
	</label>
	<br>
	<label> Verify Password:
		<input type="password" name="v_pass" value="%(v_pass)s">
		<div>%(e_two)s</div>
	</label>
	<br>
	<label> Email (Optional):
		<input type="text" name="email" value="%(email)s">
		<div>%(e_tre)s</div>
	</label>
	<br>
	<input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)


class MainPage(webapp2.RequestHandler):
    def writeForm(self,txt="Hello"):
    	self.response.out.write(form % {'txt':escape_html(txt)})
    
    def get(self):
    	self.writeForm()

    def post(self):
    	text = self.request.get('text')
    	
    	self.writeForm(text.encode('rot13'))

class UserVal(webapp2.RequestHandler):
	def write_form(self,user="",f_pass="",v_pass="",email="", e_one="", e_two="",e_tre=""):
		self.response.out.write(signup % 
		{
			"user":user,
			"f_pass":f_pass,
			"v_pass":v_pass,
			"email":email,
			"e_one":e_one,
			"e_two":e_two,
			"e_tre":e_tre
		})

	def get(self):
		self.write_form()

	def post(self):
		e1=""
		e2=""
		e3=""
		user=self.request.get("username")
		f_pass=self.request.get("f_pass")
		v_pass=self.request.get("v_pass")
		email=self.request.get("email")
		#self.response.out.write(valid_username(user))
		if not valid_username(user):
			e1="error!"
		
		if(f_pass!=v_pass):
			e2="error!"

		if not valid_username(user) or f_pass!=v_pass:
			self.write_form(user,"","",email,e1,e2,e3)
		else:
			self.redirect('/confirm?q='+user)
			

class Confirm(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks, "+self.request.get('q'))

app = webapp2.WSGIApplication([('/', MainPage),
								('/userval', UserVal),
								('/confirm', Confirm)], 
								debug=True)