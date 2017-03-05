from django.views.generic.base import TemplateView
from rest_framework_docs.api_docs import ApiDocumentation


class DRFDocsView(TemplateView):

    template_name = "rest_framework_docs/custom.html"

    def get_context_data(self, **kwargs):
        context = super(DRFDocsView, self).get_context_data(**kwargs)
        docs = ApiDocumentation()
        endpoints = docs.get_endpoints()

        query = self.request.GET.get("search", "")
        if query and endpoints:
            endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]

        context['query'] = query
        context['endpoints'] = endpoints
        return context