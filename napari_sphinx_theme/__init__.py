import os
from pathlib import Path

from .napari_code_theme import *
from sphinx.application import Sphinx
from typing import Dict, Union
from bs4 import BeautifulSoup


try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'not-installed'

def update_templates(app, pagename, templatename, context, doctree):
    """Update template names for page build."""
    template_sections = [
        "theme_navbar_start",
        "theme_navbar_center",
        "theme_navbar_end",
        "theme_footer_items",
        "theme_page_sidebar_items",
        "theme_left_sidebar_end",
        "sidebars",
    ]

    for section in template_sections:
        if context.get(section):
            # Break apart `,` separated strings so we can use , in the defaults
            if isinstance(context.get(section), str):
                context[section] = [
                    ii.strip() for ii in context.get(section).split(",")
                ]

            # Add `.html` to templates with no suffix
            for ii, template in enumerate(context.get(section)):
                if not os.path.splitext(template)[1]:
                    context[section][ii] = template + ".html"

def add_jinja_function(
        app: Sphinx, pagename: str, templatename: str, context: Dict, doctree
) -> None:
    """Add a custom Jinja function to the Sphinx context."""

    def filter_toctree(toctree: str) -> Union[BeautifulSoup, str]:
        """Filter sidebar-nav-bs toctree to remove full API path for objects
        """
        new_toctree = toctree
        soup = BeautifulSoup(toctree, "html.parser")
        # for item in soup:
        #     print(item)
        #     new_toctree.append(item)
            # if '<li class="toctree-l3">' in item:
            #     new_toctree.append(item.split(".")[-1])
            # else:
            #     new_toctree.append(item)
        return toctree

    context["filter_toctree"] = filter_toctree


def set_config_defaults(app):

    try:
        theme = app.builder.theme_options
    except AttributeError:
        theme = None
    if not theme:
        theme = {}

    # Update the HTML theme config
    app.builder.theme_options = theme


def get_html_theme_path():
    """Return list of HTML theme paths."""
    return [str(Path(__file__).parent.parent.resolve())]


# For more details, see:
# https://www.sphinx-doc.org/en/master/development/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
    here = Path(__file__).parent.resolve()
    # Include component templates
    # app.config.templates_path.append(str(here / "components"))
    app.add_html_theme("napari_sphinx_theme", str(here))
    app.connect("builder-inited", set_config_defaults)
    app.connect("html-page-context", update_templates)
    app.connect("html-page-context", add_jinja_function)


    # Include templates for sidebar
    app.config.templates_path.append(str(here / "_templates"))

    return {'version': __version__, 'parallel_read_safe': True}
