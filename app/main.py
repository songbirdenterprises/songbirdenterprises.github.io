from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Mail, Message
from flask_sitemap import Sitemap

app = Flask(__name__)
app.secret_key = 'development key'

SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True

ext = Sitemap(app=app)

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'rmccormick314@gmail.com'
app.config["MAIL_PASSWORD"] = 'nwdhuhmdzigotxdy'
mail.init_app(app)

@app.route("/")
def index():
    return render_template("home.html")

@ext.register_generator

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)

    else:
      msg = Message(form.subject.data,
                    sender='contact@songbird.com',
                    recipients=['rmccormick314@gmail.com'])
      msg.body = """
                 From: %s <%s>
                 %s
                 """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template("confirm-contact.html")

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route( '/tos' )
def tos():
    return render_template( '404.html' )

@app.route( '/privacy' )
def privacy():
    return render_template( '404.html' )

@app.route( '/faq' )
def faq():
    return render_template( '404.html' )

@app.errorhandler( 404 )
def not_found( e ):
    return render_template( '404.html' )

@app.route("/sitemap")
@app.route("/sitemap/")
@app.route("/sitemap.xml")
def sitemap():
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """
    from flask import make_response, request, render_template
    import datetime
    from urllib.parse import urlparse

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not str(rule).startswith("/admin") and not str(rule).startswith("/user"):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}"
                }
                static_urls.append(url)

    # Dynamic routes with dynamic content
    dynamic_urls = list()


    xml_sitemap = render_template("sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response

if __name__ == "__main__":
    app.run(debug=True)
