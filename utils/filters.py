# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors import CoreAPICompatInspector, NotHandled


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    """
    Add filters in swagger
    """

    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super().get_filter_parameters(filter_backend)
            for param in result:
                if not param.get("description", ""):
                    param.description = "Filter the returned list by {field_name}".format(
                        field_name=param.name
                    )

            return result

        return NotHandled
