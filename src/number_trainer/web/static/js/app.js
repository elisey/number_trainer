// Number Trainer Web Application JavaScript
// Handles UI interactions and API communication

class NumberTrainerApp {
    constructor() {
        this.currentExercise = null;
        this.currentDifficulty = 1;
        this.startTime = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStats();
        this.showWelcome();
    }

    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const exerciseScreen = document.getElementById('exercise-screen');
                const resultScreen = document.getElementById('result-screen');

                if (!exerciseScreen.classList.contains('hidden')) {
                    this.checkAnswer();
                } else if (!resultScreen.classList.contains('hidden')) {
                    this.nextExercise();
                }
            } else if (e.key === 'Escape') {
                this.showWelcome();
            } else if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                this.nextExercise();
            }
        });

        // Auto-focus on answer input when exercise screen is shown
        const answerInput = document.getElementById('answer-input');
        answerInput.addEventListener('input', (e) => {
            // Allow only numbers
            e.target.value = e.target.value.replace(/[^0-9-]/g, '');
        });
    }

    showScreen(screenId) {
        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.add('hidden');
        });

        // Show target screen
        document.getElementById(screenId).classList.remove('hidden');

        // Focus on answer input if showing exercise screen
        if (screenId === 'exercise-screen') {
            setTimeout(() => {
                document.getElementById('answer-input').focus();
            }, 100);
        }
    }

    showWelcome() {
        this.showScreen('welcome-screen');
        this.currentExercise = null;
    }

    async startTraining(difficulty) {
        this.currentDifficulty = difficulty;
        await this.generateNewExercise();
    }

    async generateNewExercise() {
        try {
            const response = await fetch('/api/exercise/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    difficulty: this.currentDifficulty
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate exercise');
            }

            this.currentExercise = await response.json();
            this.startTime = Date.now();

            // Display the exercise
            document.getElementById('question').textContent = this.currentExercise.question;
            document.getElementById('answer-input').value = '';

            this.showScreen('exercise-screen');
        } catch (error) {
            console.error('Error generating exercise:', error);
            alert('Error creating exercise. Please try again.');
        }
    }

    async checkAnswer() {
        if (!this.currentExercise) return;

        const answerInput = document.getElementById('answer-input');
        const answer = parseInt(answerInput.value);

        if (isNaN(answer)) {
            alert('Please enter a number');
            answerInput.focus();
            return;
        }

        const timeTaken = this.startTime ? (Date.now() - this.startTime) / 1000 : null;

        try {
            const response = await fetch('/api/exercise/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    exercise_id: this.currentExercise.exercise_id,
                    answer: answer,
                    time_taken: timeTaken
                })
            });

            if (!response.ok) {
                throw new Error('Failed to check answer');
            }

            const result = await response.json();
            this.showResult(result);
            await this.updateStats();
        } catch (error) {
            console.error('Error checking answer:', error);
            alert('Error checking answer. Please try again.');
        }
    }

    showResult(result) {
        const messageEl = document.getElementById('result-message');
        const detailsEl = document.getElementById('result-details');

        messageEl.textContent = result.message;
        messageEl.className = `result-message ${result.correct ? 'correct' : 'incorrect'}`;

        let details = '';
        if (result.time_taken) {
            details += `Time: ${result.time_taken.toFixed(1)} sec`;
        }
        detailsEl.textContent = details;

        this.showScreen('result-screen');
    }

    async nextExercise() {
        await this.generateNewExercise();
    }

    async updateStats() {
        try {
            const response = await fetch('/api/stats');
            if (!response.ok) return;

            const stats = await response.json();

            document.getElementById('stats-total').textContent = stats.total_exercises;
            document.getElementById('stats-correct').textContent = stats.correct_answers;
            document.getElementById('stats-incorrect').textContent = stats.incorrect_answers;
            document.getElementById('stats-accuracy').textContent = `${stats.accuracy.toFixed(1)}%`;
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    }
}

// Global functions for HTML onclick handlers
let app;

function startTraining(difficulty) {
    app.startTraining(difficulty);
}

function checkAnswer() {
    app.checkAnswer();
}

function showWelcome() {
    app.showWelcome();
}

function nextExercise() {
    app.nextExercise();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new NumberTrainerApp();
});
