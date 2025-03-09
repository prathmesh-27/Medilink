function updateTime() {
    const now = new Date();
    document.getElementById('current-date').textContent = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('current-time').textContent = now.toLocaleTimeString();
    document.getElementById('current-day').textContent = now.toLocaleDateString('en-US', { weekday: 'long' });
}

updateTime(); // Set initial time
setInterval(updateTime, 1000);


function switchTab(tabName) {
    document.querySelectorAll('.content').forEach(content => {
        content.classList.remove('show');
    });
    document.getElementById(tabName).classList.add('show');

    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}