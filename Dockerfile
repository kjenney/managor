FROM python:3.8

# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh
RUN mv /root/.pulumi/bin/pulumi /usr/local/bin/

# Install Dependencies
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install module
COPY . /usr/src/app
RUN pip install --no-cache-dir ./
