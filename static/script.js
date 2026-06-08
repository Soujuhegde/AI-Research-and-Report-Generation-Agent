document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('newResearchModal');
    const newResearchBtn = document.getElementById('newResearchBtn');
    const closeBtn = document.getElementById('closeModal');
    const submitResearchBtn = document.getElementById('submitResearchBtn');
    const topicInput = document.getElementById('topicInput');
    const instructionsInput = document.getElementById('instructionsInput');
    const loadingIndicator = document.getElementById('loadingIndicator');

    const reportTitle = document.getElementById('reportTitle');
    const reportContentArea = document.getElementById('reportContentArea');
    const tocList = document.getElementById('tocList');
    const citationsList = document.getElementById('citationsList');
    const trustValue = document.getElementById('trustValue');
    const trustProgress = document.getElementById('trustProgress');

    let currentJobId = null;

    // Wire up initial placeholder TOC items for demonstration
    const initialTocItems = document.querySelectorAll('#tocList .toc-item');
    initialTocItems.forEach(item => {
        item.onclick = () => {
            document.querySelectorAll('#tocList .toc-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            // For the placeholder, just scroll to the report area slightly
            reportContentArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
        };
    });

    // Modal Logic
    newResearchBtn.onclick = () => modal.style.display = "block";
    closeBtn.onclick = () => modal.style.display = "none";
    window.onclick = (event) => {
        if (event.target == modal) modal.style.display = "none";
    };

    let gameInterval = null;
    let gameScore = 0;
    let isGameOver = false;

    function startGame() {
        const dino = document.getElementById('dino');
        const obstacle = document.getElementById('obstacle');
        const scoreText = document.getElementById('gameScore');
        const gameContainer = document.getElementById('gameContainer');
        
        gameScore = 0;
        isGameOver = false;
        obstacle.classList.add('move');
        obstacle.style.animationDuration = '1.5s';
        
        const jump = () => {
            if (!dino.classList.contains('jump') && !isGameOver) {
                dino.classList.add('jump');
                setTimeout(() => dino.classList.remove('jump'), 500);
            }
        };
        
        gameContainer.onclick = (e) => {
            if (isGameOver) startGame();
            else jump();
        };

        window.onkeydown = (e) => {
            if (e.code === 'Space' && loadingIndicator.style.display === 'block') {
                e.preventDefault();
                if (isGameOver) startGame();
                else jump();
            }
        };

        gameInterval = setInterval(() => {
            if (isGameOver) return;
            
            let dinoTop = parseInt(window.getComputedStyle(dino).getPropertyValue('top'));
            let obstacleLeft = parseInt(window.getComputedStyle(obstacle).getPropertyValue('left'));
            
            // Basic collision detection
            if (obstacleLeft < 70 && obstacleLeft > 40 && dinoTop >= 80) {
                obstacle.classList.remove('move');
                scoreText.innerText = "Game Over! Score: " + Math.floor(gameScore / 10) + " (Click to restart)";
                isGameOver = true;
            } else {
                gameScore++;
                scoreText.innerText = "Score: " + Math.floor(gameScore / 10);
                
                // Speed up slightly over time
                if (gameScore % 500 === 0) {
                    let currentDur = parseFloat(window.getComputedStyle(obstacle).animationDuration);
                    if (currentDur > 0.8) {
                        obstacle.style.animationDuration = (currentDur - 0.1) + 's';
                    }
                }
            }
        }, 10);
    }

    function stopGame() {
        clearInterval(gameInterval);
        document.getElementById('obstacle').classList.remove('move');
        window.onkeydown = null;
    }

    // Start Research
    submitResearchBtn.onclick = async () => {
        const topic = topicInput.value.trim();
        const instructions = instructionsInput.value.trim();

        if (!topic) {
            alert('Please enter a topic');
            return;
        }

        submitResearchBtn.style.display = 'none';
        loadingIndicator.style.display = 'block';
        startGame(); // Start the mini game!

        try {
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: topic,
                    instructions: instructions,
                    max_iterations: 15
                })
            });

            const data = await response.json();
            currentJobId = data.job_id;
            
            // Poll for status
            pollStatus();

        } catch (error) {
            alert('Failed to start research: ' + error.message);
            resetModal();
        }
    };

    function resetModal() {
        submitResearchBtn.style.display = 'block';
        loadingIndicator.style.display = 'none';
        modal.style.display = 'none';
        stopGame();
    }

    async function pollStatus() {
        if (!currentJobId) return;

        try {
            const response = await fetch(`/api/research/${currentJobId}`);
            const data = await response.json();

            if (data.status === 'complete') {
                renderReport(data.topic, data.result);
                resetModal();
            } else if (data.status === 'failed') {
                alert('Research failed: ' + data.error);
                resetModal();
            } else {
                // Still running
                setTimeout(pollStatus, 3000);
            }
        } catch (error) {
            console.error("Polling error", error);
            setTimeout(pollStatus, 3000);
        }
    }

    let currentReportResult = null;
    let currentTopic = null;

    function renderReport(topic, result) {
        currentReportResult = result;
        currentTopic = topic;
        
        // Render Title
        reportTitle.innerText = topic;

        // Render Markdown content
        if (result.final_report) {
            marked.use({ headerIds: true });
            let htmlContent = marked.parse(result.final_report);

            // Extract sections based on <h2>
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlContent;
            
            const sections = [];
            let currentSection = { title: 'Abstract', elements: [], id: 'sec-abstract' };
            
            Array.from(tempDiv.childNodes).forEach(node => {
                if (node.tagName && node.tagName.toLowerCase() === 'h2') {
                    // Push previous section if it has content
                    if (currentSection.elements.length > 0 || currentSection.title !== 'Abstract') {
                        sections.push(currentSection);
                    }
                    currentSection = { 
                        title: node.innerText, 
                        elements: [node], 
                        id: node.id || 'sec-' + Math.random().toString(36).substr(2, 9) 
                    };
                } else {
                    // Ignore empty text nodes at the start of Abstract
                    if (currentSection.title === 'Abstract' && node.nodeType === 3 && node.textContent.trim() === '') {
                        return;
                    }
                    currentSection.elements.push(node);
                }
            });
            if (currentSection.elements.length > 0) {
                sections.push(currentSection);
            }

            // Render Sections
            reportContentArea.innerHTML = '';
            tocList.innerHTML = '';

            sections.forEach((sec, index) => {
                // Create section container
                const secDiv = document.createElement('div');
                secDiv.className = 'report-section';
                secDiv.id = sec.id;
                secDiv.style.display = index === 0 ? 'block' : 'none'; // Only first is visible
                
                sec.elements.forEach(el => secDiv.appendChild(el));
                reportContentArea.appendChild(secDiv);

                // Create TOC Item
                const li = document.createElement('li');
                li.className = 'toc-item' + (index === 0 ? ' active' : '');
                li.innerText = sec.title;
                
                // Tab switching logic
                li.onclick = () => {
                    // Update active TOC
                    document.querySelectorAll('.toc-item, .toc-subitem').forEach(i => i.classList.remove('active'));
                    li.classList.add('active');
                    
                    // Hide all sections, show target
                    document.querySelectorAll('.report-section').forEach(s => s.style.display = 'none');
                    document.getElementById(sec.id).style.display = 'block';
                };
                
                tocList.appendChild(li);

                // Add sub-items (h3)
                const subheadings = Array.from(secDiv.querySelectorAll('h3'));
                if (subheadings.length > 0) {
                    const subList = document.createElement('ul');
                    subList.className = 'toc-sublist';
                    subheadings.forEach(h3 => {
                        const subLi = document.createElement('li');
                        subLi.className = 'toc-subitem';
                        subLi.innerText = h3.innerText;
                        subLi.onclick = (e) => {
                            e.stopPropagation();
                            // Update active TOC
                            document.querySelectorAll('.toc-item, .toc-subitem').forEach(i => i.classList.remove('active'));
                            subLi.classList.add('active');
                            
                            // Show section
                            document.querySelectorAll('.report-section').forEach(s => s.style.display = 'none');
                            document.getElementById(sec.id).style.display = 'block';
                            
                            // scroll to h3
                            h3.scrollIntoView({behavior: 'smooth', block: 'start'});
                        };
                        subList.appendChild(subLi);
                    });
                    tocList.appendChild(subList);
                }
            });
        }

        // Render Citations
        if (result.sources && result.sources.length > 0) {
            citationsList.innerHTML = '';
            result.sources.forEach((source, index) => {
                const div = document.createElement('div');
                div.className = 'citation-item';
                div.innerHTML = `<a href="${source}" target="_blank">Citation ${index + 1}: ${source}</a>`;
                citationsList.appendChild(div);
            });
        } else {
            citationsList.innerHTML = '<div class="citation-item">No citations found.</div>';
        }

        // Render Trust Score
        if (result.credibility !== null && result.credibility !== undefined) {
            let score = Math.round(result.credibility * 100);
            trustValue.innerText = score;
            trustProgress.style.width = score + '%';
        }
    }

    // Export PDF (Using browser print to save as PDF cleanly)
    document.getElementById('btnExportPDF').onclick = () => {
        window.print();
    };

    // Download Data (JSON)
    document.getElementById('btnDownloadData').onclick = () => {
        if (!currentReportResult) {
            alert('No data available to download yet.');
            return;
        }
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
            topic: currentTopic,
            report: currentReportResult.final_report,
            sources: currentReportResult.sources,
            credibility: currentReportResult.credibility
        }, null, 2));
        
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", currentTopic.replace(/\\s+/g, '_') + "_Data.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    // Share Report
    document.getElementById('btnShareReport').onclick = () => {
        if (navigator.share) {
            navigator.share({
                title: currentTopic || 'Editorial Research Report',
                text: 'Check out this generated research report!',
                url: window.location.href,
            }).catch(console.error);
        } else {
            // Fallback
            prompt("Copy this link to share:", window.location.href);
        }
    };

    // Open modal on load
    modal.style.display = "block";
});
