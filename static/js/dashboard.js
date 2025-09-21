// Dashboard JavaScript functionality

let currentSection = 'dashboard';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    setupEventListeners();
});

function setupEventListeners() {
    // Resume upload form
    document.getElementById('resume-upload-form').addEventListener('submit', handleResumeUpload);
    
    // JD upload form
    document.getElementById('jd-upload-form').addEventListener('submit', handleJDUpload);
    
    // File input changes
    document.getElementById('resume-file').addEventListener('change', handleFileSelect);
    document.getElementById('jd-file').addEventListener('change', handleFileSelect);
    
    // Drag and drop
    setupDragAndDrop();
}

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    document.getElementById(sectionName + '-section').style.display = 'block';
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
    
    currentSection = sectionName;
    
    // Load section-specific data
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'evaluate':
            loadEvaluateData();
            break;
        case 'results':
            loadResults();
            break;
    }
}

async function loadDashboard() {
    try {
        // Load stats
        const [resumes, jds, evaluations] = await Promise.all([
            fetch('/resumes').then(r => r.json()),
            fetch('/job-descriptions').then(r => r.json()),
            fetch('/evaluations').then(r => r.json())
        ]);
        
        // Update stats
        document.getElementById('total-resumes').textContent = resumes.length;
        document.getElementById('total-jds').textContent = jds.length;
        document.getElementById('total-evaluations').textContent = evaluations.length;
        
        const highScores = evaluations.filter(e => e.verdict === 'High').length;
        document.getElementById('high-scores').textContent = highScores;
        
        // Update recent evaluations
        updateRecentEvaluations(evaluations.slice(0, 5));
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

function updateRecentEvaluations(evaluations) {
    const container = document.getElementById('recent-evaluations');
    
    if (evaluations.length === 0) {
        container.innerHTML = '<p class="text-muted">No evaluations yet. Upload resumes and job descriptions to get started.</p>';
        return;
    }
    
    const html = evaluations.map(eval => `
        <div class="d-flex justify-content-between align-items-center border-bottom py-2">
            <div>
                <strong>Resume #${eval.resume_id}</strong>
                <span class="text-muted">vs Job #${eval.job_description_id}</span>
            </div>
            <div class="text-end">
                <span class="badge score-${eval.verdict.toLowerCase()}">${eval.relevance_score}%</span>
                <small class="text-muted d-block">${new Date(eval.created_at).toLocaleDateString()}</small>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

async function handleResumeUpload(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const file = formData.get('file');
    
    if (!file || file.size === 0) {
        showAlert('Please select a file', 'warning');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
        showAlert('File size must be less than 10MB', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/upload/resume', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Resume uploaded successfully!', 'success');
            event.target.reset();
            loadDashboard();
        } else {
            showAlert(result.detail || 'Upload failed', 'danger');
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showAlert('Upload failed. Please try again.', 'danger');
    } finally {
        showLoading(false);
    }
}

async function handleJDUpload(event) {
    event.preventDefault();
    
    console.log('JD Upload form submitted');
    console.log('Form elements:', event.target.elements);
    
    const formData = new FormData(event.target);
    const file = formData.get('file');
    
    console.log('FormData entries:');
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }
    
    console.log('File selected:', file);
    console.log('File size:', file ? file.size : 'No file');
    
    if (!file || file.size === 0) {
        showAlert('Please select a file', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        console.log('Sending request to /upload/job-description');
        
        const response = await fetch('/upload/job-description', {
            method: 'POST',
            body: formData
        });
        
        console.log('Response status:', response.status);
        const result = await response.json();
        console.log('Response result:', result);
        
        if (response.ok) {
            showAlert('Job description uploaded successfully!', 'success');
            event.target.reset();
            loadDashboard();
        } else {
            showAlert(result.detail || 'Upload failed', 'danger');
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showAlert('Upload failed. Please try again.', 'danger');
    } finally {
        showLoading(false);
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const uploadArea = event.target.closest('.upload-area');
        // Don't replace the input, just update the display
        const icon = uploadArea.querySelector('i');
        const title = uploadArea.querySelector('h5');
        const subtitle = uploadArea.querySelector('p');
        
        if (icon) icon.className = 'fas fa-file fa-3x text-success mb-3';
        if (title) title.textContent = file.name;
        if (subtitle) subtitle.textContent = 'File selected successfully';
    }
}

function setupDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', () => {
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = area.querySelector('input[type="file"]');
                fileInput.files = files;
                handleFileSelect({ target: fileInput });
            }
        });
    });
}

async function loadEvaluateData() {
    try {
        const [resumes, jds] = await Promise.all([
            fetch('/resumes').then(r => r.json()),
            fetch('/job-descriptions').then(r => r.json())
        ]);
        
        // Populate resume select
        const resumeSelect = document.getElementById('resume-select');
        resumeSelect.innerHTML = '<option value="">Choose a resume...</option>' +
            resumes.map(r => `<option value="${r.id}">${r.student_name} (${r.student_email})</option>`).join('');
        
        // Populate JD select
        const jdSelect = document.getElementById('jd-select');
        jdSelect.innerHTML = '<option value="">Choose a job description...</option>' +
            jds.map(j => `<option value="${j.id}">${j.title} - ${j.location}</option>`).join('');
        
    } catch (error) {
        console.error('Error loading evaluate data:', error);
        showAlert('Error loading data', 'danger');
    }
}

async function evaluateResume() {
    const resumeId = document.getElementById('resume-select').value;
    const jdId = document.getElementById('jd-select').value;
    
    if (!resumeId || !jdId) {
        showAlert('Please select both resume and job description', 'warning');
        return;
    }
    
    try {
        console.log('Starting evaluation...');
        showLoading(true);
        
        const response = await fetch(`/evaluate/${resumeId}/${jdId}`, {
            method: 'POST'
        });
        
        console.log('Response status:', response.status);
        const result = await response.json();
        console.log('Response result:', result);
        
        if (response.ok) {
            console.log('Evaluation successful, displaying results...');
            displayEvaluationResult(result);
            showAlert('Evaluation completed successfully!', 'success');
        } else {
            console.log('Evaluation failed:', result.detail);
            showAlert(result.detail || 'Evaluation failed', 'danger');
        }
        
    } catch (error) {
        console.error('Evaluation error:', error);
        showAlert('Evaluation failed. Please try again.', 'danger');
    } finally {
        console.log('Hiding loading modal...');
        showLoading(false);
    }
}

function displayEvaluationResult(result) {
    const container = document.getElementById('evaluation-result');
    const scoreClass = getScoreClass(result.verdict);
    
    container.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-line me-2"></i> Advanced Evaluation Result</h5>
            </div>
            <div class="card-body">
                <!-- Main Score and Verdict -->
                <div class="row mb-4">
                    <div class="col-md-4">
                        <div class="text-center">
                            <div class="score-badge score-${scoreClass}">
                                ${result.relevance_score}%
                            </div>
                            <h4 class="mt-2">${result.verdict}</h4>
                            ${result.match_confidence ? `
                                <p class="text-muted">
                                    <i class="fas fa-shield-alt me-1"></i>
                                    ${result.match_confidence} Confidence
                                </p>
                            ` : ''}
                        </div>
                    </div>
                    <div class="col-md-8">
                        <h6><i class="fas fa-chart-bar me-2"></i>Detailed Score Breakdown</h6>
                        <div class="mb-2">
                            <small>Skills Match: ${result.skills_match_score || result.hard_match_score}%</small>
                            <div class="progress">
                                <div class="progress-bar bg-primary" style="width: ${result.skills_match_score || result.hard_match_score}%"></div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <small>Experience Match: ${result.experience_match_score}%</small>
                            <div class="progress">
                                <div class="progress-bar bg-success" style="width: ${result.experience_match_score}%"></div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <small>Semantic Match: ${result.semantic_match_score}%</small>
                            <div class="progress">
                                <div class="progress-bar bg-info" style="width: ${result.semantic_match_score}%"></div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <small>Education Match: ${result.education_match_score}%</small>
                            <div class="progress">
                                <div class="progress-bar bg-warning" style="width: ${result.education_match_score}%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Evaluation Summary -->
                ${result.evaluation_summary ? `
                    <div class="alert alert-info mb-4">
                        <h6><i class="fas fa-info-circle me-2"></i>Evaluation Summary</h6>
                        <p class="mb-0">${result.evaluation_summary}</p>
                    </div>
                ` : ''}
                
                <div class="row">
                    <!-- Missing Skills -->
                    ${result.missing_skills && result.missing_skills.length > 0 ? `
                        <div class="col-md-6 mb-4">
                            <h6><i class="fas fa-exclamation-triangle me-2 text-warning"></i>Missing Critical Skills</h6>
                            <div class="d-flex flex-wrap">
                                ${result.missing_skills.slice(0, 8).map(skill => 
                                    `<span class="badge bg-warning me-2 mb-2">${skill}</span>`
                                ).join('')}
                                ${result.missing_skills.length > 8 ? 
                                    `<span class="badge bg-secondary me-2 mb-2">+${result.missing_skills.length - 8} more</span>` 
                                    : ''
                                }
                            </div>
                        </div>
                    ` : `
                        <div class="col-md-6 mb-4">
                            <div class="alert alert-success">
                                <i class="fas fa-check-circle me-2"></i>
                                <strong>Excellent!</strong> All critical skills are present.
                            </div>
                        </div>
                    `}
                    
                    <!-- Advanced Suggestions -->
                    ${result.suggestions && result.suggestions.length > 0 ? `
                        <div class="col-md-6 mb-4">
                            <h6><i class="fas fa-lightbulb me-2 text-primary"></i>Personalized Recommendations</h6>
                            <div class="list-group">
                                ${result.suggestions.slice(0, 5).map(suggestion => 
                                    `<div class="list-group-item border-0 px-0 py-2">
                                        <small class="text-muted">${suggestion}</small>
                                    </div>`
                                ).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>

                <!-- Advanced Details (Collapsible) -->
                ${result.detailed_analysis ? `
                    <div class="mt-4">
                        <button class="btn btn-outline-secondary btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#advanced-details">
                            <i class="fas fa-cog me-2"></i>View Advanced Analysis
                        </button>
                        <div class="collapse mt-3" id="advanced-details">
                            <div class="card bg-light">
                                <div class="card-body">
                                    <div class="row">
                                        ${result.detailed_analysis.skills_match ? `
                                            <div class="col-md-6">
                                                <h6>Skills Analysis</h6>
                                                <p><small><strong>Skills Matched:</strong> ${result.detailed_analysis.skills_match.skills_matched || 0}/${result.detailed_analysis.skills_match.total_skills_required || 0}</small></p>
                                                ${result.detailed_analysis.skills_match.bonuses ? `
                                                    <p><small><strong>Bonuses Applied:</strong></small></p>
                                                    <ul class="small">
                                                        ${result.detailed_analysis.skills_match.bonuses.good_to_have_bonus > 0 ? 
                                                            `<li>Good-to-have skills: +${(result.detailed_analysis.skills_match.bonuses.good_to_have_bonus * 100).toFixed(1)}%</li>` : ''
                                                        }
                                                        ${result.detailed_analysis.skills_match.bonuses.diversity_bonus > 0 ? 
                                                            `<li>Skill diversity: +${(result.detailed_analysis.skills_match.bonuses.diversity_bonus * 100).toFixed(1)}%</li>` : ''
                                                        }
                                                        ${result.detailed_analysis.skills_match.bonuses.expertise_bonus > 0 ? 
                                                            `<li>Domain expertise: +${(result.detailed_analysis.skills_match.bonuses.expertise_bonus * 100).toFixed(1)}%</li>` : ''
                                                        }
                                                    </ul>
                                                ` : ''}
                                            </div>
                                        ` : ''}
                                        ${result.detailed_analysis.experience_match ? `
                                            <div class="col-md-6">
                                                <h6>Experience Analysis</h6>
                                                <p><small><strong>Experience Level:</strong> ${result.detailed_analysis.experience_match.experience_level?.candidate_level || 'Unknown'}</small></p>
                                                <p><small><strong>Required Level:</strong> ${result.detailed_analysis.experience_match.experience_level?.required_level || 'Unknown'}</small></p>
                                                <p><small><strong>Total Years:</strong> ${result.detailed_analysis.experience_match.total_years || 0}</small></p>
                                            </div>
                                        ` : ''}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
    
    container.style.display = 'block';
}

function getScoreClass(verdict) {
    const verdictMap = {
        'Excellent Match': 'high',
        'Strong Match': 'high', 
        'Good Match': 'medium',
        'Potential Match': 'medium',
        'Moderate Match': 'medium',
        'Weak Match': 'low',
        'Poor Match': 'low',
        'High': 'high',
        'Medium': 'medium',
        'Low': 'low'
    };
    return verdictMap[verdict] || 'low';
}

async function loadResults() {
    try {
        const response = await fetch('/evaluations');
        const evaluations = await response.json();
        
        updateResultsTable(evaluations);
        updateFilters(evaluations);
        
    } catch (error) {
        console.error('Error loading results:', error);
        showAlert('Error loading results', 'danger');
    }
}

function updateResultsTable(evaluations) {
    const tbody = document.getElementById('results-table');
    
    if (evaluations.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No evaluations found</td></tr>';
        return;
    }
    
    const html = evaluations.map(eval => `
        <tr>
            <td>Resume #${eval.resume_id}</td>
            <td>Job #${eval.job_description_id}</td>
            <td>
                <span class="badge score-${eval.verdict.toLowerCase()}">${eval.relevance_score}%</span>
            </td>
            <td>
                <span class="badge bg-${getVerdictColor(eval.verdict)}">${eval.verdict}</span>
            </td>
            <td>${new Date(eval.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewEvaluationDetails(${eval.id})">
                    <i class="fas fa-eye"></i> View
                </button>
            </td>
        </tr>
    `).join('');
    
    tbody.innerHTML = html;
}

function updateFilters(evaluations) {
    // Update JD filter
    const jdFilter = document.getElementById('filter-jd');
    const jdIds = [...new Set(evaluations.map(e => e.job_description_id))];
    jdFilter.innerHTML = '<option value="">All</option>' +
        jdIds.map(id => `<option value="${id}">Job #${id}</option>`).join('');
}

async function applyFilters() {
    const jdId = document.getElementById('filter-jd').value;
    const minScore = document.getElementById('filter-score').value;
    const verdict = document.getElementById('filter-verdict').value;
    
    let url = '/evaluations?';
    const params = [];
    
    if (jdId) params.push(`jd_id=${jdId}`);
    if (minScore) params.push(`min_score=${minScore}`);
    if (verdict) params.push(`verdict=${verdict}`);
    
    url += params.join('&');
    
    try {
        const response = await fetch(url);
        const evaluations = await response.json();
        updateResultsTable(evaluations);
    } catch (error) {
        console.error('Error applying filters:', error);
        showAlert('Error applying filters', 'danger');
    }
}

async function viewEvaluationDetails(evaluationId) {
    try {
        const response = await fetch(`/evaluation/${evaluationId}`);
        const data = await response.json();
        
        const modal = new bootstrap.Modal(document.getElementById('evaluationModal'));
        const content = document.getElementById('evaluation-detail-content');
        
        content.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6>Resume Information</h6>
                    <p><strong>Name:</strong> ${data.resume.student_name}</p>
                    <p><strong>Email:</strong> ${data.resume.student_email}</p>
                </div>
                <div class="col-md-6">
                    <h6>Job Description</h6>
                    <p><strong>Title:</strong> ${data.job_description.title}</p>
                    <p><strong>Location:</strong> ${data.job_description.location}</p>
                </div>
            </div>
            
            <hr>
            
            <div class="text-center mb-4">
                <div class="score-badge score-${data.evaluation.verdict.toLowerCase()}">
                    ${data.evaluation.relevance_score}%
                </div>
                <h4 class="mt-2">${data.evaluation.verdict} Suitability</h4>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <h6>Score Breakdown</h6>
                    <div class="mb-2">
                        <small>Hard Match: ${data.evaluation.evaluation_data.hard_match?.skills_match * 100 || 0}%</small>
                        <div class="progress">
                            <div class="progress-bar" style="width: ${data.evaluation.evaluation_data.hard_match?.skills_match * 100 || 0}%"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6>Missing Skills</h6>
                    <div class="d-flex flex-wrap">
                        ${JSON.parse(data.evaluation.missing_skills || '[]').map(skill => 
                            `<span class="badge bg-warning me-2 mb-2">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <h6>Suggestions</h6>
                <ul class="list-group">
                    ${JSON.parse(data.evaluation.suggestions || '[]').map(suggestion => 
                        `<li class="list-group-item">${suggestion}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
        
        modal.show();
        
    } catch (error) {
        console.error('Error loading evaluation details:', error);
        showAlert('Error loading evaluation details', 'danger');
    }
}

function exportResults() {
    // Simple CSV export functionality
    const table = document.getElementById('results-table');
    const rows = table.querySelectorAll('tr');
    
    let csv = 'Student,Job Title,Score,Verdict,Date\n';
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length > 1) {
            const rowData = Array.from(cells).map(cell => cell.textContent.trim()).join(',');
            csv += rowData + '\n';
        }
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'evaluation_results.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

function showLoading(show) {
    const modalElement = document.getElementById('loadingModal');
    
    if (show) {
        console.log('Showing loading modal...');
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } else {
        console.log('Hiding loading modal...');
        forceCloseModal();
    }
}

function forceCloseModal() {
    console.log('Force closing modal...');
    const modalElement = document.getElementById('loadingModal');
    
    // Get existing modal instance and hide it
    const modal = bootstrap.Modal.getInstance(modalElement);
    if (modal) {
        modal.hide();
    }
    
    // Force remove all modal backdrops and reset body
    setTimeout(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => backdrop.remove());
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        document.body.style.paddingLeft = '';
        
        // Also hide the modal element directly
        modalElement.style.display = 'none';
        modalElement.classList.remove('show');
        
        console.log('Modal force closed');
    }, 100);
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

function getVerdictColor(verdict) {
    const colors = {
        'High': 'success',
        'Medium': 'warning',
        'Low': 'danger'
    };
    return colors[verdict] || 'secondary';
}
