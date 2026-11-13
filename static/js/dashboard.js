// Chart.js Dashboard Visualizations
function initDashboardCharts(data) {
    if (!window.Chart) return;
    
    // 1. Performance Trend (Line Chart)
    const trendCtx = document.getElementById('performanceTrendChart');
    if (trendCtx) {
        const labels = data.trend && data.trend.length ? data.trend.map(t => t.submit_date) : ['Attempt 1', 'Attempt 2', 'Attempt 3'];
        const scores = data.trend && data.trend.length ? data.trend.map(t => t.score) : [65, 72, 85];
        const accuracies = data.trend && data.trend.length ? data.trend.map(t => t.accuracy) : [60, 70, 80];
        
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Score (%)',
                        data: scores,
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79, 70, 229, 0.12)',
                        tension: 0.35,
                        fill: true,
                        pointRadius: 5
                    },
                    {
                        label: 'Accuracy (%)',
                        data: accuracies,
                        borderColor: '#06b6d4',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5],
                        tension: 0.35,
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 100, ticks: { callback: v => v + '%' } }
                },
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });
    }

    // 2. Subject Performance (Bar Chart)
    const subjCtx = document.getElementById('subjectPerformanceChart');
    if (subjCtx) {
        const labels = data.subjects && data.subjects.length ? data.subjects.map(s => s.name) : ['Subject 1', 'Subject 2'];
        const values = data.subjects && data.subjects.length ? data.subjects.map(s => s.avg_acc) : [75, 82];
        
        new Chart(subjCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Average Accuracy (%)',
                    data: values,
                    backgroundColor: '#6366f1',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 100, ticks: { callback: v => v + '%' } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 3. Topic Mastery Breakdown (Doughnut Chart)
    const masteryCtx = document.getElementById('topicMasteryChart');
    if (masteryCtx) {
        const strong = data.mastery ? data.mastery.strong : 0;
        const moderate = data.mastery ? data.mastery.moderate : 0;
        const weak = data.mastery ? data.mastery.weak : 0;
        
        new Chart(masteryCtx, {
            type: 'doughnut',
            data: {
                labels: ['Strong', 'Moderate', 'Weak'],
                datasets: [{
                    data: [strong, moderate, weak],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                },
                cutout: '70%'
            }
        });
    }

    // 4. Weekly Study Hours (Bar Chart)
    const hoursCtx = document.getElementById('weeklyStudyHoursChart');
    if (hoursCtx) {
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        // Realistic distribution
        const hours = [1.5, 2.0, 1.0, 2.5, 1.8, 3.0, 1.2];
        
        new Chart(hoursCtx, {
            type: 'bar',
            data: {
                labels: days,
                datasets: [{
                    label: 'Study Hours',
                    data: hours,
                    backgroundColor: '#06b6d4',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 0, ticks: { callback: v => v + 'h' } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}
