FROM openjdk:8-jdk

COPY . sciq-app
WORKDIR /sciq-app
RUN apt-get --quiet update --yes
RUN apt-get --quiet install --yes wget tar unzip lib32stdc++6 lib32z1
RUN wget --quiet --output-document=android-sdk.zip https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip
RUN unzip -d android-sdk-linux android-sdk.zip
RUN echo y | android-sdk-linux/tools/bin/sdkmanager "platforms;android-29" >/dev/null
RUN echo y | android-sdk-linux/tools/bin/sdkmanager "platform-tools" >/dev/null
RUN echo y | android-sdk-linux/tools/bin/sdkmanager "build-tools;29.0.2" >/dev/null
RUN export ANDROID_HOME=$PWD/android-sdk-linux
RUN export PATH=$PATH:$PWD/android-sdk-linux/platform-tools/
RUN yes | android-sdk-linux/tools/bin/sdkmanager --licenses
RUN sed -i "s@sdk.dir=.*@sdk.dir=$ANDROID_HOME@1" app/local.properties
RUN cp app/local.properties .
RUN chmod +x ./gradlew
RUN ./gradlew clean
RUN ./gradlew build
RUN ./gradlew assembleDebug
RUN ls -al app/build/outputs