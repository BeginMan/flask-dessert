## One.

You can simply specify it using the `class_` parameter in the jinja template.

e.g.

	{{ form.email(class_="form-control") }}
	# or dynamically
	{{ form.username(class_="form-style-"+form.username.name) }}


will result in the following HTML::

	<input class="form-control" id="email" name="email" type="text" value="">
	<input class="form-style-username" id="username" name="username" type="text" value="">


[**wtforms rendering-fields**](http://wtforms.readthedocs.org/en/latest/crash_course.html#rendering-fields)

## Two.

If all of your fields should include a class name as well as an ID then just pass in each field's `short_name` to it when you render it:

	<dl>
	{% for field in form %}
		<dt>{{field.label}}</dt>
		<dd>{{field(class_=field.short_name)}}</dd>
	{% endfor %}
	</dl>

or:

	{{ form.name(size=20, class_='input-small') }}


## Three.

Create a [custom widget](http://wtforms.readthedocs.org/en/latest/widgets.html#custom-widgets) mixin that provides the class name:

	from wtforms.fields import StringField
	from wtforms.widgets import TextInput

	class ClassedWidgetMixin(object):
	    """Adds the field's name as a class 
	    when subclassed with any WTForms Field type.

	    Has not been tested - may not work."""
	    def __init__(self, *args, **kwargs):
	        super(ClassedWidgetMixin, self).__init__(*args, **kwargs)

	    def __call__(self, field, **kwargs):
	        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
	        kwargs['class'] = u'%s %s' % (field.short_name, c)
	        return super(ClassedWidgetMixin, self).__call__(field, **kwargs)

	# An example
	class ClassedTextInput(ClassedWidgetMixin, TextInput):
	    pass

	class Company(Form):
	    company_name = StringField('Company Name', widget=ClassedTextInput)

