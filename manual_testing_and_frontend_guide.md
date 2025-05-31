# Manual Testing and Frontend Implementation Guide

This document provides step-by-step instructions for completing the manual testing tasks (Task 1.13) and implementing the React frontend (Phases 2 and 3) for the Homescreen Visualization App.

## Task 1.13: Basic API Endpoint Testing (Manual)

### Prerequisites
- Django backend is set up and configured
- Superuser account has been created (username: admin, password: adminpassword)
- ScreenType objects have been created in the admin interface

### Step-by-Step Guide

1. **Start the Development Server**
   ```bash
   cd /home/reid/projects/homescreen_project
   python3 manage.py runserver
   ```
   This will start the Django development server at http://127.0.0.1:8000/

2. **Access the Admin Interface**
   - Open a web browser and navigate to http://127.0.0.1:8000/admin/
   - Log in using the superuser credentials:
     - Username: admin
     - Password: adminpassword

3. **Verify Screen Types**
   - In the admin interface, click on "Screen types" under the "API" section
   - Verify that the screen types you created earlier (e.g., "Security" and "Solar") are listed
   - If needed, add more screen types by clicking "Add screen type"

4. **Test the API Endpoints**
   - Navigate to http://127.0.0.1:8000/api/screentypes/
   - You should see a list of screen types in the Django REST Framework browsable API
   - Navigate to http://127.0.0.1:8000/api/visualizations/
   - You should see an authentication error or be prompted to log in

5. **Log in to the Browsable API**
   - Click the "Log in" link in the top right corner of the browsable API
   - Log in using the superuser credentials

6. **Test the Visualizations Endpoint**
   - Navigate again to http://127.0.0.1:8000/api/visualizations/
   - You should now see an empty list (since no visualization requests have been created yet)
   - You should also see a form at the bottom of the page that allows you to create a new visualization request

7. **Stop the Development Server**
   - Return to the terminal where the server is running
   - Press Ctrl+C to stop the server

## Phase 2: React Frontend Setup

### Task 2.1: Project Initialization

1. **Navigate to the Parent Directory**
   ```bash
   cd /home/reid/projects
   ```

2. **Create a New React App**
   ```bash
   npx create-react-app frontend
   ```
   This will create a new React application in the `frontend` directory.

3. **Navigate to the Frontend Directory**
   ```bash
   cd frontend
   ```

4. **Verify the Directory Structure**
   ```bash
   ls -la
   ```
   You should see the standard React project structure with directories like `src`, `public`, `node_modules`, etc.

### Task 2.2: Install Frontend Dependencies

1. **Install Axios and React Router**
   ```bash
   npm install axios react-router-dom
   ```
   Axios is used for making HTTP requests, and React Router is used for client-side routing.

2. **Install State Management Library**
   ```bash
   npm install zustand
   ```
   Zustand is a lightweight state management library. Alternatively, you could use Redux or React Context.

3. **Verify Dependencies**
   - Open `package.json` in a text editor
   - Verify that the dependencies have been added to the `dependencies` section

### Task 2.3: Basic Project Structure Setup

1. **Create Required Subdirectories in src**
   ```bash
   mkdir -p src/components src/pages src/services src/hooks src/store src/assets
   ```

2. **Create Subdirectories in components**
   ```bash
   mkdir -p src/components/Auth src/components/Upload src/components/Results src/components/Layout src/components/Common
   ```

### Task 2.4: Implement API Service Module

1. **Create the API Service File**
   ```bash
   mkdir -p src/services
   touch src/services/api.js
   ```

2. **Add the API Service Code**
   - Open `src/services/api.js` in a text editor
   - Add the code for the API service as specified in the tasks.md file
   - The code should include functions for authentication, fetching screen types, and managing visualization requests

## Phase 3: Core Feature Implementation

### Task 3.1: Implement Basic Routing

1. **Modify App.js**
   - Open `src/App.js` in a text editor
   - Import the necessary components from react-router-dom
   - Set up the router with routes for login, register, upload, results, etc.

2. **Create Placeholder Components**
   - Create placeholder components for each page in the `src/pages` directory
   - For example:
     ```bash
     touch src/pages/LoginPage.js src/pages/RegisterPage.js src/pages/UploadPage.js src/pages/ResultsPage.js src/pages/ResultDetailPage.js
     ```

### Task 3.2: Implement Authentication Components & Logic

1. **Create Authentication Form Components**
   ```bash
   touch src/components/Auth/LoginForm.js src/components/Auth/RegisterForm.js
   ```

2. **Create Authentication Pages**
   - Implement `src/pages/LoginPage.js` and `src/pages/RegisterPage.js` using the form components

3. **Implement Authentication Logic**
   - Add logic to call the `loginUser` and `registerUser` functions from the API service
   - Handle form submission, validation, and error handling

4. **Implement State Management for Authentication**
   - Create a store for authentication state using Zustand (or your chosen state management solution)
   - Store the authentication token and user information
   - Implement protected routes that require authentication

### Task 3.3: Implement Screen Type Selection

1. **Create Screen Selector Component**
   ```bash
   touch src/components/Upload/ScreenSelector.js
   ```

2. **Implement Screen Type Fetching**
   - Use the `getScreenTypes` function from the API service to fetch screen types
   - Use `useEffect` to fetch the screen types when the component mounts

3. **Display Screen Types**
   - Render the screen types as options (e.g., dropdown, radio buttons)
   - Style the component appropriately

4. **Manage Selected Screen Type**
   - Add state to track the selected screen type ID
   - Update the state when the user selects a different option

### Task 3.4: Implement Image Upload Component

1. **Create Image Uploader Component**
   ```bash
   touch src/components/Upload/ImageUploader.js
   ```

2. **Implement File Input**
   - Add an `<input type="file" accept="image/*">` element
   - Style the input or create a custom file input component

3. **Handle File Selection**
   - Add an event handler for the file input's onChange event
   - Store the selected file in the component's state

4. **Display Image Preview**
   - Use URL.createObjectURL to create a preview URL for the selected image
   - Display the preview image
   - Clean up the URL when the component unmounts or when a new file is selected

### Task 3.5: Create Upload Page

1. **Create Upload Page Component**
   - Implement `src/pages/UploadPage.js` using the `ImageUploader` and `ScreenSelector` components

2. **Combine Components**
   - Include both the `ImageUploader` and `ScreenSelector` components on the page
   - Add a form to wrap the components

3. **Implement Form Submission Logic**
   - Create a `FormData` object to hold the form data
   - Append the selected image file and screen type ID to the `FormData`
   - Call the `createVisualizationRequest` function from the API service
   - Handle success (e.g., navigate to results page) and errors

### Task 3.6: Implement Results Display

1. **Create Results Page Component**
   - Implement `src/pages/ResultsPage.js` to display a list of visualization requests

2. **Fetch Visualization Requests**
   - Use the `getVisualizationRequests` function from the API service
   - Use `useEffect` to fetch the requests when the component mounts

3. **Display Request List**
   - Render the list of requests, showing key information like original image thumbnail, status, and date
   - Add links to the detail page for each request

4. **Create Result Detail Page**
   - Implement `src/pages/ResultDetailPage.js` to display details for a single request

5. **Fetch Request Details**
   - Use the `getVisualizationRequestDetails` function from the API service
   - Use `useEffect` to fetch the details when the component mounts or when the request ID changes

6. **Create Results Display Component**
   ```bash
   touch src/components/Results/ResultsDisplay.js
   ```
   - Implement the component to display the original image and any generated result images
   - Use this component in the `ResultDetailPage`

## Running the Complete Application

1. **Start the Django Backend**
   ```bash
   cd /home/reid/projects/homescreen_project
   python3 manage.py runserver
   ```

2. **Start the React Frontend (in a separate terminal)**
   ```bash
   cd /home/reid/projects/frontend
   npm start
   ```

3. **Access the Application**
   - Open a web browser and navigate to http://localhost:3000
   - You should see the React frontend, which will communicate with the Django backend API

## Troubleshooting

### CORS Issues
If you encounter CORS (Cross-Origin Resource Sharing) issues, you'll need to install and configure django-cors-headers:

1. **Install django-cors-headers**
   ```bash
   pip install django-cors-headers
   ```

2. **Add it to INSTALLED_APPS in settings.py**
   ```python
   INSTALLED_APPS = [
       # ...
       'corsheaders',
       # ...
   ]
   ```

3. **Add the middleware**
   ```python
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       # ... other middleware
   ]
   ```

4. **Configure CORS settings**
   ```python
   # Allow requests from the React development server
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
   ]
   ```

### Authentication Issues
If you encounter authentication issues:

1. **Check that the token is being sent correctly** in the Authorization header
2. **Verify that the token is valid** and has not expired
3. **Check the browser console for errors** related to authentication

### API Connection Issues
If the frontend cannot connect to the backend:

1. **Verify that both servers are running**
2. **Check that the API base URL** in the frontend matches the URL where the Django server is running
3. **Check for network errors** in the browser console
