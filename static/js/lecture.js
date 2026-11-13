// YouTube IFrame Player API & Real-time Watch Tracking
let player;
let trackerInterval = null;
let lastReportedTime = 0;

function initPlayer() {
    if (!window.lectureConfig || !window.lectureConfig.videoId) return;
    if (player) return;
    
    player = new YT.Player('youtube-player', {
        videoId: window.lectureConfig.videoId,
        playerVars: {
            rel: 0,
            modestbranding: 1,
            controls: 1,
            enablejsapi: 1,
            origin: window.location.origin
        },
        events: {
            'onStateChange': onPlayerStateChange,
            'onError': onPlayerError
        }
    });
}

function onYouTubeIframeAPIReady() {
    initPlayer();
}

// Fallback if API was already loaded before this script
if (window.YT && window.YT.Player) {
    initPlayer();
}

function onPlayerError(e) {
    console.warn('YouTube Player notice (code ' + e.data + ') for video:', window.lectureConfig.videoId);
    const wrapper = document.querySelector('.video-wrapper');
    if (wrapper && !document.getElementById('yt-fallback-notice')) {
        const notice = document.createElement('div');
        notice.id = 'yt-fallback-notice';
        notice.className = 'alert alert-light border mt-2 d-flex align-items-center justify-content-between p-2 px-3 rounded-pill';
        notice.innerHTML = `<span><i class="bi bi-youtube text-danger me-2"></i>Having trouble playing in embedded mode?</span>
            <a href="https://www.youtube.com/watch?v=${window.lectureConfig.videoId}" target="_blank" class="btn btn-sm btn-outline-danger rounded-pill px-3">
                <i class="bi bi-box-arrow-up-right me-1"></i>Watch on YouTube
            </a>`;
        wrapper.parentNode.insertBefore(notice, wrapper.nextSibling);
    }
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING) {
        if (!trackerInterval) {
            trackerInterval = setInterval(sendWatchProgress, 5000); // Check every 5 seconds
        }
    } else {
        if (trackerInterval) {
            clearInterval(trackerInterval);
            trackerInterval = null;
        }
    }
}

async function sendWatchProgress() {
    if (!player || typeof player.getCurrentTime !== 'function') return;
    
    const currentTime = player.getCurrentTime();
    const duration = player.getDuration();
    
    // Only send if at least 4 seconds have elapsed since last report
    if (Math.abs(currentTime - lastReportedTime) < 4) return;
    lastReportedTime = currentTime;
    
    try {
        const response = await fetch(`/lecture/${window.lectureConfig.lectureId}/progress`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': window.lectureConfig.csrfToken
            },
            body: JSON.stringify({
                watched_seconds: currentTime,
                duration_seconds: duration
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            const pct = data.progress;
            
            // Update UI elements
            const progressBar = document.getElementById('lecture-progress-bar');
            const progressText = document.getElementById('lecture-progress-text');
            const completeBtn = document.getElementById('complete-lecture-btn');
            
            if (progressBar) progressBar.style.width = pct + '%';
            if (progressText) progressText.innerText = pct + '%';
            
            if (pct >= 90.0 && completeBtn) {
                completeBtn.disabled = false;
                completeBtn.classList.remove('btn-secondary');
                completeBtn.classList.add('btn-success');
                completeBtn.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Mark Lecture Complete';
            }
        }
    } catch (err) {
        console.error('Watch progress sync error:', err);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const completeBtn = document.getElementById('complete-lecture-btn');
    if (completeBtn) {
        completeBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`/lecture/${window.lectureConfig.lectureId}/complete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': window.lectureConfig.csrfToken
                    }
                });
                
                const data = await response.json();
                if (response.ok) {
                    // Reload page to reflect unlocked assignment
                    window.location.reload();
                } else {
                    alert(data.error || 'Unable to mark lecture as complete.');
                }
            } catch (err) {
                alert('Network error while completing lecture.');
            }
        });
    }
});
