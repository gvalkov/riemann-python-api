from setuptools import setup, find_packages


install_requires = [
    'protobuf>=3.0.0b2,<4.0.0'
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Intended Audience :: Developers',
    'License :: OSI Approved',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: System :: Networking',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Systems Administration'
]

kw = {
    'name':                 'riemann-api',
    'version':              '1.0.0',

    'description':          'Client for the Riemann event stream processor',
    'long_description':     open('README.rst').read(),

    'author':               'Georgi Valkov',
    'author_email':         'georgi.t.valkov@gmail.com',
    'license':              'MIT',
    'keywords':             'riemann',
    'url':                  'https://github.com/gvalkov/riemann-api',
    'classifiers':          classifiers,

    'install_requires':     install_requires,
    'packages':             find_packages(),
    'zip_safe':             True,
}


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    setup(**kw)
