from django.core.management.base import BaseCommand
from django.core.management.base import no_translations

from notification.models import Project


class Command(BaseCommand):
    help = "Send notifications email to all admins of project passed as first argument"

    def add_arguments(self, parser):
        parser.add_argument(
            "project_id",
            type=int,
            help="BIMData API project's id",
        )

    @no_translations
    def handle(self, *args, **options):
        project_id = options["project_id"]
        project = Project.objects.filter(api_id=project_id).first()
        if not project:
            print(f"Unable to find project with id {project_id}")
            return
