from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
        )
        parser.add_argument(
            "--password",
            type=str,
        )
        parser.add_argument(
            "--email",
            type=str,
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        password = kwargs["password"]
        email = kwargs["email"]

        if not username:
            username = "admin"

        if not password:
            password = "admin1234"

        if not email:
            email = f"{username}@example.com"

        if User.objects.filter(username=username).first():
            raise CommandError(f"Username `{username}` already taken.")

        if User.objects.filter(email=email).first():
            raise CommandError(f"Email `{email}` already taken.")

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
            user_type="Administrador",
        )

        self.stdout.write(
            self.style.SUCCESS(f"Admin `{username}` successfully created!"),
        )
