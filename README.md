# EduBot - Educational Management Assistant

## Overview

EduBot is a virtual assistant designed to enhance the management processes within educational institutions. Built on the robust Rasa framework, EduBot leverages advanced Natural Language Processing (NLP) techniques. This repository contains the codebase.

## Architecture
![Arquitectura de EduBot](arquitectura_edubot.png)

The architecture of EduBot is designed to ensure scalability, reliability, and efficiency in handling educational management tasks. The key components of the system are as follows:

- **Front End:** A responsive web interface accessible from both desktop and mobile devices. This interface allows users to interact with EduBot and access its features seamlessly. The front end is containerized and deployed in the cloud to ensure scalability and high availability.

- **Rasa Server:** The core of EduBot, hosted in a cloud-based container. It comprises two primary components:
  - **Dialogue Policies:** Define the conversational flow, guiding EduBot's responses based on user input and dialogue context.
  - **NLU Pipeline (Natural Language Understanding):** Processes user inputs, transforming them into structured data that EduBot can understand and respond to.

- **Agent:** The central component within the Rasa Server that manages interactions based on dialogue policies and NLU output. It receives actions and events from the Action Server to deliver appropriate responses.

- **Action Server:** Deployed using Rasa SDK, this server handles specific tasks required to fulfill user requests. It includes:
  - **Drive Folder:** Interacts with Google Drive to store and retrieve data.
  - **Flows Folder:** Contains predefined dialogue flows to maintain coherent conversations.
  - **LLM Folder (Meta):** Integrates with Meta's LLaMa (Large Language Model) to perform advanced NLP tasks.

- **Google Drive Integration:** EduBot uses Google Drive to manage and store various educational documents, including learning units, sessions, and annual plans. The integration is handled through the Google Drive API, developed in Python.

## Key Features

EduBot is designed to address three primary workflows within educational management:

1. **Educational Management:** Handles queries related to learning units, sessions, and annual plans. If any required documents are missing, EduBot sends notifications to the responsible teachers via email.

2. **Monitoring Schedule:** Evaluates teachers based on criteria established by the Ministry of Education (Minedu). The results are communicated to the teachers through email.

3. **Teacher Monitoring:** Provides information on the classrooms assigned to the deputy director for supervision, including reminders to manage schedules effectively.

## Technology Stack

EduBot is built using the following technologies:

- **Rasa:** For conversational AI and NLP.
- **Docker:** To containerize the application components.
- **Google Drive API:** For document management and integration.
- **Meta's LLaMa:** For advanced NLP processing.
- **Python:** As the primary programming language for backend development.

## Getting Started

### Prerequisites

Before deploying EduBot, ensure you have the following:

- Docker installed on your local machine.
- Access to a cloud service provider (e.g., Google Cloud, AWS).
- API credentials for Google Drive.
- Rasa and Rasa SDK installed.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/edubot.git
   cd edubot

2. Set up environment variables and configure the docker-compose.yml file with your API keys and credentials.

3. Build and run the Docker containers

    ```bash
    docker-compose up --build
    ```
    
4. Access the EduBot front end through your browser at http://localhost:5005.
