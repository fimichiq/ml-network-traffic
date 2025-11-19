# ===========================
# Stage 1: Build CICFlowMeter (Java/Gradle)
# ===========================
FROM openjdk:8-jdk AS builder
WORKDIR /app

# Copy Gradle wrapper and build files
COPY java/gradlew java/build.gradle java/settings.gradle /app/
COPY java/gradle /app/gradle

# Copy source code and dependencies
COPY java/src /app/src
COPY java/jnetpcap /app/jnetpcap

RUN chmod +x ./gradlew

# Install Maven for jnetpcap installation
RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*

# Install jnetpcap in the local Maven repository
RUN mvn install:install-file \
    -Dfile=/app/jnetpcap/linux/jnetpcap-1.4.r1425/jnetpcap.jar \
    -DgroupId=org.jnetpcap \
    -DartifactId=jnetpcap \
    -Dversion=1.4.1 \
    -Dpackaging=jar

# Build the CICFlowMeter application
RUN ./gradlew build
RUN ./gradlew distZip && \
    cd build/distributions && \
    jar xf *.zip && \
    chmod +x CICFlowMeter-4.0/bin/cfm


# ===========================
# Stage 2: Runtime (Python server + CICFlowMeter)
# ===========================
FROM eclipse-temurin:8-jre
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY python/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy built CICFlowMeter from builder stage (already extracted)
COPY --from=builder /app/build/distributions/CICFlowMeter-4.0 /app/CICFlowMeter-4.0
COPY --from=builder /app/jnetpcap /app/jnetpcap

# Set up jnetpcap library path
ENV LD_LIBRARY_PATH=/app/jnetpcap/linux/jnetpcap-1.4.r1425
ENV JAVA_OPTS="-Djava.library.path=/app/jnetpcap/linux/jnetpcap-1.4.r1425"

# Copy Python server
COPY python/server.py /app/server.py

# Expose port
EXPOSE 6000

# Run the Python HTTP server
CMD ["python3", "/app/server.py"]

