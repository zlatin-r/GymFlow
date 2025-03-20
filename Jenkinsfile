pipeline {
    agent any

    environment {
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'password'
        POSTGRES_DB = 'gym_flow_db'
        DATABASE_URL = "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
        VENV_DIR = "venv"  // Virtual environment directory
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

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                echo "Virtual environment created at $VENV_DIR"
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                deactivate
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
                sh '''
                source $VENV_DIR/bin/activate
                python manage.py migrate
                deactivate
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                source $VENV_DIR/bin/activate
                python manage.py test
                deactivate
                '''
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
