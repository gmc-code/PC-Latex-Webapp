# PC-Latex-Webapp
Flask version of latex worksheets hosted at python anywhere.
The repo can be cloned using bash at python anywhere.

Uploading a GitHub repository to PythonAnywhere involves cloning the repository to your PythonAnywhere account. Here's how you can do it:

### Step 1: Log in to PythonAnywhere

1. Visit [PythonAnywhere](https://www.pythonanywhere.com/) and log in to your account.

----

### Step 2: Open a Bash Console

1. Navigate to the **"Consoles"** tab.
2. Start a **Bash** console.

----

### Step 3: Clone the GitHub Repository

1. In your GitHub repository, click the green **"Code"** button and copy the HTTPS or SSH URL of the repo (e.g., `https://github.com/username/repo.git`).
2. In the Bash console, type the following command to clone the repo:
   ```bash
   git clone https://github.com/username/repo.git
   ```
   e.g.
   ```bash
   git clone https://github.com/gmc-code/PC-Latex-Webapp.git
   ```
----

### Step 4: Set Up a Web App

1. Go to the **"Web"** tab in PythonAnywhere.
2. Click **"Add a new web app"**.
3. Follow the prompts to configure your web app (e.g., choose Flask, Python version, etc.).
4. Update the WSGI configuration file to point to your app.
   - You can edit the WSGI file under the **"Web"** tab.
   - Add the path to your repository and virtual environment.

----

### Step 5: Test Your Application

1. Run your application or scripts to ensure they work correctly.
2. Use the **"Files"** tab to view/edit files if needed.


----

### Step 6: Update from git

1. Since the folder already exists in the PythonAnywhere files, manually delete it first.
2. In your GitHub repository, click the green **"Code"** button and copy the HTTPS or SSH URL of the repo.
3. In the Bash console, type the following command to clone the repo:
   ```bash
   git clone https://github.com/username/repo.git
   ```
   e.g.
   ```bash
   git clone https://github.com/gmc-code/PC-Latex-Webapp.git
   ```

4. In the PythonAnywhere web, click to reload.

OR

1. In the Bash console, type the following command to clone the repo:
   ```bash
   cd path/to/project
   git pull https://github.com/username/repo.git
   ```
   e.g.
   ```bash
   cd  ~/PC-Latex-Webapp
   git pull https://github.com/gmc-code/PC-Latex-Webapp.git
   ```