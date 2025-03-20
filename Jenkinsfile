pipeline {
    agent any  // Run on any available node (e.g., the Jenkins master)

    environment {
        // Environment variables for PostgreSQL (assumes a local or network instance)
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
                // Ensure Python 3.11 is available (assumes pyenv or system Python)
                sh '''
                if ! command -v pyenv >/dev/null 2>&1; then
                    echo "pyenv not found, using system Python"
                    python3 --version
                else
                    pyenv install 3.11 -s || true
                    pyenv global 3.11
                    python --version
                fi
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Set up PostgreSQL') {
            steps {
                script {
                    // Create the database if it doesn’t exist (assumes PostgreSQL is running locally)
                    sh '''
                    psql -U ${POSTGRES_USER} -tc "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1 || \
                    createdb -U ${POSTGRES_USER} ${POSTGRES_DB}
                    '''
                }
            }
        }

        stage('Run migrations') {
            steps {
                sh 'python manage.py migrate'
            }
        }

        stage('Run tests') {
            steps {
                sh 'python manage.py test'
            }
        }

        stage('Clean up') {
            steps {
                // Optional: Drop the database (uncomment if desired)
                // sh 'dropdb -U ${POSTGRES_USER} ${POSTGRES_DB} || true'
                echo 'Skipping Docker cleanup since no containers were used'
            }
        }
    }

    post {
        always {
            // No Docker cleanup needed
            echo 'No Docker containers to stop or remove'
        }
    }
}
