# Base image
FROM ubuntu

# Update debian packages
RUN apt-get update

# Install python
RUN apt-get install -y python3.9

# Install pip package manager
RUN apt-get install -y python3-pip

# Install git
RUN apt-get install -y git

# Install required packages and dependencies
RUN pip install paho-mqtt \
	pandas \
	scikit-learn \
	matplotlib \ 
	seaborn \
	boto3 \ 
	serial

# Clone application code from the remote repository on GitHub
RUN git clone https://github.com/HassanMahmoodKhan/Remote-Health-Monitoring.git /opt/

# Open a bash terminal
CMD ["/bin/bash"]
