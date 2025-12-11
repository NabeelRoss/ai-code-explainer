document.addEventListener('DOMContentLoaded', () => {
    const codeInput = document.getElementById('codeInput');
    const maxLengthRange = document.getElementById('maxLengthRange');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');

    const placeholderState = document.getElementById('placeholderState');
    const resultContainer = document.getElementById('resultContainer');
    const errorContainer = document.getElementById('errorContainer');

    // Helper function to manage UI state during loading
    const setLoadingState = (isLoading) => {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
            btnText.textContent = 'Analyzing...';
            btnSpinner.classList.remove('hidden');
            
            // Hide results and show placeholder faintly while loading
            resultContainer.classList.add('hidden');
            errorContainer.classList.add('hidden');
            placeholderState.classList.remove('hidden');
            placeholderState.classList.add('opacity-50');
        } else {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
            btnText.textContent = 'Explain Code';
            btnSpinner.classList.add('hidden');
            placeholderState.classList.remove('opacity-50');
        }
    };

    // Helper function to display results
    const displayResult = (isSuccess, message) => {
        placeholderState.classList.add('hidden');
        if (isSuccess) {
            errorContainer.classList.add('hidden');
            resultContainer.textContent = message;
            resultContainer.classList.remove('hidden');
        } else {
            resultContainer.classList.add('hidden');
            errorContainer.textContent = message || "An unknown error occurred.";
            errorContainer.classList.remove('hidden');
        }
    };


    submitBtn.addEventListener('click', async () => {
        const code = codeInput.value;
        const maxLength = maxLengthRange.value;

        // Basic client-side validation
        if (!code || code.trim().length === 0) {
            displayResult(false, "Please enter some code first.");
            return;
        }

        setLoadingState(true);

        try {
            const response = await fetch('/explain', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    code: code,
                    max_length: maxLength
                }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                displayResult(true, data.explanation);
            } else {
                // Handle API reported errors (e.g., code too long)
                displayResult(false, data.error || "Failed to generate explanation.");
            }

        } catch (error) {
            console.error('Network Error:', error);
            displayResult(false, "Network error. Is the Flask server running?");
        } finally {
            setLoadingState(false);
        }
    });
});