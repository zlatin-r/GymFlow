pipeline {
    agent any

//     environment {
//         POSTGRES_USER = 'postgres'
//         POSTGRES_PASSWORD = 'password'
//         POSTGRES_DB = 'gym_flow_db'
//         DATABASE_URL = "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
//     }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

//         stage('Set up Python') {
//             steps {
//                 sh '''
//                 if ! command -v python3 >/dev/null 2>&1; then
//                     echo "Python 3 is not installed"
//                     exit 1
//                 fi
//                 python3 --version
//                 '''
//             }
//         }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                # Verify venv creation
                if [ ! -f venv/bin/activate ]; then
                    echo "Failed to create virtual environment"
                    ls -la
                    exit 1
                fi
                echo "Virtual environment created successfully"
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

//         stage('Set up PostgreSQL') {
//             steps {
//                 sh '''
//                 service postgresql start
//                 export PGPASSWORD=${POSTGRES_PASSWORD}
//                 psql -U ${POSTGRES_USER} -tc "SELECT 1 FROM pg_database WHERE datname = '${POSTGRES_DB}'" | grep -q 1 || \
//                 createdb -U ${POSTGRES_USER} ${POSTGRES_DB}
//                 '''
//             }
//         }

//         stage('Run migrations') {
//             steps {
//                 sh '''
//                 . venv/bin/activate
//                 python manage.py migrate
//                 '''
//             }
//         }

        stage('Run Authentication Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test gym_flow.accounts.tests.AuthTests
                '''
            }
        }

        stage('Run View Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test gym_flow.accounts.tests.ViewTests
                '''
            }
        }

        stage('Run Form Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test gym_flow.accounts.tests.FormTests
                '''
            }
        }

        stage('Run User Model Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test gym_flow.accounts.tests.UserModelTests
                '''
            }
        }

        stage('Run Profile Model Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python manage.py test gym_flow.accounts.tests.ProfileModelTests
                '''
            }
        }
    }
}


