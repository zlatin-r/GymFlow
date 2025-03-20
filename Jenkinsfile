pipeline {
    agent any  // Run on any available node (e.g., the Jenkins master)

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
                    echo "Python 3 is not installed"
                    exit 1
                fi
                python3 --version
                '''
            }
        }

        stage('Install venv package') {
            steps {
                sh '''
                # Install python3-venv if not available (on Debian/Ubuntu systems)
                apt-get update
                apt-get install -y python3.11-venv
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                # Activate the virtual environment and install dependencies
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Set up PostgreSQL') {
            steps {
                script {
                    sh '''
                    psql -U ${POSTGRES_USER} -tc "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1 || \
                    createdb -U ${POSTGRES_USER} ${POSTGRES_DB}
                    '''
                }
            }
        }

        stage('Run migrations') {
            steps {
                sh 'source venv/bin/activate && python manage.py migrate'
            }
        }

        stage('Run tests') {
            steps {
                sh 'source venv/bin/activate && python manage.py test'
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
            echo 'No Docker containers to stop or remove'
        }
    }
}

