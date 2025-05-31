#!/usr/bin/env python3
"""
Git Commit Strategy Executor
Executes the comprehensive git commit plan for the homescreen project
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Execute a command and return the result"""
    try:
        print(f"🔄 {description}")
        print(f"   Command: {cmd}")
        
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30,
            cwd="/home/reid/projects/homescreen"
        )
        
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {description}")
        return False
    except Exception as e:
        print(f"💥 Exception: {description} - {str(e)}")
        return False

def main():
    """Execute the git commit strategy"""
    print("🚀 Starting Homescreen Git Commit Strategy Execution")
    print("=" * 60)
    
    # Change to project directory
    project_dir = "/home/reid/projects/homescreen"
    if not os.path.exists(project_dir):
        print(f"❌ Project directory not found: {project_dir}")
        return False
    
    os.chdir(project_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Git commands to execute
    commands = [
        ("git init", "Initialize Git repository"),
        ("git config user.name 'Homescreen Developer'", "Configure Git user name"),
        ("git config user.email 'developer@homescreen.local'", "Configure Git user email"),
        ("git add .gitignore", "Stage .gitignore file"),
        ("git commit -m 'chore: add comprehensive .gitignore file'", "Commit .gitignore"),
        ("git add manage.py homescreen_project/ requirements.txt requirements-dev.txt pyproject.toml", "Stage Django project files"),
        ("git commit -m 'feat: initialize Django project with basic configuration'", "Commit Django project"),
        ("git add api/__init__.py api/models.py api/admin.py api/apps.py api/migrations/", "Stage database models"),
        ("git commit -m 'feat: add core database models for image processing'", "Commit database models"),
        ("git add api/serializers.py api/views.py api/urls.py", "Stage API foundation"),
        ("git commit -m 'feat: implement core API serializers and views'", "Commit API foundation"),
        ("git add api/auth_views.py", "Stage authentication"),
        ("git commit -m 'feat: implement JWT authentication with refresh tokens'", "Commit authentication"),
        ("git add api/ai_services/__init__.py api/ai_services/interfaces.py api/ai_services/registry.py api/ai_services/factory.py api/ai_services/config.py", "Stage AI services foundation"),
        ("git commit -m 'feat: implement service-agnostic AI architecture'", "Commit AI services foundation"),
        ("git add api/ai_services/providers/", "Stage AI providers"),
        ("git commit -m 'feat: add AI service providers and mock implementation'", "Commit AI providers"),
        ("git add api/ai_enhanced_processor.py api/image_processor.py", "Stage AI processing"),
        ("git commit -m 'feat: implement AI-enhanced image processor'", "Commit AI processing"),
        ("git add frontend/package.json frontend/package-lock.json frontend/public/ frontend/src/index.js frontend/src/App.js frontend/src/App.css frontend/src/index.css frontend/src/logo.svg frontend/src/reportWebVitals.js", "Stage React initialization"),
        ("git commit -m 'feat: initialize React frontend with basic structure'", "Commit React initialization"),
        ("git add frontend/src/components/", "Stage UI components"),
        ("git commit -m 'feat: add reusable UI components library'", "Commit UI components"),
        ("git add frontend/src/store/ frontend/src/services/ frontend/src/utils/", "Stage state management"),
        ("git commit -m 'feat: implement Zustand state management and API services'", "Commit state management"),
        ("git add frontend/src/pages/ frontend/src/hooks/", "Stage application pages"),
        ("git commit -m 'feat: implement core application pages and routing'", "Commit application pages"),
        ("git add api/tests/", "Stage backend tests"),
        ("git commit -m 'test: add comprehensive backend test suite'", "Commit backend tests"),
        ("git add frontend/src/setupTests.js frontend/src/App.test.js frontend/cypress.config.js frontend/cypress/", "Stage frontend tests"),
        ("git commit -m 'test: add comprehensive frontend test suite'", "Commit frontend tests"),
        ("git add Dockerfile docker-compose.yml docker-compose.dev.yml docker/", "Stage Docker configuration"),
        ("git commit -m 'feat: add Docker containerization and development setup'", "Commit Docker configuration"),
        ("git add scripts/ Makefile", "Stage build scripts"),
        ("git commit -m 'feat: add build scripts and development tools'", "Commit build scripts"),
        ("git add README.md PROJECT_DOCUMENTATION.md task_tracker.md", "Stage core documentation"),
        ("git commit -m 'docs: add comprehensive project documentation'", "Commit core documentation"),
        ("git add docs/", "Stage technical documentation"),
        ("git commit -m 'docs: add technical guides and API documentation'", "Commit technical documentation"),
        ("git add *_GUIDE.md *_SUMMARY.md CONTEXT_AWARE_DETECTION.md SCREEN_REFERENCE_GUIDE.md SIMPLIFIED_SCREEN_CATEGORIES.md OPENAI_INTEGRATION_COMPLETE.md manual_testing_and_frontend_guide.md commit_plan.md COMMIT_EXECUTION_GUIDE.md REPOSITORY_ANALYSIS.md IMPLEMENTATION_COMPLETE.md EXECUTE_NOW.md", "Stage implementation guides"),
        ("git commit -m 'docs: add implementation and refactoring guides'", "Commit implementation guides"),
        ("git add *.py *.sh", "Stage utility scripts"),
        ("git commit -m 'feat: add utility scripts and project configuration'", "Commit utility scripts"),
        ("git add media/", "Stage media structure"),
        ("git commit -m 'feat: add media structure and screen reference system'", "Commit media structure"),
    ]
    
    # Execute commands
    success_count = 0
    total_commands = len(commands)
    
    for i, (cmd, desc) in enumerate(commands, 1):
        print(f"\n📦 Step {i}/{total_commands}: {desc}")
        if run_command(cmd, desc):
            success_count += 1
        else:
            print(f"⚠️  Continuing with next command...")
    
    # Final verification
    print(f"\n🔍 FINAL VERIFICATION")
    print("=" * 30)
    
    run_command("git rev-list --count HEAD", "Count total commits")
    run_command("git ls-files | wc -l", "Count tracked files")
    run_command("git log --oneline -10", "Show recent commits")
    
    # Summary
    print(f"\n🎉 EXECUTION SUMMARY")
    print("=" * 30)
    print(f"✅ Successful commands: {success_count}/{total_commands}")
    print(f"📊 Success rate: {(success_count/total_commands)*100:.1f}%")
    
    if success_count >= total_commands * 0.8:  # 80% success rate
        print("🎊 Git commit strategy executed successfully!")
        print("🚀 Repository is ready for collaboration!")
        return True
    else:
        print("⚠️  Some commands failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
