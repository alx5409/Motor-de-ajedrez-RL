from setuptools import setup, find_packages

setup(
    name='chess-rl-engine',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A reinforcement learning based chess engine capable of defeating real players.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'tensorflow',
        'gym',
        'python-chess'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)