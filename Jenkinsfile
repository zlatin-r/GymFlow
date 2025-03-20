pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
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