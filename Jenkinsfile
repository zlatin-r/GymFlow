pipeline {
    agent any

    environment {
        // Environment variables for PostgreSQL
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'password'
        POSTGRES_DB = 'gym_flow_db'
        DATABASE_URL = "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                checkout scm
            }
        }

        stage('Set up PostgreSQL') {
            steps {
                script {
                    // Start PostgreSQL in a Docker container
                    sh '''
                    docker run -d --name postgres \
                      -e POSTGRES_USER=${POSTGRES_USER} \
                      -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                      -e POSTGRES_DB=${POSTGRES_DB} \
                      -p 5432:5432 \
                      postgres:13
                    '''
                    // Wait for PostgreSQL to be ready
                    sh '''
                    until docker exec postgres pg_isready; do
                      sleep 1
                    done
                    '''
                }
            }
        }

        stage('Set up Python') {
            steps {
                // Set up Python 3.11
                sh '''
                pyenv install 3.11 -s
                pyenv global 3.11
                python --version
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                // Install Python dependencies
                sh '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run migrations') {
            steps {
                // Run Django migrations
                sh 'python manage.py migrate'
            }
        }

        stage('Run tests') {
            steps {
                // Run Django tests
                sh 'python manage.py test'
            }
        }

        stage('Clean up') {
            steps {
                // Stop and remove the PostgreSQL container
                sh 'docker stop postgres && docker rm postgres'
            }
        }
    }

    post {
        always {
            // Clean up Docker containers even if the pipeline fails
            sh 'docker stop postgres || true'
            sh 'docker rm postgres || true'
        }
    }
}