// pipeline {
//     agent any

//     stages {

//         stage('Setup') {
//             steps {
//                 script {
//                     sh "docker stop app_container || true"
//                     sh "docker rm app_container || true"
//                 }
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 // dir('stockPrediction/') {
//                     script {
//                         // Run the command to build a Docker image
//                         sh 'docker build -t app ./stockPrediction/'
                        
//                     }
//                 // }
                
//             }
//         }

//         stage('Run Docker Image') {
//             steps {
//                 sh 'docker run -d -p 4000:80 --name app_container app'

//             }
//         }

//         stage('Wait for Docker Container') {
//             steps {
//                 // Wait for the container to start (you can adjust the sleep time as needed)
//                 script {
//                     sleep 10
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             // Clean up or perform other actions after the build
//             cleanWs()
//         }
//     }
// }

pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                script {
                    sh "docker stop app_container || true"
                    sh "docker rm app_container || true"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        // Run the command to build a Docker image
                        sh 'docker build -t app ./stockPrediction/'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to build Docker image: ${e.message}")
                    }
                }
            }
        }

        stage('Run Docker Image') {
            steps {
                script {
                    try {
                        sh 'docker run -d -p 4000:80 --name app_container app'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Failed to run Docker image: ${e.message}")
                    }
                }
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
        }

        success {
            // Send email notification on success
            emailext subject: "Build Successful: ${currentBuild.fullDisplayName}",
                      body: "Build successful for job ${env.JOB_NAME}.\n\n${BUILD_URL}",
                      to: "shaik.asif20@st.niituniversity.in",
                      attachLog: true
        }

        failure {
            // Send email notification on failure
            emailext subject: "Build Failed: ${currentBuild.fullDisplayName}",
                      body: "Build failed for job ${env.JOB_NAME}.\n\n${BUILD_URL}",
                      to: "shaik.asif20@st.niituniversity.in",
                      attachLog: true
        }
    }
}
