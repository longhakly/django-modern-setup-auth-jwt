import os
from django.conf import settings
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def __init__(self):
        super().__init__()

    def handle(self, **options):
        app_name = options.pop("name")
        target = options.pop("directory") or os.path.join(os.getcwd(), "apps", app_name)
        os.makedirs(target, exist_ok=True)
        super().handle("app", app_name, target, **options)
        self._add_default_file(target)
        self._remove_unused_file(target)
        self._re_write_app_name(app_name, target)
        self._add_app_to_local_apps(app_name)

        self.stdout.write(
            self.style.SUCCESS(f'App "apps/{app_name}" created successfully!')
        )

    @staticmethod
    def _add_default_file(target):
        default_files = [
            "serializers.py",
            "mixins.py",
            "constants.py",
            "signals.py",
            "urls.py",
            "services.py",
            "utils.py",
        ]
        for file in default_files:
            file_path = os.path.join(target, file)

            with open(file_path, "w") as f:
                pass

    @staticmethod
    def _remove_unused_file(target):
        files_to_remove = ["admin.py"]
        for file_name in files_to_remove:
            file_path = os.path.join(target, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

    def _re_write_app_name(self, app_name, target):
        apps_file_path = f"{target}/apps.py"
        try:
            with open(apps_file_path, "r+") as file:
                content = file.read()
                content = content.replace(
                    f'name = "{app_name}"', f'name = "apps.{app_name}"'
                )
                file.seek(0)
                file.write(content)
                file.truncate()
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f"apps.py not found in {apps_file_path}")
            )

    def _add_app_to_local_apps(self, app_name):
        try:

            class_app_name = "".join(word.capitalize() for word in app_name.split("_"))
            class_app_name += "Config"
            settings_path = os.path.join(
                settings.BASE_DIR, "config", "django", "base.py"
            )
            app_config = f"    'apps.{app_name}.apps.{class_app_name}',\n"
            with open(settings_path, "r+") as file:
                content = file.readlines()
                local_apps_line_index = -1
                for i, line in enumerate(content):
                    if line.strip().startswith("LOCAL_APPS = ["):
                        local_apps_line_index = i
                        break
                if local_apps_line_index >= 0:
                    # Find the closing bracket of the LOCAL_APPS list
                    for i in range(local_apps_line_index + 1, len(content)):
                        if "]" in content[i]:
                            content.insert(i, app_config)
                            break
                    file.seek(0)
                    file.writelines(content)
                    file.truncate()
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            "LOCAL_APPS not found in base.py. Please add the app manually."
                        )
                    )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "base.py not found. Please add the app manually to your settings."
                )
            )
