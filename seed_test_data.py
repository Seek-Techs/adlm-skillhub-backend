#!/usr/bin/env python
"""
Seed script for ADLM SkillHub - AI Career Coach testing
This script populates the database with realistic test data for all models
"""

import os
import sys
from datetime import datetime, timedelta

import django
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import ForumPost, JobListing, LearningResource, User
from ai.models import AnalyticsEvent, Recommendation


def create_users():
    """Create test users with different roles and skills"""
    users_data = [
        {
            'email': 'alice.learner@example.com',
            'password': 'SecurePass123!',
            'role': 'Learner',
            'skills': ['Python', 'Django', 'Machine Learning', 'Data Analysis'],
            'progress': 0.3,
            'is_verified': True
        },
        {
            'email': 'bob.mentor@example.com',
            'password': 'MentorPass123!',
            'role': 'Mentor',
            'skills': ['React', 'Node.js', 'DevOps', 'AWS', 'Kubernetes'],
            'progress': 0.9,
            'is_verified': True
        },
        {
            'email': 'charlie.advanced@example.com',
            'password': 'AdvancedPass123!',
            'role': 'Learner',
            'skills': ['TensorFlow', 'PyTorch', 'Deep Learning', 'Computer Vision'],
            'progress': 0.7,
            'is_verified': True
        },
        {
            'email': 'diana.fullstack@example.com',
            'password': 'FullstackPass123!',
            'role': 'Learner',
            'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Express'],
            'progress': 0.5,
            'is_verified': True
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user.email}")
        created_users.append(user)
    
    return created_users

def create_learning_resources():
    """Create learning resources for different skill areas"""
    resources_data = [
        {
            'title': 'Python Fundamentals for Beginners',
            'type': 'Course',
            'content': 'Learn Python programming from scratch. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming. Perfect for beginners who want to start their programming journey with Python.'
        },
        {
            'title': 'Machine Learning with Scikit-learn',
            'type': 'Tutorial',
            'content': 'Master machine learning algorithms using scikit-learn library. Learn about supervised and unsupervised learning, model evaluation, feature engineering, and building predictive models for real-world applications.'
        },
        {
            'title': 'Django Web Development Masterclass',
            'type': 'Course',
            'content': 'Build powerful web applications with Django framework. Learn about models, views, templates, forms, authentication, REST APIs, deployment, and best practices for scalable web development.'
        },
        {
            'title': 'React Hooks and Modern Patterns',
            'type': 'Tutorial',
            'content': 'Discover modern React development with hooks, context API, and advanced patterns. Learn about useState, useEffect, custom hooks, performance optimization, and building maintainable React applications.'
        },
        {
            'title': 'Deep Learning with TensorFlow',
            'type': 'Course',
            'content': 'Dive deep into neural networks and deep learning using TensorFlow. Cover convolutional neural networks, recurrent neural networks, transfer learning, and deploying ML models in production.'
        },
        {
            'title': 'DevOps with Docker and Kubernetes',
            'type': 'Course',
            'content': 'Master containerization and orchestration with Docker and Kubernetes. Learn about container deployment, scaling, monitoring, CI/CD pipelines, and infrastructure as code.'
        },
        {
            'title': 'Data Analysis with Pandas',
            'type': 'Tutorial',
            'content': 'Analyze and manipulate data efficiently using Pandas library. Learn data cleaning, transformation, aggregation, visualization, and handling real-world datasets for data science projects.'
        },
        {
            'title': 'AWS Cloud Architecture',
            'type': 'Course',
            'content': 'Design and deploy scalable applications on AWS cloud. Learn about EC2, S3, RDS, Lambda, API Gateway, CloudFormation, and building fault-tolerant cloud architectures.'
        }
    ]
    
    created_resources = []
    for resource_data in resources_data:
        resource, created = LearningResource.objects.get_or_create(
            title=resource_data['title'],
            defaults=resource_data
        )
        if created:
            print(f"Created resource: {resource.title}")
        else:
            print(f"Resource already exists: {resource.title}")
        created_resources.append(resource)
    
    return created_resources

def create_forum_posts(users):
    """Create forum posts with realistic content"""
    posts_data = [
        {
            'title': 'Best practices for Python error handling and debugging',
            'content': "I'm working on a Python project and struggling with proper error handling. What are the best practices for exception handling in Python? Should I use try-except blocks everywhere or are there better patterns? Also, what debugging tools do you recommend for Python development? I've been using print statements but I know there must be better ways to debug complex applications.",
            'author': users[0]  # Alice
        },
        {
            'title': 'Getting started with machine learning: choosing the right algorithms',
            'content': "I'm new to machine learning and overwhelmed by the number of algorithms available. How do I choose between linear regression, decision trees, random forests, and neural networks? What factors should I consider when selecting an algorithm for a specific problem? Are there any rules of thumb or decision frameworks that can help guide algorithm selection for beginners?",
            'author': users[0]  # Alice
        },
        {
            'title': 'React hooks vs class components: when to use what?',
            'content': "I've been learning React and I'm confused about when to use hooks versus class components. I understand that hooks are the modern approach, but are there still use cases where class components are better? What are the performance implications of using hooks? Should I refactor all my existing class components to use hooks, or is it okay to mix both approaches in the same project?",
            'author': users[3]  # Diana
        },
        {
            'title': 'Docker vs Kubernetes: understanding container orchestration',
            'content': "I'm transitioning from traditional deployment methods to containerization. I understand Docker for creating containers, but I'm struggling to understand when and why I need Kubernetes. What problems does Kubernetes solve that Docker alone cannot? Is it overkill for small applications? What's the learning curve like, and are there simpler alternatives to Kubernetes for container orchestration?",
            'author': users[1]  # Bob
        },
        {
            'title': 'Deep learning model optimization and performance tuning',
            'content': "I'm working on a computer vision project using TensorFlow and my models are training very slowly. What are the best practices for optimizing deep learning models? Should I focus on data preprocessing, model architecture, or training parameters? I've heard about techniques like batch normalization, dropout, and learning rate scheduling but I'm not sure how to apply them effectively.",
            'author': users[2]  # Charlie
        },
        {
            'title': 'Building scalable APIs with Django REST Framework',
            'content': "I'm developing a REST API using Django REST Framework for a mobile app with potentially thousands of users. What are the best practices for ensuring scalability and performance? How should I handle authentication, rate limiting, and caching? Are there specific patterns or architectural decisions I should consider for high-traffic applications?",
            'author': users[3]  # Diana
        }
    ]
    
    created_posts = []
    for post_data in posts_data:
        post, created = ForumPost.objects.get_or_create(
            title=post_data['title'],
            defaults=post_data
        )
        if created:
            print(f"Created forum post: {post.title}")
        else:
            print(f"Forum post already exists: {post.title}")
        created_posts.append(post)
    
    return created_posts

def create_job_listings():
    """Create realistic job listings"""
    jobs_data = [
        {
            'title': 'Senior Python Developer - Machine Learning',
            'description': 'We are seeking a Senior Python Developer with expertise in machine learning to join our AI team. Requirements: 5+ years Python experience, experience with TensorFlow/PyTorch, strong background in data science, knowledge of MLOps practices. Responsibilities include developing ML models, optimizing algorithms, and deploying models to production. Competitive salary and benefits package.',
            'company': 'TechAI Solutions'
        },
        {
            'title': 'Frontend React Developer',
            'description': "Join our frontend team as a React Developer! We're looking for someone with 3+ years of React experience, proficiency in modern JavaScript (ES6+), experience with state management (Redux/Context API), and knowledge of testing frameworks (Jest, React Testing Library). You'll work on building responsive user interfaces and collaborating with design and backend teams.",
            'company': 'WebFlow Innovations'
        },
        {
            'title': 'DevOps Engineer - Cloud Infrastructure',
            'description': "We're hiring a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. Required skills: AWS/Azure experience, Docker and Kubernetes, Infrastructure as Code (Terraform), CI/CD tools (Jenkins, GitLab CI), monitoring and logging tools. You'll be responsible for maintaining high availability systems, automating deployments, and ensuring security best practices.",
            'company': 'CloudOps Pro'
        },
        {
            'title': 'Full Stack Developer - Django/React',
            'description': 'Looking for a Full Stack Developer to work on our web platform. Tech stack includes Django backend with REST APIs and React frontend. Requirements: 4+ years full stack experience, proficiency in Python/Django, React/JavaScript, PostgreSQL, Git, and Agile methodologies. Experience with AWS deployment is a plus.',
            'company': 'StartupTech Inc'
        },
        {
            'title': 'Data Scientist - Computer Vision',
            'description': 'Join our computer vision team to develop cutting-edge image recognition systems. Requirements: PhD or Masters in Computer Science/Statistics, 3+ years experience with deep learning frameworks, computer vision libraries (OpenCV, PIL), and cloud platforms. Experience with production ML systems preferred.',
            'company': 'VisionAI Corp'
        }
    ]
    
    created_jobs = []
    for job_data in jobs_data:
        job, created = JobListing.objects.get_or_create(
            title=job_data['title'],
            defaults=job_data
        )
        if created:
            print(f"Created job listing: {job.title}")
        else:
            print(f"Job listing already exists: {job.title}")
        created_jobs.append(job)
    
    return created_jobs

def create_analytics_events(users):
    """Create analytics events for testing predictive analytics"""
    event_types = ['login', 'resource_view', 'forum_post']
    
    # Create events for the past 30 days
    base_time = timezone.now() - timedelta(days=30)
    
    for i in range(150):  # Create 150 events
        user = users[i % len(users)]
        event_type = event_types[i % len(event_types)]
        timestamp = base_time + timedelta(
            days=i // 5,  # Spread over 30 days
            hours=i % 24,  # Different hours
            minutes=i % 60
        )
        
        details = {}
        if event_type == 'resource_view':
            details = {'resource_id': (i % 8) + 1}  # Assuming 8 resources
        elif event_type == 'forum_post':
            details = {'post_id': (i % 6) + 1}  # Assuming 6 forum posts
        
        event, created = AnalyticsEvent.objects.get_or_create(
            user=user,
            event_type=event_type,
            timestamp=timestamp,
            defaults={'details': details}
        )
        
        if created:
            print(f"Created analytics event: {event_type} for {user.email}")

def create_recommendations(users, resources):
    """Create recommendation scores for testing recommendation engine"""
    import random
    
    for user in users:
        for resource in resources:
            # Generate realistic recommendation scores based on user skills
            score = random.uniform(0.1, 1.0)
            
            # Boost scores for relevant resources
            user_skills_lower = [skill.lower() for skill in user.skills]
            resource_content_lower = resource.content.lower()
            
            for skill in user_skills_lower:
                if skill in resource_content_lower:
                    score = min(1.0, score + 0.3)
            
            recommendation, created = Recommendation.objects.get_or_create(
                user=user,
                resource=resource,
                defaults={'score': score}
            )
            
            if created:
                print(f"Created recommendation: {resource.title} for {user.email} (score: {score:.2f})")

def main():
    """Main function to populate all test data"""
    print("Starting database seeding for ADLM SkillHub AI Career Coach...")
    
    print("\n1. Creating users...")
    users = create_users()
    
    print("\n2. Creating learning resources...")
    resources = create_learning_resources()
    
    print("\n3. Creating forum posts...")
    forum_posts = create_forum_posts(users)
    
    print("\n4. Creating job listings...")
    job_listings = create_job_listings()
    
    print("\n5. Creating analytics events...")
    create_analytics_events(users)
    
    print("\n6. Creating recommendations...")
    create_recommendations(users, resources)
    
    print("\n✅ Database seeding completed successfully!")
    print("\nTest users created:")
    for user in users:
        print(f"  - {user.email} ({user.role}) - Skills: {', '.join(user.skills)}")
    
    print(f"\nCreated:")
    print(f"  - {len(users)} users")
    print(f"  - {len(resources)} learning resources")
    print(f"  - {len(forum_posts)} forum posts")
    print(f"  - {len(job_listings)} job listings")
    print(f"  - 150 analytics events")
    print(f"  - {len(users) * len(resources)} recommendations")

if __name__ == '__main__':
    main()
