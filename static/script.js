const API_BASE_URL = window.location.origin;

// DOM Elements
const totalIncomeEl = document.getElementById('totalIncome');
const totalExpensesEl = document.getElementById('totalExpenses');
const netSavingsEl = document.getElementById('netSavings');
const uploadForm = document.getElementById('uploadForm');
const csvFileInput = document.getElementById('csvFile');
const uploadStatus = document.getElementById('uploadStatus');
const anomaliesList = document.getElementById('anomaliesList');
const anomalyCount = document.getElementById('anomalyCount');

let chartInstance = null;

// Formatter for currency
const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
};

// Fetch and update summary cards
async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/summary`);
        if (!response.ok) return;
        const data = await response.json();
        
        totalIncomeEl.textContent = formatCurrency(data.total_income);
        totalExpensesEl.textContent = formatCurrency(data.total_expenses);
        netSavingsEl.textContent = formatCurrency(data.net_savings);
    } catch (error) {
        console.error("Error loading summary:", error);
    }
}

// Fetch and render spending chart
async function loadChart() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/spending-by-category`);
        if (!response.ok) return;
        const data = await response.json();

        const labels = data.map(item => item.category.toUpperCase());
        const values = data.map(item => item.total_amount);

        const ctx = document.getElementById('spendingChart').getContext('2d');
        
        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#ef4444', '#f59e0b', '#10b981', '#3b82f6', 
                        '#8b5cf6', '#ec4899', '#14b8a6'
                    ],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#f8fafc', font: { family: 'Inter' } }
                    }
                },
                cutout: '70%'
            }
        });
    } catch (error) {
        console.error("Error loading chart:", error);
    }
}

// Fetch and display anomalies
async function loadAnomalies() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/anomalies`);
        if (!response.ok) return;
        const anomalies = await response.json();
        
        anomalyCount.textContent = anomalies.length;
        
        if (anomalies.length === 0) {
            anomaliesList.innerHTML = '<li class="empty-state">No anomalies detected.</li>';
            return;
        }

        anomaliesList.innerHTML = anomalies.map(txn => `
            <li>
                <div class="txn-desc">${txn.description}</div>
                <div class="txn-amount">${formatCurrency(txn.amount)}</div>
                <div class="txn-date">${txn.date} | ${txn.category.toUpperCase()}</div>
            </li>
        `).join('');
    } catch (error) {
        console.error("Error loading anomalies:", error);
    }
}

// Handle file upload
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const file = csvFileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadStatus.textContent = 'Uploading and processing...';
    uploadStatus.className = 'status-msg';

    try {
        const response = await fetch(`${API_BASE_URL}/transactions/upload`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            uploadStatus.textContent = result.message || 'Upload successful!';
            uploadStatus.className = 'status-msg success';
            csvFileInput.value = ''; // clear input
            
            // Reload dashboard data
            refreshDashboard();
        } else {
            uploadStatus.textContent = 'Upload failed. Please ensure it is a valid CSV.';
            uploadStatus.className = 'status-msg error';
        }
    } catch (error) {
        uploadStatus.textContent = 'Network error during upload.';
        uploadStatus.className = 'status-msg error';
    }
});

function refreshDashboard() {
    loadSummary();
    loadChart();
    loadAnomalies();
}

// Initial load
document.addEventListener('DOMContentLoaded', refreshDashboard);
