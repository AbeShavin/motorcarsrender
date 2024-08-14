document.addEventListener('DOMContentLoaded', function() {
    const makeDropdown = document.getElementById('id_make');
    const modelDropdown = document.getElementById('id_model'); // Ensure this matches your HTML ID

    if (makeDropdown) {
        makeDropdown.addEventListener('change', function() {
            const makeId = makeDropdown.value;
            
            // If makeId is empty, reset the model dropdown
            if (!makeId) {
                modelDropdown.innerHTML = '<option value="">Select Model</option>';
                return;
            }
            
            fetch(`/search/ajax/load_models/?make_id=${makeId}`)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Network response was not ok.');
                    }
                })
                .then(data => {
                    // Clear current models
                    modelDropdown.innerHTML = '<option value="">Select Model</option>';
                    
                    // Add new models
                    data.models.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.Id; // Use correct property name
                        option.textContent = model.name; // Use correct property name
                        modelDropdown.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });

        // Populate the make dropdown on page load
        fetch(`/search/ajax/load_makes/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                // Add makes to the dropdown
                data.makes.forEach(make => {
                    const option = document.createElement('option');
                    option.value = make.Id; // Use correct property name
                    option.textContent = make.name; // Use correct property name
                    makeDropdown.appendChild(option);
                });
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    }
});
