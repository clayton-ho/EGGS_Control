#!/bin/sh
#/*--------------------------------------------------------------------------
# *  Copyright 2012 Taro L. Saito
# *
# *  Licensed under the Apache License, Version 2.0 (the "License");
# *  you may not use this file except in compliance with the License.
# *  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# *  Unless required by applicable law or agreed to in writing, software
# *  distributed under the License is distributed on an "AS IS" BASIS,
# *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *  See the License for the specific language governing permissions and
# *  limitations under the License.
# *--------------------------------------------------------------------------*/

if [ -z "$PROG_HOME" ] ; then
  ## resolve links - $0 may be a link to PROG_HOME
  PRG="$0"

  # need this for relative symlinks
  while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \(.*\)$'`
    if expr "$link" : '/.*' > /dev/null; then
      PRG="$link"
    else
      PRG="`dirname "$PRG"`/$link"
    fi
  done

  saveddir=`pwd`

  PROG_HOME=`dirname "$PRG"`/..

  # make it fully qualified
  PROG_HOME=`cd "$PROG_HOME" && pwd`

  cd "$saveddir"
fi


cygwin=false
mingw=false
darwin=false
case "`uname`" in
  CYGWIN*) cygwin=true
          ;;
  MINGW*) mingw=true
          ;;
  Darwin*) darwin=true
           if [ -z "$JAVA_VERSION" ] ; then
             JAVA_VERSION="CurrentJDK"
           else
            echo "Using Java version: $JAVA_VERSION" 1>&2
           fi
           if [ -z "$JAVA_HOME" ] ; then
             JAVA_HOME=/System/Library/Frameworks/JavaVM.framework/Versions/${JAVA_VERSION}/Home
           fi
           JVM_OPT="$JVM_OPT -Xdock:name=${PROG_NAME} -Xdock:icon=$PROG_HOME/icon-mac.png -Dapple.laf.useScreenMenuBar=true"
           JAVACMD="`which java`"
           ;;
esac

# Resolve JAVA_HOME from javac command path
if [ -z "$JAVA_HOME" ]; then
  javaExecutable="`which javac`"
  if [ -n "$javaExecutable" -a ! "`expr \"$javaExecutable\" : '\([^ ]*\)'`" = "no" ]; then
    # readlink(1) is not available as standard on Solaris 10.
    readLink=`which readlink`
    if [ ! `expr "$readLink" : '\([^ ]*\)'` = "no" ]; then
      javaExecutable="`readlink -f \"$javaExecutable\"`"
      javaHome="`dirname \"$javaExecutable\"`"
      javaHome=`expr "$javaHome" : '\(.*\)/bin'`
      JAVA_HOME="$javaHome"
      export JAVA_HOME
    fi
  fi
fi


if [ -z "$JAVACMD" ] ; then
  if [ -n "$JAVA_HOME"  ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
      # IBM's JDK on AIX uses strange locations for the executables
      JAVACMD="$JAVA_HOME/jre/sh/java"
    else
      JAVACMD="$JAVA_HOME/bin/java"
    fi
  else
    JAVACMD="`which java`"
  fi
fi

if [ ! -x "$JAVACMD" ] ; then
  echo "Error: JAVA_HOME is not defined correctly."
  echo "  We cannot execute $JAVACMD"
  exit 1
fi

if [ -z "$JAVA_HOME" ] ; then
  echo "Warning: JAVA_HOME environment variable is not set."
fi

CLASSPATH_SUFFIX=""
# Path separator used in EXTRA_CLASSPATH
PSEP=":"

# For Cygwin, switch paths to Windows-mixed format before running java
if $cygwin; then
  [ -n "$PROG_HOME" ] &&
    PROG_HOME=`cygpath -am "$PROG_HOME"`
  [ -n "$JAVA_HOME" ] &&
    JAVA_HOME=`cygpath -am "$JAVA_HOME"`
  CLASSPATH_SUFFIX=";"
  PSEP=";"
fi

# For Migwn, ensure paths are in UNIX format before anything is touched
if $mingw ; then
  [ -n "$PROG_HOME" ] &&
    PROG_HOME="`(cd "$PROG_HOME"; pwd)`"
  [ -n "$JAVA_HOME" ] &&
    JAVA_HOME="`(cd "$JAVA_HOME"; pwd)`"
  CLASSPATH_SUFFIX=";"
  PSEP=";"
fi


PROG_NAME=labrad-web
PROG_VERSION=2.0.6
echo $JVM_OPT
exec "$JAVACMD" \
     ${JVM_OPT} \
      \
     -cp "${PROG_HOME}/bin/lib/*${CLASSPATH_SUFFIX}" \
     -Dprog.home="${PROG_HOME}" \
     -Dprog.version="${PROG_VERSION}" \
     org.labrad.browser.WebServer "$@"
