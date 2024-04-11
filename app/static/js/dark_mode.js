// dark_mode.js

// Function to toggle dark mode
function toggleDarkMode() {
    const element = document.body;
    element.dataset.bsTheme = element.dataset.bsTheme === "light" ? "dark" : "light";

    // Store the dark mode preference in local storage
    const isDarkModeEnabled = element.dataset.bsTheme === "dark";
    localStorage.setItem("darkModeEnabled", JSON.stringify(isDarkModeEnabled));
}

// Function to apply dark mode based on stored preference
function applyDarkModeFromStorage() {
    const isDarkModeEnabled = JSON.parse(localStorage.getItem("darkModeEnabled"));
    const element = document.body;
    if (isDarkModeEnabled) {
        element.dataset.bsTheme = "dark";
    } else {
        element.dataset.bsTheme = "light";
    }
}

// Apply dark mode preference when the page loads
window.addEventListener("DOMContentLoaded", applyDarkModeFromStorage);
