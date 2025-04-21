// JavaScript will be added here
// Initialize the map
const map = L.map('map').setView([18.554499, 73.825729], 13); // Set to Pune University Coordinates 

// Add the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Variables to store markers and search radius
let locationMarkers = [];
let imageMarkers = [];
let searchCircle = null;
let currentSearchPoint = null;
const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));

// Add event listener for map clicks
map.on('click', function(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;
    
    // Set this as the current search point
    currentSearchPoint = {lat, lng};
    
    // Get the radius from input
    const radius = parseFloat(document.getElementById('radiusInput').value);
    
    // Search for locations and images
    searchByCoordinates(lat, lng, radius);
});

// Search button click handler
document.getElementById('searchCenterBtn').addEventListener('click', function() {
    const center = map.getCenter();
    const radius = parseFloat(document.getElementById('radiusInput').value);
    
    // Set this as the current search point
    currentSearchPoint = {lat: center.lat, lng: center.lng};
    
    // Search for locations and images
    searchByCoordinates(center.lat, center.lng, radius);
});

// Location search input handler
document.getElementById('locationSearch').addEventListener('input', debounce(function(e) {
    const query = e.target.value.trim();
    if (query.length < 2) {
        document.getElementById('locationResults').innerHTML = '';
        return;
    }
    
    fetch(`/api/search_by_name?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('locationResults');
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No locations found</p>';
                return;
            }
            
            let html = '';
            data.forEach(location => {
                html += `
                    <div class="location-item" data-lat="${location.latitude}" data-lon="${location.longitude}" data-id="${location.id}">
                        ${location.name}
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
            
            // Add click handlers to location items
            document.querySelectorAll('.location-item').forEach(item => {
                item.addEventListener('click', function() {
                    const lat = parseFloat(this.getAttribute('data-lat'));
                    const lon = parseFloat(this.getAttribute('data-lon'));
                    const id = parseInt(this.getAttribute('data-id'));
                    const radius = parseFloat(document.getElementById('radiusInput').value);
                    
                    // Pan map to location
                    map.flyTo([lat, lon], 14);
                    
                    // Set as current search point
                    currentSearchPoint = {lat, lng: lon};
                    
                    // Search around this location
                    searchByCoordinates(lat, lon, radius);
                });
            });
        })
        .catch(error => console.error('Error searching locations:', error));
}, 300));

// Function to search by coordinates
function searchByCoordinates(lat, lng, radius) {
    // Clear previous results
    clearResults();
    
    // Draw search circle
    if (searchCircle) {
        map.removeLayer(searchCircle);
    }
    searchCircle = L.circle([lat, lng], {
        radius: radius * 1000, // Convert km to meters
        color: '#3388ff',
        fillColor: '#3388ff',
        fillOpacity: 0.1
    }).addTo(map);
    
    // Show loading message
    document.getElementById('searchResults').innerHTML = '<p>Loading results...</p>';
    
    // Fetch results from API
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            lat: lat,
            lon: lng,
            radius: radius
        })
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data, lat, lng);
    })
    .catch(error => {
        console.error('Error fetching search results:', error);
        document.getElementById('searchResults').innerHTML = '<p>Error loading results. Please try again.</p>';
    });
}

// Function to display search results
function displayResults(data, centerLat, centerLng) {
    const { locations, images } = data;
    
    // Update the results panel
    let resultsHtml = '';
    
    if (locations.length === 0 && images.length === 0) {
        resultsHtml = '<p>No results found in this area.</p>';
    } else {
        // Show summary
        resultsHtml = `
            <div class="results-header">
                Found ${locations.length} location(s) and ${images.length} image(s)
            </div>
        `;
        
        // Show images in a grid
        if (images.length > 0) {
            resultsHtml += '<h6 class="mt-3">Images:</h6>';
            resultsHtml += '<div class="image-grid">';
            
            images.forEach(image => {
                resultsHtml += `
                    <div class="image-preview" data-id="${image.id}" data-path="${image.path}" 
                         data-lat="${image.latitude}" data-lon="${image.longitude}" 
                         data-location="${image.location_name}" data-distance="${image.distance}">
                        <div style="position: relative;">
                            <img src="${image.path}" alt="${image.location_name}">
                            <div class="image-info">
                                <small>${image.distance} km away</small>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            resultsHtml += '</div>';
        }
    }
    
    document.getElementById('searchResults').innerHTML = resultsHtml;
    
    // Add click handlers to image previews
    document.querySelectorAll('.image-preview').forEach(preview => {
        preview.addEventListener('click', function() {
            const imagePath = this.getAttribute('data-path');
            const locationName = this.getAttribute('data-location');
            const distance = this.getAttribute('data-distance');
            
            // Show in modal
            document.getElementById('modalImage').src = imagePath;
            document.getElementById('imageModalLabel').textContent = locationName;
            document.getElementById('imageInfo').innerHTML = `
                <p><strong>Location:</strong> ${locationName}</p>
                <p><strong>Distance:</strong> ${distance} km from search point</p>
            `;
            
            imageModal.show();
        });
    });
    
    // Add markers to the map
    addMarkersToMap(locations, images, centerLat, centerLng);
}

// Function to add markers to the map
function addMarkersToMap(locations, images, centerLat, centerLng) {
    // Add location markers
    locations.forEach(loc => {
        const marker = L.marker([loc.latitude, loc.longitude], {
            title: loc.name
        }).addTo(map);
        
        marker.bindPopup(`
            <div class="popup-content">
                <h5>${loc.name}</h5>
                <p>${loc.distance} km from search point</p>
            </div>
        `);
        
        locationMarkers.push(marker);
    });
    
    // Add image markers
    const imagesByLocation = {};
    
    // Group images by location (rounded coordinates)
    images.forEach(img => {
        const roundedLat = Math.round(img.latitude * 10000) / 10000;
        const roundedLon = Math.round(img.longitude * 10000) / 10000;
        const key = `${roundedLat},${roundedLon}`;
        
        if (!imagesByLocation[key]) {
            imagesByLocation[key] = [];
        }
        
        imagesByLocation[key].push(img);
    });
    
    // Add markers for each group
    Object.entries(imagesByLocation).forEach(([key, imgs]) => {
        const [lat, lon] = key.split(',').map(parseFloat);
        
        // Use a custom icon for image markers
        const imageIcon = L.divIcon({
            className: 'location-marker',
            html: `
                <div style="background-color: #ff4136; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;">
                    ${imgs.length > 1 ? `<div class="image-count-badge">${imgs.length}</div>` : ''}
                </div>
            `,
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });
        
        const marker = L.marker([lat, lon], {
            icon: imageIcon
        }).addTo(map);
        
        // Create popup content with carousel if multiple images
        let popupContent = `<div class="popup-content">`;
        
        if (imgs.length === 1) {
            const img = imgs[0];
            popupContent += `
                <img src="${img.path}" class="popup-image" alt="${img.location_name}">
                <h6 class="mt-2">${img.location_name}</h6>
                <p><small>${img.distance} km from search point</small></p>
            `;
        } else {
            // Show the first image and info about how many more
            popupContent += `
                <img src="${imgs[0].path}" class="popup-image" alt="${imgs[0].location_name}">
                <h6 class="mt-2">${imgs[0].location_name}</h6>
                <p><small>${imgs.length} images at this location</small></p>
            `;
        }
        
        popupContent += `</div>`;
        
        marker.bindPopup(popupContent, {
            className: 'custom-popup',
            maxWidth: 250
        });
        
        imageMarkers.push(marker);
    });
}

// Function to clear previous results
function clearResults() {
    // Clear markers
    locationMarkers.forEach(marker => map.removeLayer(marker));
    imageMarkers.forEach(marker => map.removeLayer(marker));
    
    locationMarkers = [];
    imageMarkers = [];
}

// Utility function for debouncing
function debounce(func, delay) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
    };
}

// Try to get user's location
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            map.setView([lat, lng], 13);
        },
        function(error) {
            console.log("Could not get current location:", error);
        }
    );
}
