import re
from django.contrib import messages


class Util:
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    @staticmethod
    def convert(name):
        s1 = Util.first_cap_re.sub(r'\1_\2', name)
        return Util.all_cap_re.sub(r'\1_\2', s1).lower()

    @staticmethod
    def form_validation_error(request, form):
        error = dict()
        for key in form.errors.as_data():
            if key != '__all__':
                error[key] = form.errors.as_data()[key][0].message
            else:
                messages.error(request, form.errors.as_data()[key][0].message)
        return error
