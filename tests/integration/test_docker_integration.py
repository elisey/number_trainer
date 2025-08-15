"""Integration tests for Docker container."""

import subprocess
import time
from collections.abc import Generator

import pytest
import requests

pytestmark = pytest.mark.integration


def docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


docker_required = pytest.mark.skipif(not docker_available(), reason="Docker is not available or not running")


class DockerContainer:
    """Helper class to manage Docker container lifecycle."""

    def __init__(self, image_name: str, container_name: str, port: int):
        self.image_name = image_name
        self.container_name = container_name
        self.port = port
        self.base_url = f"http://localhost:{port}"

    def build(self) -> None:
        """Build Docker image."""
        result = subprocess.run(["docker", "build", "-t", self.image_name, "."], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to build image: {result.stderr}")

    def start(self) -> None:
        """Start Docker container."""
        # Remove existing container if exists
        subprocess.run(["docker", "rm", "-f", self.container_name], capture_output=True)

        result = subprocess.run(
            ["docker", "run", "--rm", "-d", "-p", f"{self.port}:8000", "--name", self.container_name, self.image_name],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to start container: {result.stderr}")

    def stop(self) -> None:
        """Stop Docker container."""
        subprocess.run(["docker", "stop", self.container_name], capture_output=True)

    def wait_for_health(self, timeout: int = 30) -> None:
        """Wait for container to become healthy."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.base_url}/api/health", timeout=5)
                if response.status_code == 200:
                    return
            except requests.RequestException:
                pass
            time.sleep(1)
        raise TimeoutError("Container did not become healthy within timeout")

    def get_logs(self) -> str:
        """Get container logs."""
        result = subprocess.run(["docker", "logs", self.container_name], capture_output=True, text=True)
        return result.stdout + result.stderr


@pytest.fixture(scope="session")
def docker_container() -> Generator[DockerContainer]:
    """Pytest fixture to manage Docker container lifecycle."""
    if not docker_available():
        pytest.skip("Docker is not available or not running")

    container = DockerContainer(image_name="number-trainer:test", container_name="pytest-test-app", port=8081)

    # Build and start container
    container.build()
    container.start()

    try:
        container.wait_for_health()
        yield container
    finally:
        container.stop()


@docker_required
class TestDockerIntegration:
    """Docker integration tests."""

    def test_health_endpoint(self, docker_container: DockerContainer):
        """Test health endpoint responds correctly."""
        response = requests.get(f"{docker_container.base_url}/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "number-trainer-web"

    def test_main_page_loads(self, docker_container: DockerContainer):
        """Test main page loads correctly."""
        response = requests.get(docker_container.base_url)

        assert response.status_code == 200
        assert "Number Trainer" in response.text
        assert "Select Difficulty" in response.text

    def test_create_exercise_endpoint(self, docker_container: DockerContainer):
        """Test exercise creation endpoint."""
        # Test valid difficulty levels
        for difficulty in [1, 2, 3]:
            response = requests.post(f"{docker_container.base_url}/api/exercise/new", json={"difficulty": difficulty})

            assert response.status_code == 200
            data = response.json()
            assert "exercise_id" in data
            assert "question" in data
            assert "operation" in data
            assert len(data["exercise_id"]) > 0

        # Test invalid difficulty
        response = requests.post(f"{docker_container.base_url}/api/exercise/new", json={"difficulty": 5})
        assert response.status_code == 400

    def test_exercise_workflow(self, docker_container: DockerContainer):
        """Test complete exercise workflow."""
        # Create exercise
        create_response = requests.post(f"{docker_container.base_url}/api/exercise/new", json={"difficulty": 1})
        assert create_response.status_code == 200

        exercise_data = create_response.json()
        exercise_id = exercise_data["exercise_id"]
        question = exercise_data["question"]

        # Parse question to get correct answer
        # Format: "X + Y" or "X - Y"
        parts = question.split()
        first_num = int(parts[0])
        operation = parts[1]
        second_num = int(parts[2])

        if operation == "+":
            correct_answer = first_num + second_num
        else:  # operation == "-"
            correct_answer = first_num - second_num

        # Submit correct answer
        answer_response = requests.post(
            f"{docker_container.base_url}/api/exercise/check",
            json={"exercise_id": exercise_id, "answer": correct_answer, "time_taken": 5.0},
        )

        assert answer_response.status_code == 200
        answer_data = answer_response.json()
        assert answer_data["correct"] is True
        assert answer_data["correct_answer"] == correct_answer

        # Try to use the same exercise_id again (should fail)
        reuse_response = requests.post(
            f"{docker_container.base_url}/api/exercise/check",
            json={"exercise_id": exercise_id, "answer": correct_answer, "time_taken": 5.0},
        )
        assert reuse_response.status_code == 404

    def test_stats_endpoint(self, docker_container: DockerContainer):
        """Test stats endpoint."""
        # Get initial stats
        initial_response = requests.get(f"{docker_container.base_url}/api/stats")
        assert initial_response.status_code == 200

        initial_stats = initial_response.json()
        assert "total_exercises" in initial_stats
        assert "correct_answers" in initial_stats
        assert "incorrect_answers" in initial_stats
        assert "accuracy" in initial_stats

        # Create and solve an exercise
        create_response = requests.post(f"{docker_container.base_url}/api/exercise/new", json={"difficulty": 1})
        exercise_data = create_response.json()

        # Submit wrong answer
        requests.post(
            f"{docker_container.base_url}/api/exercise/check",
            json={
                "exercise_id": exercise_data["exercise_id"],
                "answer": 999999,  # Obviously wrong
                "time_taken": 3.0,
            },
        )

        # Check updated stats
        updated_response = requests.get(f"{docker_container.base_url}/api/stats")
        updated_stats = updated_response.json()

        assert updated_stats["total_exercises"] >= initial_stats["total_exercises"] + 1
        assert updated_stats["incorrect_answers"] >= initial_stats["incorrect_answers"] + 1

    def test_container_startup_speed(self, docker_container: DockerContainer):
        """Test that container starts quickly (no package reinstallation)."""
        # Stop current container
        docker_container.stop()

        # Start new container and measure time
        start_time = time.time()
        docker_container.start()
        docker_container.wait_for_health(timeout=20)
        startup_time = time.time() - start_time

        # Container should start quickly (under 15 seconds)
        assert startup_time < 15, f"Container took {startup_time:.2f}s to start, expected < 15s"

        # Check logs don't contain package installation
        logs = docker_container.get_logs()
        assert "Downloading" not in logs, "Container is downloading packages on startup"
        assert "Installing" not in logs, "Container is installing packages on startup"

    def test_api_error_handling(self, docker_container: DockerContainer):
        """Test API error handling."""
        # Test invalid exercise ID
        response = requests.post(
            f"{docker_container.base_url}/api/exercise/check",
            json={"exercise_id": "invalid-id", "answer": 42, "time_taken": 1.0},
        )
        assert response.status_code == 404

        # Test malformed request
        response = requests.post(f"{docker_container.base_url}/api/exercise/new", json={"invalid_field": "value"})
        assert response.status_code == 422  # Validation error
