# Dynamic-IP-Provider-Service

![Python](https://img.shields.io/badge/Python-3.11.4-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative)


## **Project Overview**

> The application has 2 roles: administrator and users. The administrator can view the current IP addresses of users, the list of users themselves, delete users, and also has the ability to make a user account a premium account or remove this privilege. Users can view and edit their IP addresses and domains.


## 💾 Installation

### 📂 Clone the Repository

```bash
git clone https://github.com/MaximPyanin/Event-Management-System.git
cd Event-Management-System
```
### 🔐 Set Up Environment Variables
Create a .env file in the root directory of the project and add the following environment variables:

- SENDGRID_API_KEY=your_sendgrid_api_key
- MONGO_URI=your_mongodb_uri
- SENDER_EMAIL=your_sender_email
- PAPERTRAIL_HOST=your_papertrail_host
- PAPERTRAIL_PORT=your_papertrail_port
- PUBLIC_KEY=your_public_key
- PRIVATE_KEY=yout_private_key

Install Dependencies
```bash
poetry install
```

### Docker Setup
Build and Run Docker Containers
```bash
docker compose pull
docker compose up -d  --build
```
This command will build the Docker images and start the containers for the application and RabbitMQ.

### 🔧 Usage
Run the Application
To start the application, use the following command:

```bash
docker compose up -d --build
```
### Automated Deployment with Ansible
Set the environment variable for the host IP:
```bash
export HOST_IP=your_host_ip
```
To execute the Ansible playbook, run the following command:
```bash
ansible-playbook -i inventory.yml -e ansible_host='{{ lookup("env", "HOST_IP") }}' ansible.yml
```


### 📚 Documentation
The project's API documentation can be accessed via the FastAPI interactive docs once the application is running at /docs


### 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

### 📄   License
This project is licensed under the MIT License - see the LICENSE file for details.
