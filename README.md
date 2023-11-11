# FairTicketonChain

FairTicketonChain is an innovative Anti-Scalping Booking System designed to combat ticket scalping, leveraging Cloud and Distributed Computing technologies for enhanced scalability and performance.

## Introduction

Ticket scalping remains a prevalent issue, impacting consumers and event organizers alike. Current solutions often fall short in providing real-time and comprehensive anti-scalping measures. In response to these challenges, our Anti-Scalping Booking System is designed to revolutionize ticket sales by combining anti-scalping knowledge with cloud-native technologies.

## Dependancies required

- **Flask:**
- To install: run on env terminal "pip install flask"

- **Config:**
- To install: run on env terminal "pip install config"

- **Boto3:**
- To install: run on env terminal "pip install boto3"

- **Flask_WTF:**
- To install: run on env terminal "pip install flask_wtf"

- **Flask_Cors:**
- To install: run on env terminal "pip install flask_cors"

- **Flask_Session:**
- To install: run on env terminal "pip install flask_session"

## System Design

### A. System Architecture Components

Our system architecture incorporates the following components:

- **Frontend:** Python Flask for an interactive and responsive user interface.
- **Microservices:** Two essential microservices - Authentication/TicketMaster and Fairness Algorithm for secure user access and fair data processing.
- **Backend:** Amazon DynamoDB, a NoSQL database, for efficient data storage.

### B. Cloud-Native Framework Integration

Our system leverages Docker containerization and Kubernetes (K8s) framework for efficient management, providing consistency, portability, and scalability. We discuss the implications and challenges for comprehensive fault tolerance.

### C. Overview of Distributed Algorithms

Our project employs distributed algorithms tailored to specific tasks, particularly the Fair Distribution Algorithm, promoting equitable ticket allocation and enhancing overall booking experience.

## Implementation

### A. Microservices-Based Architecture

In our microservices-based architecture, we have developed essential components, including User Interface (UI), Authentication & Authorization, Ticket Inventory, Search & Recommendation, Order History, Security, and Notification services. API Gateway facilitates communication between microservices, supported by dedicated databases.

### B. Fair Distribution Algorithm

The Fair Distribution Algorithm ensures users in the waiting room receive queue positions based on arrival times, promoting fairness within an acceptable range.

## Conclusions

Our Anti-Scalping Booking System addresses gaps in current solutions by combining anti-scalping knowledge and cloud-native technology.
