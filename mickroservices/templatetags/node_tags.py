from sushi_app.models import Directory, UserProfile

from django import template

register = template.Library()

@register.inclusion_tag('directories.html', takes_context=True)
def make_node(context):
	request = context["request"]
	user = UserProfile.objects.get(user=request.user)
	print(user.is_manager)
	return{'node': Directory.objects.get(parent=None), 'user': user}
