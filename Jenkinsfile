pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                // dir('stockPrediction/') {
                    script {
                        // Run the command to build a Docker image
                        sh 'docker build -t app ./stockPrediction/'
                        
                    }
                // }
                
            }
        }

        stage('Run Docker Image') {
            steps {
                sh "docker run -d -p 4000:80 app"
            }
        }

        stage('Wait for Docker Container') {
            steps {
                // Wait for the container to start (you can adjust the sleep time as needed)
                script {
                    sleep 10
                }
            }
        }
    }

    post {
        always {
            // Clean up or perform other actions after the build
            cleanWs()
            sh "docker stop app || true"
            sh "docker rm app || true"
        }
    }
}
