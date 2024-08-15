// USED FOR THE DYNAMIC ADDITION OF BOOKS TO THE LIBRARY

document.addEventListener('DOMContentLoaded', function() {
    const addToLibraryButtons = document.querySelectorAll('.add-to-library');

    addToLibraryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const bookData = {
                title: this.dataset.title,
                author: this.dataset.author,
                categories: this.dataset.categories,
                rating: this.dataset.rating,
                cover_art: this.dataset.cover,
                isbn: this.dataset.isbn,
                pages: this.dataset.pages,
                description: this.dataset.description,
                // Include any other data attributes you need
            };

            const url = this.dataset.url;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is sent; implement getCookie function as needed
                },
                body: JSON.stringify(bookData),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data); // Handle success
                
                // Create the message element
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('alert', 'alert-success', 'mt-3');
                messageDiv.textContent = 'Book added to your library successfully!';
                
                // Append the message to a container in your HTML
                const container = document.querySelector('.message-container'); // Ensure you have a container with this class
                container.innerHTML = ''; // Clear previous messages
                container.appendChild(messageDiv);
                
                // Optionally, remove the message after a few seconds
                setTimeout(() => {
                    messageDiv.remove();
                }, 2000);
            })            
            .catch((error) => {
                console.error('Error:', error); // Handle errors here

                const messageDiv = document.createElement('div');
                messageDiv.classList.add('alert', 'alert-warning', 'mt-3');
                messageDiv.textContent = 'Book could not be added :( Sorry about that';
                
                // Append the message to a container in your HTML
                const container = document.querySelector('.message-container'); // Ensure you have a container with this class
                container.innerHTML = ''; // Clear previous messages
                container.appendChild(messageDiv);
                
                // Optionally, remove the message after a few seconds
                setTimeout(() => {
                    messageDiv.remove();
                }, 2000);
            });
        });
    });
});

// USED GENERALLY

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// FOR THE LIBRARY INTERACTIVITY OF PROGRESS BARS AND ALSO DYNAMIC DATA UPDATES -> CURRENT PAGE

document.addEventListener('DOMContentLoaded', function() {
    // Initialize progress bars on page load
    updateProgressBars();

    // Set up event listeners for saving current page
    document.querySelectorAll('.save-current-page').forEach(button => {
        button.addEventListener('click', function() {
            const bookId = this.dataset.bookId;
            const currentPageInput = document.querySelector(`.current-page-input[data-book-id="${bookId}"]`);
            const currentPage = parseInt(currentPageInput.value, 10);
            const url = this.dataset.url;
            const totalPages = parseInt(currentPageInput.dataset.totalPages, 10);

            // Validate the current page does not exceed total pages
            if (currentPage > totalPages) {
                alert('Current page cannot exceed total pages of the book.');
                currentPageInput.value = totalPages; // Optional: reset input to max allowed value
                event.preventDefault(); // Prevent form submission
                return false; // Stop further execution
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ bookId: bookId, currentPage: currentPage }),
            })
            .then(response => response.json())
            .then(data => {
                displayMessage(data.message, 'success'); // Show success message
                updateProgressBars(); // Refresh progress bars to reflect any changes
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage('An error occurred. Please try again.', 'error'); // Show error message
            });
        });
    });
});

function updateProgressBars() {
    document.querySelectorAll('.current-page-input').forEach(input => {
        const bookId = input.dataset.bookId;
        const currentPage = parseInt(input.value, 10);
        const totalPages = parseInt(input.dataset.totalPages, 10);
        updateProgressBar(bookId, currentPage, totalPages);
    });
}

function updateProgressBar(bookId, currentPage, totalPages) {
    const percentage = (currentPage / totalPages) * 100;
    const progressBar = document.querySelector(`.card[data-book-id="${bookId}"] .progress-bar`);
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute('aria-valuenow', percentage);
        progressBar.textContent = `${percentage.toFixed(0)}%`;
    }
}

function displayMessage(message, type) {
    const messageContainer = document.querySelector('.alert.alert-success');
    const messageDiv = document.getElementById('update-message');
    messageDiv.textContent = message;
    messageContainer.style.display = 'block';
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 3000);
}

document.querySelectorAll('.xp-text').forEach(xp => {
    xp.addEventListener('mouseover', function() {
        // Code to show tooltip
    });

    xp.addEventListener('mouseout', function() {
        // Code to hide tooltip
    });
});


// FOR THE CHART IN PROFILE_DETAIL


document.addEventListener('DOMContentLoaded', function() {
    var xpProgressChartCanvas = document.getElementById('xpProgressChart');
    if (xpProgressChartCanvas) {
        var url = xpProgressChartCanvas.getAttribute('data-url');
        var ctx = xpProgressChartCanvas.getContext('2d');
        fetch(url)
            .then(response => response.json())
            .then(data => {
                var gradient = ctx.createLinearGradient(0, 0, 0, 400);
                gradient.addColorStop(0, 'rgba(255, 99, 132, 0.5)');
                gradient.addColorStop(1, 'rgba(255, 99, 132, 0.0)');
                
                data.datasets.forEach(dataset => {
                    dataset.backgroundColor = gradient;
                    dataset.borderColor = 'rgba(255, 99, 132, 1)';
                    dataset.pointBackgroundColor = 'rgba(255, 99, 132, 1)';
                    dataset.pointHoverBackgroundColor = 'rgba(255, 99, 132, 1)';
                    dataset.pointHoverBorderColor = 'rgba(255, 255, 255, 1)';
                    dataset.borderWidth = 2;
                    dataset.pointBorderWidth = 2;
                    dataset.pointHoverRadius = 6;
                });

                var xpProgressChart = new Chart(ctx, {
                    type: 'line',
                    data: data,
                    options: {
                        scales: {
                            y: {  
                                beginAtZero: true
                            }
                        },
                        plugins: {
                            tooltip: {
                                mode: 'index',
                                intersect: false,
                                bodySpacing: 8,
                                titleMarginBottom: 10,
                                titleFontSize: 14,
                                bodyFontSize: 12,
                                backgroundColor: 'rgba(0,0,0,0.8)'
                            },
                            legend: {
                                labels: {
                                    color: '#fff'
                                }
                            }
                        },
                        responsive: true,
                        maintainAspectRatio: false,
                        elements: {
                            line: {
                                tension: 0.4 // Smoothens the line
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error loading XP progress data:', error));
    }
});

// FOR THE PROGRESS BAR IN PROFILE_DETAIL

$(document).ready(function() {
    var progressPercentage = $('#userProgress').attr('aria-valuenow');
    progressPercentage = parseInt(progressPercentage, 10);

    if (!isNaN(progressPercentage)) {
        $('#userProgress').animate({
            width: progressPercentage + '%'
        }, 1000, function() { // Reduced to 500 milliseconds for a faster animation
            $(this).text(progressPercentage + '%');
        });
    }
});

function updateProgress(newProgressPercentage) {
    newProgressPercentage = parseInt(newProgressPercentage, 10);

    if (!isNaN(newProgressPercentage)) {
        $('#userProgress').animate({
            width: newProgressPercentage + '%'
        }, 1000, function() { // Again, reduced to 500 milliseconds for consistency
            $(this).attr('aria-valuenow', newProgressPercentage).text(newProgressPercentage + '%');
        });
    }
}

// FOR THE PROFILE INDEX PAGE
document.addEventListener("DOMContentLoaded", function() {
    // Add interactivity, like animations or dynamic content changes here
    // Example: Animate list group items on hover
    const listItems = document.querySelectorAll('.list-group-item');

    listItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.transform = "scale(1.05)";
            item.style.transition = "transform 0.5s ease";
        });
        item.addEventListener('mouseleave', () => {
            item.style.transform = "scale(1)";
        });
    });
});

// SCRIPT FOR PUSHER CHAT FUNCTIONALITY
document.addEventListener('DOMContentLoaded', function() {
    var threadIdElement = document.getElementById('threadId');
    if (threadIdElement) {
        var pusher = new Pusher(window.PUSHER_KEY, {
            cluster: window.PUSHER_CLUSTER,
            encrypted: true
        });

        var threadId = threadIdElement.value;
        var channel = pusher.subscribe('thread-' + threadId);

        // Listen for new post events
        channel.bind('new-post', function(data) {
            var messagesList = document.getElementById('messages-list');
            if (messagesList) {
                var newPost = document.createElement('div');
                newPost.className = 'list-group-item list-group-item-action flex-column align-items-start';
                newPost.innerHTML = `
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">Posted by ${data.username}</h5>
                        <small>${new Date(data.created_at).toLocaleString()}</small>
                    </div>
                    <p class="mb-1">${data.message}</p>
                `;
                messagesList.appendChild(newPost);
            }
        });

        var sendButton = document.getElementById('chat-message-submit');
        var messageInput = document.getElementById('chat-message-input');

        if (sendButton && messageInput) {
            sendButton.addEventListener('click', function(event) {
                event.preventDefault(); 
                var message = messageInput.value.trim();
                if (message) {
                    // send message via AJAX to the server
                    fetch(`/forum/thread/${threadId}/create_post/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
                        },
                        body: JSON.stringify({ message: message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            messageInput.value = ''; 
                        } else {
                            console.error('Failed to send message:', data.error);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            });
        }
    } else {
        console.error('Element with ID threadId not found.');
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
