// Navbar scroll effect - adds/removes 'scrolled' class based on scroll position
// This creates a visual effect when user scrolls down the page
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('mainNavbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Scroll to top button logic
const scrollToTopBtn = document.getElementById('scrollToTopBtn');
window.addEventListener('scroll', function() {
    if (window.scrollY > 200) {
        scrollToTopBtn.classList.add('show');
    } else {
        scrollToTopBtn.classList.remove('show');
    }
});
scrollToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});


// Login page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePasswordBtn = document.getElementById('togglePassword');
    if (togglePasswordBtn) {
        togglePasswordBtn.addEventListener('click', function() {
            const password = document.getElementById('password');
            const icon = this.querySelector('i');
            
            if (password.type === 'password') {
                password.type = 'text';
                icon.classList.remove('bi-eye-fill');
                icon.classList.add('bi-eye-slash-fill');
            } else {
                password.type = 'password';
                icon.classList.remove('bi-eye-slash-fill');
                icon.classList.add('bi-eye-fill');
            }
        });
    }

    // Login form validation
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields');
                return false;
            }
        });
    }

    // Registration page functionality
    const registerForm = document.querySelector('.register-form');
    if (registerForm) {
        // Toggle confirm password visibility
        const toggleConfirmPasswordBtn = document.getElementById('toggleConfirmPassword');
        if (toggleConfirmPasswordBtn) {
            toggleConfirmPasswordBtn.addEventListener('click', function() {
                const confirmPassword = document.getElementById('confirmPassword');
                const icon = this.querySelector('i');
                
                if (confirmPassword.type === 'password') {
                    confirmPassword.type = 'text';
                    icon.classList.remove('bi-eye-fill');
                    icon.classList.add('bi-eye-slash-fill');
                } else {
                    confirmPassword.type = 'password';
                    icon.classList.remove('bi-eye-slash-fill');
                    icon.classList.add('bi-eye-fill');
                }
            });
        }

        // Password strength checker
        const passwordInput = document.getElementById('password');
        const strengthFill = document.getElementById('strengthFill');
        const strengthText = document.getElementById('strengthText');
        
        if (passwordInput && strengthFill && strengthText) {
            passwordInput.addEventListener('input', function() {
                const password = this.value;
                const strength = checkPasswordStrength(password);
                
                // Update strength bar
                strengthFill.className = 'strength-fill ' + strength.level;
                
                // Update strength text
                strengthText.textContent = strength.message;
                strengthText.className = 'strength-text ' + strength.level;
            });
        }

        // Registration form validation
        registerForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
            
            // Reset validation states
            resetValidation();
            
            let isValid = true;
            
            // Email validation
            if (!email || !isValidEmail(email)) {
                showError('email', 'Please enter a valid email address');
                isValid = false;
            }
            
            // Username validation
            if (!username || username.length < 3) {
                showError('username', 'Username must be at least 3 characters long');
                isValid = false;
            }
            
            // Password validation
            if (!password || password.length < 8) {
                showError('password', 'Password must be at least 8 characters long');
                isValid = false;
            }
            
            // Confirm password validation
            if (password !== confirmPassword) {
                showError('confirmPassword', 'Passwords do not match');
                isValid = false;
            }
            
            // Terms agreement validation
            if (!agreeTerms) {
                showError('agreeTerms', 'You must agree to the terms and conditions');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                return false;
            }
        });
    }
});

// Password strength checker function
function checkPasswordStrength(password) {
    let score = 0;
    let feedback = [];
    
    if (password.length >= 8) score++;
    if (password.match(/[a-z]/)) score++;
    if (password.match(/[A-Z]/)) score++;
    if (password.match(/[0-9]/)) score++;
    if (password.match(/[^a-zA-Z0-9]/)) score++;
    
    if (score < 2) {
        return { level: 'weak', message: 'Weak password' };
    } else if (score < 3) {
        return { level: 'fair', message: 'Fair password' };
    } else if (score < 5) {
        return { level: 'good', message: 'Good password' };
    } else {
        return { level: 'strong', message: 'Strong password' };
    }
}

// Email validation function
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Show error function
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.classList.add('is-invalid');
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
}

// Reset validation function
function resetValidation() {
    const fields = document.querySelectorAll('.form-control');
    fields.forEach(field => {
        field.classList.remove('is-invalid', 'is-valid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    });
}