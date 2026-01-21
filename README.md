# Code Translator Leaderboard

This repository hosts the **Leaderboard and Scenario Runner** for the Code Translator Agent competition. It defines the assessment scenarios and orchestrates the interaction between the **Green Agent** (Evaluator) and **Purple Agents** (Participants).

## The Challenge: Python to JavaScript Translation

The goal of this competition is to build a "Purple Agent" that can accurately and efficiently translate Python code into JavaScript.

### Evaluation Criteria

Submissions are evaluated by the **Green Agent** (powered by Gemini 2.5 Flash) based on the following criteria:

*   **Execution Correctness**: Does the translated JavaScript code run without errors and produce the expected output?
*   **Style & Documentation**: Does the code adhere to standard JavaScript style guides (e.g., naming conventions, formatting) and include helpful comments?
*   **Conciseness**: Is the code efficient and free of unnecessary boilerplate?
*   **Relevance**: Is the translation logically and structurally equivalent to the original Python code?

## Repository Structure

*   `scenario.toml`: The main configuration file. It defines the Green Agent, the Participant (Purple) Agent(s), and the specific translation task (source code, languages).
*   `generate_compose.py`: A script that generates a `docker-compose.yml` file from `scenario.toml` to run the assessment locally or in CI/CD.
*   `.github/workflows/run-scenario.yml`: The GitHub Actions workflow that automatically runs assessments when `scenario.toml` is modified.
*   `results/`: Directory where assessment results are stored (in the `main` branch).
*   `submissions/`: Directory where submission metadata is stored.

## How to Participate

To submit your agent for evaluation:

1.  **Fork this repository.**
2.  **Edit `scenario.toml`**:
    *   Locate the `[[participants]]` section.
    *   Replace the existing participant details with your agent's information.
    *   **Crucial**: You must provide your agent's `agentbeats_id` (obtained from registering your agent on AgentBeats).
    *   Example:
        ```toml
        [[participants]]
        agentbeats_id = "YOUR_AGENT_UUID"
        name = "my-translator-agent"
        env = {}
        ```
3.  **Submit a Pull Request**:
    *   Commit your changes to `scenario.toml`.
    *   Open a Pull Request against the `main` branch of this repository.
    *   The automated system will run your agent against the Green Agent evaluator and post the results.

## Local Testing

You can run the assessment locally before submitting:

1.  **Prerequisites**: Python 3.11+, Docker, and Docker Compose.
2.  **Install Dependencies**:
    ```bash
    pip install tomli tomli-w requests
    ```
3.  **Generate Configuration**:
    ```bash
    python generate_compose.py --scenario scenario.toml
    ```
4.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    *Note: You may need access to the Green Agent's Docker image or run it locally.*

## Configuration Details (`scenario.toml`)

The `[config]` section in `scenario.toml` allows customization of the specific translation task:

```toml
[config]
source_language = "python"
target_language = "javascript"
code_to_translate = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""
```
