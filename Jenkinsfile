pipeline {
  agent {
      node "agent"
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
  }
  stages {
    stage('Fetch files') {
      steps {
        // Checkout the code 
        git branch: 'main', credentialsId: 'github_repo', url: 'https://github.com/tamarshnirer/jenkins-project.git'
      }
    }
    stage('Build and test') {
      steps { 
        sh 'sudo docker build -t tamarshnirer/test:latest .' 
      }
    }
    stage('Run and Test container') {
      steps {
        script {
          def containerName = "test_container"

          // Check if the container is running
          def containerStatus = sh(script: "docker ps --format '{{.Names}}' | grep ${containerName}", returnStatus: true)

          if (containerStatus == 0) {
            echo "Container ${containerName} is already running."
            sh 'sudo docker stop test_container'
            'sudo docker rmi tamarshnirer/test:latest'
          } 
          sh 'sudo docker run --name test_container --rm -d -p 5000:5000 tamarshnirer/test:latest'
          sh 'pytest /home/ubuntu/workspace/web_deployment/tests.py'
          sh 'sudo docker stop test_container'
          
        }
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'sudo docker push tamarshnirer/test:latest'
        sh 'sudo docker rmi tamarshnirer/test:latest'
      }
    }
    stage('Deployment') {
      steps {
        script {
          sshagent(credentials: ['deployment']) {
            sh 'ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.26.62 echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            sh 'ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.26.62 sudo docker pull tamarshnirer/test'
            sh 'ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.26.62 sudo docker stop $(sudo docker ps -aq) || true'
            sh 'ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.26.62 sudo docker rm $(sudo docker ps -aq) || true'
            sh 'ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.26.62 sudo docker run --name test_container --rm -d -p 5000:5000 tamarshnirer/test'
          }
        }
      }
    }
  }
}
