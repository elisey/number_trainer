// Number Trainer Web Application JavaScript
// Handles UI interactions and API communication

class NumberTrainerApp {
    constructor() {
        this.currentExercise = null;
        this.currentDifficulty = 1;
        this.startTime = null;
        this.isMobile = this.detectMobile();
        this.userTriggeredAction = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupMobileEnhancements();
        this.updateStats();
        this.showWelcome();
    }

    detectMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    setupMobileEnhancements() {
        if (!this.isMobile) return;

        // Add touch feedback to all buttons
        document.querySelectorAll('.btn').forEach(btn => {
            this.addTouchFeedback(btn);
        });

        // Enhance input experience on mobile
        this.enhanceInputExperience();

        // Add swipe gestures
        this.setupSwipeGestures();
    }

    addTouchFeedback(element) {
        element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: true });
        element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: true });
    }

    handleTouchStart(e) {
        // Haptic feedback if available
        if (navigator.vibrate) {
            navigator.vibrate(10); // Subtle vibration
        }

        // Visual feedback
        e.currentTarget.style.transform = 'scale(0.98)';
        e.currentTarget.style.opacity = '0.8';
    }

    handleTouchEnd(e) {
        // Reset visual state
        setTimeout(() => {
            e.currentTarget.style.transform = '';
            e.currentTarget.style.opacity = '';
        }, 100);
    }

    enhanceInputExperience() {
        const answerInput = document.getElementById('answer-input');
        if (!answerInput) return;

        // Prevent keyboard zoom on iOS
        answerInput.addEventListener('focus', () => {
            if (this.isIOS()) {
                document.querySelector('meta[name=viewport]').setAttribute('content',
                    'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
            }
        });

        answerInput.addEventListener('blur', () => {
            if (this.isIOS()) {
                document.querySelector('meta[name=viewport]').setAttribute('content',
                    'width=device-width, initial-scale=1.0, user-scalable=no');
            }
        });

        // Force keyboard to open on mobile when input is shown
        answerInput.addEventListener('touchstart', (e) => {
            if (this.isMobile) {
                e.target.focus();
                e.target.click();
            }
        });

        // Better numeric input handling
        answerInput.addEventListener('input', (e) => {
            // Force numeric input and allow negative numbers
            const value = e.target.value.replace(/[^0-9-]/g, '');
            if (value !== e.target.value) {
                e.target.value = value;
            }
        });
    }

    setupSwipeGestures() {
        let startX = null;
        let startY = null;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;

            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;

            const diffX = startX - endX;
            const diffY = startY - endY;

            // Only trigger if swipe is more horizontal than vertical
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                const exerciseScreen = document.getElementById('exercise-screen');
                const resultScreen = document.getElementById('result-screen');

                // Swipe left (next) on result screen
                if (diffX > 0 && !resultScreen.classList.contains('hidden')) {
                    this.nextExercise();
                }
                // Swipe right (back) on exercise screen
                else if (diffX < 0 && !exerciseScreen.classList.contains('hidden')) {
                    this.showWelcome();
                }
            }

            startX = null;
            startY = null;
        }, { passive: true });
    }

    isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent);
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
            const focusInput = () => {
                const answerInput = document.getElementById('answer-input');
                if (!answerInput) return;

                // Only auto-focus if this was triggered by user action
                if (this.userTriggeredAction && this.isMobile) {
                    // Force focus and keyboard on mobile
                    answerInput.focus();

                    // For iOS devices, use different approach
                    if (this.isIOS()) {
                        // Create a fake click event to trigger keyboard
                        const event = new Event('click', { bubbles: true });
                        answerInput.dispatchEvent(event);
                    } else {
                        // For Android, try multiple methods
                        answerInput.click();
                        answerInput.select();
                    }

                    this.userTriggeredAction = false; // Reset flag
                } else if (!this.isMobile) {
                    // Auto-focus works fine on desktop
                    answerInput.focus();
                }
            };

            // Use requestAnimationFrame for better timing
            requestAnimationFrame(() => {
                setTimeout(focusInput, 100);
            });
        }
    }

    showWelcome() {
        this.showScreen('welcome-screen');
        this.currentExercise = null;
    }

    async startTraining(difficulty) {
        this.currentDifficulty = difficulty;
        this.userTriggeredAction = true; // Mark as user-triggered action
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
        this.userTriggeredAction = true; // Mark as user-triggered action
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
