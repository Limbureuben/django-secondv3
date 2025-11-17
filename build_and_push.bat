@echo off
echo ========================================
echo  Build and Push Docker Image to Hub
echo ========================================

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo  Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo.
echo  This script will build and push your Docker image to Docker Hub.
echo  You need to:
echo    1. Have a Docker Hub account
echo    2. Be logged in: docker login
echo    3. Enter your Docker Hub username below
echo.
set /p DOCKER_USERNAME="Enter your Docker Hub username: "

if "%DOCKER_USERNAME%"=="" (
    echo  Error: Username cannot be empty!
    pause
    exit /b 1
)

echo.
echo  Choose what to build and push:
echo    1. Development image (dev target)
echo    2. Production image (prod target)
echo    3. Both
echo.
set /p CHOICE="Enter choice (1/2/3): "

if "%CHOICE%"=="1" goto BUILD_DEV
if "%CHOICE%"=="2" goto BUILD_PROD
if "%CHOICE%"=="3" goto BUILD_BOTH
echo  Invalid choice!
pause
exit /b 1

:BUILD_DEV
echo.
echo  Building development image...
docker build --target dev -t %DOCKER_USERNAME%/openspace-backend:dev -t %DOCKER_USERNAME%/openspace-backend:dev-latest .
if errorlevel 1 (
    echo  Build failed!
    pause
    exit /b 1
)
echo.
echo  Pushing development image to Docker Hub...
docker push %DOCKER_USERNAME%/openspace-backend:dev
docker push %DOCKER_USERNAME%/openspace-backend:dev-latest
goto END

:BUILD_PROD
echo.
echo  Building production image...
docker build --target prod -t %DOCKER_USERNAME%/openspace-backend:prod -t %DOCKER_USERNAME%/openspace-backend:latest .
if errorlevel 1 (
    echo  Build failed!
    pause
    exit /b 1
)
echo.
echo  Pushing production image to Docker Hub...
docker push %DOCKER_USERNAME%/openspace-backend:prod
docker push %DOCKER_USERNAME%/openspace-backend:latest
goto END

:BUILD_BOTH
echo.
echo  Building development image...
docker build --target dev -t %DOCKER_USERNAME%/openspace-backend:dev -t %DOCKER_USERNAME%/openspace-backend:dev-latest .
if errorlevel 1 (
    echo  Development build failed!
    pause
    exit /b 1
)
echo.
echo  Building production image...
docker build --target prod -t %DOCKER_USERNAME%/openspace-backend:prod -t %DOCKER_USERNAME%/openspace-backend:latest .
if errorlevel 1 (
    echo  Production build failed!
    pause
    exit /b 1
)
echo.
echo  Pushing development image to Docker Hub...
docker push %DOCKER_USERNAME%/openspace-backend:dev
docker push %DOCKER_USERNAME%/openspace-backend:dev-latest
echo.
echo  Pushing production image to Docker Hub...
docker push %DOCKER_USERNAME%/openspace-backend:prod
docker push %DOCKER_USERNAME%/openspace-backend:latest
goto END

:END
echo.
echo ========================================
echo  Build and push complete!
echo ========================================
echo  Your images are now available at:
echo    https://hub.docker.com/r/%DOCKER_USERNAME%/openspace-backend
echo.
echo  To use these images in production, update docker-compose.prod.yml:
echo    Change from: build: { context: ., dockerfile: Dockerfile, target: prod }
echo    Change to:   image: %DOCKER_USERNAME%/openspace-backend:prod
echo ========================================
pause
