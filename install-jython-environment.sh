#!/usr/bin/env sh

JYTHON_URL='http://search.maven.org/remotecontent?filepath=org/python/jython-installer/2.7.1/jython-installer-2.7.1.jar'
JAMA_JAR_URL='http://search.maven.org/remotecontent?filepath=gov/nist/math/jama/1.0.3/jama-1.0.3.jar'

# Install Jama jar
mkdir -p lib
cd lib
wget $JAMA_JAR_URL -O jama-1.0.3.jar
export CLASSPATH=$HOME/lib/jama-1.0.3.jar:$CLASSPATH

# Install Jython
wget $JYTHON_URL -O jython_installer.jar
java -jar jython_installer.jar -s -d $HOME/jython

# Install nose for Jython
# TODO: move to a setup.py
$HOME/jython/bin/pip install nose
$HOME/jython/bin/pip install pytest==3.10.1
$HOME/jython/bin/pip install pytest-xdist
