import os
import webapp2
import jinja2


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

# class MainPage(webapp2.RequestHandler):
#   def get(self):
#       self.response.headers['Content-Type'] = 'text/plain'
#       self.response.out.write('Hello, Udacity!')

# app = webapp2.WSGIApplication([('/', MainPage)],
#                               debug=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'name': 'a niggerfag',
            'verb': 'extremely enjoy'
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)