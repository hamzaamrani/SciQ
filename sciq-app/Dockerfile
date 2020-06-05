FROM openjdk:8-jdk

COPY . sciq-app
WORKDIR /sciq-app
RUN apt-get --quiet update --yes
RUN apt-get --quiet install --yes wget tar unzip lib32stdc++6 lib32z1
RUN wget --quiet --output-document=cmdline-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip
RUN unzip -d cmdline-tools cmdline-tools.zip
RUN echo y | cmdline-tools/tools/bin/sdkmanager "platforms;android-29" >/dev/null
RUN echo y | cmdline-tools/tools/bin/sdkmanager "platform-tools" >/dev/null
RUN echo y | cmdline-tools/tools/bin/sdkmanager "build-tools;29.0.2" >/dev/null
RUN export ANDROID_HOME=$PWD/cmdline-tools
RUN export PATH=$PATH:$PWD/cmdline-tools/platform-tools/
RUN yes | cmdline-tools/tools/bin/sdkmanager --licenses
RUN sed -i "s@sdk.dir=.*@sdk.dir=$ANDROID_HOME@1" app/local.properties
RUN cp app/local.properties .
RUN chmod +x ./gradlew
RUN ./gradlew clean
RUN ./gradlew build
RUN ./gradlew assembleDebug
RUN ls -al app/build/outputs