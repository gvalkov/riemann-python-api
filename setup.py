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
    'Operating System :: POSIX :: Linux',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: BSD License',
]

kw = {
    'name':                 'riemann-api',
    'version':              '1.0.0',

    'description':          'TBD',
    'long_description':     open('README.rst').read(),

    'author':               'Georgi Valkov',
    'author_email':         'georgi.t.valkov@gmail.com',
    'license':              'Revised BSD License',
    'keywords':             'evdev input uinput',
    'url':                  'https://github.com/gvalkov/riemann-api',
    'classifiers':          classifiers,

    'install_requires':     install_requires,
    'packages':             find_packages(),
    'zip_safe':             True,
}


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    setup(**kw)
