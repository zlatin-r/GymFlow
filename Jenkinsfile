pipeline {
    agent any  // Run on any available node

    environment {
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'password'
        POSTGRES_DB = 'gym_flow_db'
        DATABASE_URL = "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                if ! command -v python3 >/dev/null 2>&1; then
                    echo "Python3 not found. Please install Python 3.11+."
                    exit 1
                fi
                python3 --version
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Set up PostgreSQL') {
            steps {
                script {
                    sh '''
                    export PGPASSWORD="${POSTGRES_PASSWORD}"
                    if ! psql -U "${POSTGRES_USER}" -h localhost -c "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1; then
                        createdb -U "${POSTGRES_USER}" -h localhost "${POSTGRES_DB}"
                    fi
                    '''
                }
            }
        }

        stage('Run migrations') {
            steps {
                sh 'python3 manage.py migrate'
            }
        }

        stage('Run tests') {
            steps {
                sh 'python3 manage.py test'
            }
        }

        stage('Clean up') {
            steps {
                echo 'Skipping Docker cleanup since no containers were used'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed'
        }
    }
}
