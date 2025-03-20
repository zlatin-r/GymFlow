pipeline {
    agent any

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
                apt-get update
                apt-get install -y python3.11-venv
                '''
            }
        }

        stage('Install PostgreSQL') {
            steps {
                sh '''
                apt-get update
                apt-get install -y postgresql postgresql-contrib
                service postgresql start
                # Ensure md5 authentication is set before any psql commands
                sed -i 's/local   all   postgres   peer/local   all   postgres   md5/' /etc/postgresql/15/main/pg_hba.conf
                service postgresql restart
                # Use PGPASSWORD with psql directly instead of su
                export PGPASSWORD=${POSTGRES_PASSWORD}
                psql -U ${POSTGRES_USER} -c "ALTER USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';" || \
                echo "Password might already be set, proceeding..."
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
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Set up PostgreSQL') {
            steps {
                script {
                    sh '''
                    export PGPASSWORD=${POSTGRES_PASSWORD}
                    psql -U ${POSTGRES_USER} -tc "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1 || \
                    createdb -U ${POSTGRES_USER} ${POSTGRES_DB}
                    '''
                }
            }
        }

        stage('Run migrations') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py migrate
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test
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
            echo 'No Docker containers to stop or remove'
        }
    }
}