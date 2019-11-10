from django.views.generic import TemplateView


# content/templates/main/index.html
class IndexPageView(TemplateView):
	template_name = 'main/index.html'
