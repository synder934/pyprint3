from flask import Flask, render_template, request, redirect, url_for
from .utils.printer import Printer
from .utils.camera import Camera
import logging


class customFlask(Flask):
    def __init__(
        self,
        import_name,
        static_url_path=None,
        static_folder="static",
        static_host=None,
        host_matching=False,
        subdomain_matching=False,
        template_folder="templates",
        instance_path=None,
        instance_relative_config=False,
        root_path=None,
    ):
        super().__init__(
            import_name,
            static_url_path,
            static_folder,
            static_host,
            host_matching,
            subdomain_matching,
            template_folder,
            instance_path,
            instance_relative_config,
            root_path,
        )
        self.printer = Printer()
        self.camera = Camera()


def create_app():
    app = customFlask(__name__)

    from .routes import main

    app.register_blueprint(main)

    return app
