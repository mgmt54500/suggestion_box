# Suggestion Box — Backend

This repository contains the starter backend for the Suggestion Box demo. By the end of this setup, you will have a live FastAPI application running on Google Cloud Run, connected to a BigQuery table that stores anonymous suggestions.

## What's in this repo

| File | Description |
|---|---|
| `main.py` | FastAPI application with three working endpoints |
| `pyproject.toml` | Poetry dependency configuration |
| `Dockerfile` | Container build instructions for Cloud Run |
| `schema.sql` | BigQuery DDL — creates the `suggestions` table |

## Overview

1. [Set Up the Database in BigQuery](#part-1-set-up-the-database-in-bigquery)
   - [Step 1: Select Your Google Cloud Project](#step-1-select-your-google-cloud-project)
   - [Step 2: Create a BigQuery Dataset](#step-2-create-a-bigquery-dataset)
   - [Step 3: Create the Table](#step-3-create-the-table)
2. [Fork and Clone the Repository](#part-2-fork-and-clone-the-repository)
   - [Step 4: Fork This Repository](#step-4-fork-this-repository)
   - [Step 5: Clone Your Fork in Cloud Shell](#step-5-clone-your-fork-in-cloud-shell)
3. [Configure and Run the API](#part-3-configure-and-run-the-api)
   - [Step 6: Open the Project in Cloud Shell Editor](#step-6-open-the-project-in-cloud-shell-editor)
   - [Step 7: Install Dependencies](#step-7-install-dependencies)
   - [Step 8: Update Your Project ID](#step-8-update-your-project-id)
   - [Step 9: Test Locally](#step-9-test-locally)
   - [Step 10: Connect Cloud Run to GitHub](#step-10-connect-cloud-run-to-github)
   - [Step 11: Push to GitHub and Deploy](#step-11-push-to-github-and-deploy)
   - [Step 12: Add Your Service Account to Cloud Run](#step-12-add-your-service-account-to-cloud-run)

---

## Part 1: Set Up the Database in BigQuery

### Step 1: Select Your Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com)
2. In the project selector at the top of the page, confirm that your course project is selected

---

### Step 2: Create a BigQuery Dataset

1. Search for **BigQuery** in the top search bar and open it
2. In the **Explorer** pane on the left, click the three dots (`⋮`) next to your Project ID and select **Create dataset**
3. Fill in the following fields:
   - **Dataset ID**: `suggestion_box`
   - **Location type**: `us-central1`
4. Click **Create Dataset**

---

### Step 3: Create the Table

1. At the top of the BigQuery interface, click the **Untitled query** tab
2. Open `schema.sql` from this repository and copy its entire contents
3. Paste the contents into the query tab

> [!IMPORTANT]
> Before running the query, replace the table reference `` `suggestion_box.suggestions` `` with your actual project ID and dataset, following this format:
> `` `your-project-id.suggestion_box.suggestions` ``
>
> For example, if your project ID is `mgmt54500-jsmith`, the CREATE TABLE statement should read:
> ```sql
> CREATE TABLE IF NOT EXISTS `mgmt54500-jsmith.suggestion_box.suggestions` (
> ```

4. Click **Run**
5. Verify that a `suggestions` table appears under `suggestion_box` in the Explorer pane

---

## Part 2: Fork and Clone the Repository

### Step 4: Fork This Repository

Forking creates your own personal copy of this repository under your GitHub account. All of your work for this project will live in your fork.

1. Click the **Fork** button at the top right of this page
2. Leave all settings at their defaults and click **Create fork**
3. You should now be looking at `your-github-username/suggestion_box` — confirm that the URL includes your username

---

### Step 5: Clone Your Fork in Cloud Shell

1. Open [Google Cloud Shell](https://shell.cloud.google.com)
2. Click the **Code** button on your forked repository page and copy the HTTPS clone URL
3. In the Cloud Shell terminal, run:

```bash
git clone YOUR_FORK_URL
```

4. Navigate into the project directory:

```bash
cd suggestion_box
```

---

## Part 3: Configure and Run the API

### Step 6: Open the Project in Cloud Shell Editor

1. Click the **Open Editor** button (pencil icon) in the Cloud Shell toolbar
2. In the editor's Explorer pane, click **File → Open Folder** and navigate to the `suggestion_box` directory you cloned, then click **OK**
3. You should see the following files in the Explorer pane:

```
suggestion_box/
├── main.py             ← Your FastAPI application
├── pyproject.toml      ← Poetry dependencies
├── Dockerfile          ← Container build instructions
└── schema.sql          ← Reference copy of the table definition
```

---

### Step 7: Install Dependencies

In the Cloud Shell terminal, run:

```bash
poetry install
```

Poetry will read `pyproject.toml` and install FastAPI, Uvicorn, and the BigQuery client library.

---

### Step 8: Update Your Project ID

1. Open `main.py` in the Cloud Shell Editor
2. Find this line near the top of the file:

```python
PROJECT_ID = "your-project-id"
```

3. Replace `your-project-id` with your actual Google Cloud project ID — the same one you used in the BigQuery steps above

> [!TIP]
> You can find your project ID in the [Google Cloud Console](https://console.cloud.google.com) project selector at the top of the page. It looks something like `mgmt54500-jsmith`.

---

### Step 9: Test Locally

Before you can test locally, Cloud Shell needs to know which Google Cloud project to use when connecting to BigQuery.

1. In the Cloud Shell terminal, set your active project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with your actual project ID — the same value you put in `main.py`.

2. Start the development server:

```bash
poetry run uvicorn main:app --reload --port 8080
```

3. Click the **Web Preview** button (the eye icon in the Cloud Shell toolbar) and select **Preview on port 8080**
4. In the browser tab that opens, add `/suggestions` to the URL

You should see an empty JSON array (`[]`) since the table has no data yet. If you see an authentication error, confirm that your `PROJECT_ID` in `main.py` matches the project you set with `gcloud config set project`.

5. Press `Ctrl+C` in the terminal to stop the server

---

### Step 10: Connect Cloud Run to GitHub

This step creates the Cloud Build trigger and Cloud Run service that will automatically deploy your API whenever you push to GitHub. You only need to do this once.

1. In the [Google Cloud Console](https://console.cloud.google.com), search for **Cloud Run** and select **Services**
2. Click **+ Create Service**
3. Select **Continuously deploy from a repository (source or function)**
4. Click **Set up with Cloud Build**
5. Under **Repository provider**, select **GitHub** and click **Authenticate** — authorize Google Cloud Build to access your GitHub account when prompted
6. Under **Repository**, search for and select your forked repository (`your-github-username/suggestion_box`)
7. Click **Next**
8. Under **Branch**, leave the default (`^main$`)
9. Under **Build type**, select **Dockerfile** — leave the Dockerfile location as `/Dockerfile`
10. Click **Save**
11. Back on the service configuration screen, fill in the following:
    - **Service name**: `suggestion-box`
    - **Region**: `us-central1`
    - **Authentication**: Allow unauthenticated invocations
12. Click **Create**

Cloud Build will trigger an initial deployment. This may take a few minutes. Once it completes, you will see a green checkmark and a live URL at the top of the service page.

> [!NOTE]
> If you see a build error on the first deploy, it is likely because `your-project-id` was not replaced in `main.py` before pushing. Update the file, commit, and push again — Cloud Build will automatically trigger a new deployment.

---

### Step 11: Push to GitHub and Deploy

Now that Cloud Run is connected to your repository, every push to `main` will automatically trigger a new deployment.

1. Stage your changes:

```bash
git add .
```

2. Commit with a descriptive message:

```bash
git commit -m "Configure project ID for BigQuery connection"
```

3. Push to your fork:

```bash
git push
```

4. In the [Google Cloud Console](https://console.cloud.google.com), search for **Cloud Build** and confirm that a new build has triggered
5. Once the build finishes, search for **Cloud Run** and click on **suggestion-box**

> [!NOTE]
> The service is deployed, but visiting `/suggestions` may return a permissions error at this point. The deployed API runs under the default service account, which does not have permission to query BigQuery. Complete Step 12 to fix this, then return here to verify the live URL.

---

### Step 12: Add Your Service Account to Cloud Run

Now that your service exists in Cloud Run, assign it the service account that has permission to query BigQuery. The Cloud Run service must exist before this step can be completed — that is why it comes after the first deployment.

> [!NOTE]
> You are not creating a new service account — you are reusing the one you created in a previous assignment (`fastapi-bq-accessor`).

1. In the [Google Cloud Console](https://console.cloud.google.com), search for **Cloud Run** and select **Services**
2. Click on **suggestion-box**
3. At the top of the screen, click **✏️ Edit & deploy new revision**
4. Select the **Security** tab
5. In the **Service account** dropdown, choose `fastapi-bq-accessor`
6. Click **Deploy**
7. Once the new revision has deployed, click the service URL at the top of the page and append `/suggestions` — you should see an empty JSON array, confirming the API can reach BigQuery

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/suggestions` | Returns all suggestions, newest first |
| `GET` | `/suggestions/{id}` | Returns a single suggestion by UUID (404 if not found) |
| `POST` | `/suggestions` | Creates a new suggestion; returns the created record |

**POST body example:**

```json
{
  "category": "Technology",
  "message": "Please update the projector software."
}
```

`category` must be one of: `"Facilities"`, `"Technology"`, `"General"`.

The interactive API documentation is available at `/docs` on both your local server and your deployed Cloud Run URL.
