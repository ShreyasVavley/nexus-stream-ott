const API = window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'https://' + window.location.hostname;

const loadMovies = async () => {
    try {
        const res = await fetch(`${API}/trending`);
        const data = await res.json();
        const grid = document.getElementById('movie-grid');
        grid.innerHTML = data.map(m => `
            <div class="card">
                <div class="title">${m.title}</div>
                <div class="meta">${m.views} Views in last 24h</div>
            </div>
        `).join('');
    } catch (e) {
        console.error("Movie fetch failed:", e);
    }
};

const loadUsers = async () => {
    try {
        const res = await fetch(`${API}/users`);
        const data = await res.json();
        const grid = document.getElementById('user-grid');
        grid.innerHTML = data.map(u => `
            <div class="card">
                <div class="title">${u.name}</div>
                <div class="meta">ID: ${u.id} | ${u.email}</div>
            </div>
        `).join('');
    } catch (e) {
        console.error("User fetch failed:", e);
    }
};

const requestPlay = async () => {
    const userId = document.getElementById('play-user-id').value;
    const contentId = document.getElementById('play-content-id').value;
    const status = document.getElementById('play-status');

    if (!userId || !contentId) {
        status.innerText = "Please enter both User and Movie IDs.";
        status.style.color = "#ff9900";
        return;
    }

    try {
        const res = await fetch(`${API}/play/${userId}/${contentId}`);
        const data = await res.json();
        
        if (res.ok) {
            status.innerText = data.message;
            status.style.color = "#4ade80"; // Emerald Green
        } else {
            status.innerText = data.detail || "Streaming unavailable.";
            status.style.color = "#ff2e35"; // Vibrant Red
        }
    } catch (e) {
        status.innerText = "Connection lost. Try again later.";
        status.style.color = "#ff2e35";
    }
};

// Start the app logic. Focus on user experience.
document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
    loadUsers();
});
