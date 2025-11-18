document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('login-view');
    const dashboardView = document.getElementById('dashboard-view');
    const loginForm = document.getElementById('login-form');
    const loginError = document.getElementById('login-error');
    const logoutBtn = document.getElementById('logout-btn');
    const feedbackForm = document.getElementById('feedback-form');
    const feedbackSuccess = document.getElementById('feedback-success');

    const API_BASE_URL = '/api';

    // Mock decryption function for display
    const decryptData = (encryptedData) => encryptedData.replace("encrypted_", "");

    // Chart rendering
    let tempChart;
    const renderTempChart = (data) => {
        const ctx = document.getElementById('temp-chart').getContext('2d');
        const decryptedData = Object.entries(data).reduce((acc, [key, value]) => {
            acc[key] = parseFloat(decryptData(value));
            return acc;
        }, {});

        if (tempChart) {
            tempChart.destroy();
        }
        tempChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(decryptedData),
                datasets: [{
                    label: 'Average Temperature (°C)',
                    data: Object.values(decryptedData),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };

    // Fetch and display alerts
    const fetchAlerts = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/alerts`);
            if (!response.ok) throw new Error('Failed to fetch alerts');
            const alerts = await response.json();
            const alertsSection = document.getElementById('alerts-section');
            alertsSection.innerHTML = '';
            alerts.forEach(alert => {
                const alertEl = document.createElement('div');
                alertEl.className = `list-group-item list-group-item-action flex-column align-items-start ${alert.severity === 'High' ? 'list-group-item-danger' : 'list-group-item-warning'}`;
                alertEl.innerHTML = `<div class="d-flex w-100 justify-content-between">
                                        <h6 class="mb-1">${alert.severity} Priority</h6>
                                     </div>
                                     <p class="mb-1">${alert.message}</p>`;
                alertsSection.appendChild(alertEl);
            });
        } catch (error) {
            console.error('Error fetching alerts:', error);
        }
    };

    // Fetch and display climate data
    const fetchClimateData = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/climate-data`);
            if (!response.ok) throw new Error('Failed to fetch climate data');
            const data = await response.json();
            renderTempChart(data.average_temp_region);
        } catch (error) {
            console.error('Error fetching climate data:', error);
        }
    };

    // Show dashboard
    const showDashboard = (role, username) => {
        loginView.style.display = 'none';
        dashboardView.style.display = 'block';
        document.getElementById('user-role').textContent = role;
        document.getElementById('username-display').textContent = username;
        fetchClimateData();
        fetchAlerts();
    };

    // Show login
    const showLogin = () => {
        loginView.style.display = 'block';
        dashboardView.style.display = 'none';
    };

    // Handle login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (data.success) {
                showDashboard(data.role, username);
            } else {
                loginError.textContent = data.message;
                loginError.style.display = 'block';
            }
        } catch (error) {
            loginError.textContent = 'An error occurred. Please try again.';
            loginError.style.display = 'block';
        }
    });

    // Handle logout
    logoutBtn.addEventListener('click', async () => {
        await fetch(`${API_BASE_URL}/auth/logout`, { method: 'POST' });
        showLogin();
    });

    // Handle feedback form
    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackText = document.getElementById('feedback-text').value;
        try {
            const response = await fetch(`${API_BASE_URL}/feedback`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ feedback: feedbackText })
            });
            const data = await response.json();
            if (data.success) {
                feedbackSuccess.textContent = data.message;
                feedbackSuccess.style.display = 'block';
                feedbackForm.reset();
                setTimeout(() => { feedbackSuccess.style.display = 'none'; }, 3000);
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    });

    // Check login status on page load
    const checkLoginStatus = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/status`);
            const data = await response.json();
            if (data.isLoggedIn) {
                showDashboard(data.role, data.username);
            } else {
                showLogin();
            }
        } catch (error) {
            showLogin();
        }
    };

    checkLoginStatus();
});
