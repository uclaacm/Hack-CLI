from setuptools import setup

setup(name = "acm",
	url = "http://hackucla.com",
	version = "1.0.0",
	description = "ACM Hack CLI",
	author = "Nikhil Kansal",
	author_email = "nkansal@hackucla.com",
	packages = ['acm'],
	install_requires = ['requests'],
	entry_points = {
		'console_scripts' : [
			'acm=acm.main:main'
		]
	}
)
