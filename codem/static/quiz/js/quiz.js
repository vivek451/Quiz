Vue.config.devtools = true
var quiz_container = new Vue({
    delimiters: ["[[", "]]"], el: '#quiz-container', data: {
        questions: [],
        quizzesPerPage: 1, //# Assuming you want 10 quizzes per page, adjust as needed
        currentPage: 1, isLoading: true,
        name: null,
        form: {
            isValid: true,
            message: null,
        },
        form_data: {
            name: null,
        }
    }, computed: {
        paginatedQuestions() {
            const startIndex = (this.currentPage - 1) * this.quizzesPerPage;
            const endIndex = startIndex + this.quizzesPerPage;

            return this.questions.slice(startIndex, endIndex);
        }, totalPages() {
            return Math.ceil(this.questions.length / this.quizzesPerPage);
        }
    }, created() {
        fetch('/questions/')
            .then(response => response.json())
            .then(data => {
                this.questions = data;
                this.isLoading = false;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.isLoading = false;
            });
    }, methods: {
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        }, nextPage() {
            if (this.validateForm() && this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        isQuestionVisible(question) {
            return this.paginatedQuestions.includes(question)
        },
        validateForm() {
            this.form.isValid = true;
            this.form.message = null;
            if (!this.form_data.name || !this.form_data.name.trim()) {
                this.form.isValid = false
                this.form.message = "Please fill in your name before proceeding."
                alert(this.form.message);
                return false;
            }
            for (const question of this.paginatedQuestions) {
                if (!question.response) {
                    this.form.isValid = false;
                    this.form.message = `Please answer all questions in this page.`;
                    alert(this.form.message);
                    return false;
                }
            }

            return true;
        }
    }

});