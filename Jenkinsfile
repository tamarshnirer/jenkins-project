pipeline {
  agent {
    label 'My Agent'
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
  }
  stages {
    stage('Fetch Files') {
      steps {
        // Checkout the code from the GitHub repo
        git branch: 'main', credentialsId: 'github_repo', url: 'https://github.com/tamarshnirer/jenkins-project.git'
      }
    }
    stage('Build and Test') {
      steps {
        // Build the Docker image
        sh 'sudo docker build -t tamarshnirer/test:latest .'
        sh 'sudo docker run --name test_container --rm -d -p 5000:5000 tamarshnirer/test:latest'
        sh 'pytest ex3.py'
        sh 'sudo docker stop test_container'
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
