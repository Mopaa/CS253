import os
import webapp2
import jinja2


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir)
								,autoescape = True)

class Handler(webapp2.RequestHandler):

	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))


class Data(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)



class MainPage(Handler):

	def render_front(self, subject="", content="", error=""):
		contents = db.GqlQuery("SELECT * FROM Data ORDER BY created DESC limit 5")
		self.render("front.html", subject=subject, content=content, error=error, contents=contents)

	def get(self):
		self.render_front()

class NewPost(Handler):
	def get(self):
		self.render("newpost.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			post_data = Data(subject = subject, content = content)
			pd_key = post_data.put()
			self.redirect("/%d" % pd_key.id())
		else:
			error = "we need subject and content"
			self.render_front(subject, content, error=error)

class Permalink(MainPage):
	def get(self, blog_id):
		s = Data.get_by_id(int(blog_id))
		for i,j in vars(s).iteritems():
			if i == '_subject':
				sub = j
			elif i == '_content':
				con = j
		self.render("singlepost.html", subject=sub, content=con)

app = webapp2.WSGIApplication([('/', MainPage), ('/newpost', NewPost), ('/(\d+)', Permalink)], debug=True)
