# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx_rtd_theme
import sys, os, django
sys.path.append(os.path.abspath('../../../encomp/templates/'))
sys.path.insert(0, os.path.abspath('../../../encomp'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'encomp.settings.base'
django.setup()
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Encomp'
copyright = '2022, Andrew Young'
author = 'Andrew Young'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme']
html_static_path=['_static']
templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

add_module_names = False
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': -1,
}
