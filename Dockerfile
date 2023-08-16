# This Python package should include most dependencies for our purposes.
FROM python:3.8-bullseye
# Install curl and netcat => Install poetry
RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat gnupg2 unzip \
    && curl -sSL https://install.python-poetry.org | python3 -
# Set PATH enviromental variable to enable bash commands as e.g. '$ poetry version'
ENV PATH="${PATH}:/root/.local/bin"
# robot test chrome & chromedriver etc.
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list &&  apt-get -y update &&  apt-get -y install google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip && unzip chromedriver_linux64.zip
RUN chmod +x chromedriver && cp /chromedriver /usr/local/bin && rm chromedriver_linux64.zip
# Application work directory inside container as per convention:
WORKDIR /usr/src/app
# Copy configuration files for '$ poetry install' before copying the rest of the repository to container for caching purposes
COPY poetry* .
COPY pyproject.toml .
COPY robot-requirements.txt .
# Check poetry installation and that the PATH enviromental variable works properly:
RUN poetry version
# Disable poetry virtual environments, see https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
RUN poetry config virtualenvs.create false
# Install project dependencies utilising poetry as usual. Changes above this line result in a more expensive '$ docker build' operation.
RUN poetry install
# Install robot framework
RUN pip install -r robot-requirements.txt
# Now we can copy the repository files to the container.
COPY . .
# Now, set database env variables, expose the required ports and so forth!
EXPOSE 3000
# Finally, this CMD starts up the application
CMD [ "invoke", "start"]
