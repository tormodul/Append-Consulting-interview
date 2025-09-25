# Append-Consulting-interview
Repo for interview with Append consulting: MCP solution for consult staffing


This project is a microservices-based application that finds available consultants based on specific criteria and uses a Large Language Model (LLM) to generate a human-readable summary.

The system consists of two services:
* **`consultant-api`**: A simple FastAPI server that provides a static list of consultant data.
* **`llm-tools-api`**: A FastAPI server that fetches data from the first service, filters it based on user queries, and uses the OpenRouter API to generate a summary with an AI model.

---

## Prerequisites

* Docker Desktop must be installed and running on your machine.

---

## How to Run the Project

1.  **Clone the repository (ssh):**
    ```sh
    git clone git@github.com:tormodul/Append-Consulting-interview.git
    cd Append-Consulting-interview
    ```

2.  **Create an environment file:**
    Create a file named `.env` in the root of the project directory.

3.  **Add your API Key:**
    Open the `.env` file and add your OpenRouter API key in the following format:
    ```
    OPENROUTER_API_KEY=your_api_key_goes_here
    ```

4.  **Build and run the containers:**
    From the root directory, run the following command. This will build the images for both services and start them.
    ```sh
    docker compose up --build
    ```
    The `llm-tools-api` will be available on `http://localhost:8001` and the `consultant-api` on `http://localhost:8000`.

---

## Example Usage

You can test the main endpoint using `curl` in your terminal or by visiting the URL in your browser.

**Example Request:**
Find consultants with at least 50% availability who have the skill 'python'.

```sh
curl -X GET "http://localhost:8001/available-consultants/summary?my_availability_percent=50&required_skill=python"
```

**Example Response:**
```json
{
  "summary": "Found 2 consultants with the skill 'python'. Anna K. has 60% availability. Leo T. has 80% availability."
}
```