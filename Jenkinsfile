pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                dir('stockPrediction/') {
                    script {
                        // Run the command to build a Docker image
                        sh 'docker build -t app .'
                    }
                }
                
            }
        }

        stage('Run Docker Image') {
            steps {
                sh "docker run -p 4000:80 app"
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
