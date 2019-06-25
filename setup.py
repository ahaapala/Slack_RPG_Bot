from setuptools import setup

setup(
   name='slack_rpg_bot',
   version='0.0.2',
   description='A slack bot to assiste ttrpgs',
   author='Adam Haapala',
   author_email='adamhaapala@yahoo.com',
   packages=['slack_rpg_bot'],  # Same as name
   install_requires=['slackclient'],  # External packages as dependencies
)
