import sys
import os

sys.path.append(os.path.abspath('..', ))
sys.path.insert(0, os.path.abspath('../'))
sys.path.append(os.path.join(os.getcwd(), "..", ".."))

project = 'Telegram_bot'
copyright = '2024, Skopenko'
author = 'Skopenko'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']
