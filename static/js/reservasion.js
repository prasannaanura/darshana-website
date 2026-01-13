document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bookingForm');
    const checkinInput = document.getElementById('checkin');
    const checkoutInput = document.getElementById('checkout');
    const errorDiv = document.getElementById('dateError');
    
    // Set minimum date to today
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time for accurate comparison
    const todayStr = today.toISOString().split('T')[0];
    
    checkinInput.setAttribute('min', todayStr);
    checkoutInput.setAttribute('min', todayStr);
    
    // Validate dates function
    function validateDates() {
        // Clear previous errors
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';
        
        if (!checkinInput.value || !checkoutInput.value) {
            return true; // Don't validate if dates aren't filled
        }
        
        const checkinDate = new Date(checkinInput.value);
        const checkoutDate = new Date(checkoutInput.value);
        
        // Reset time for accurate date-only comparison
        checkinDate.setHours(0, 0, 0, 0);
        checkoutDate.setHours(0, 0, 0, 0);
        
        // Check if check-in is in the past
        if (checkinDate < today) {
            errorDiv.textContent = '❌ Check-in date cannot be in the past';
            errorDiv.style.display = 'block';
            return false;
        }
        
        // Check if check-out is before or equal to check-in
        if (checkoutDate <= checkinDate) {
            errorDiv.textContent = '❌ Check-out date must be after check-in date';
            errorDiv.style.display = 'block';
            return false;
        }
        
        return true;
    }
    
    // Validate on check-in change
    checkinInput.addEventListener('change', function() {
        validateDates();
        // Update checkout minimum date to day after checkin
        if (checkinInput.value) {
            const nextDay = new Date(checkinInput.value);
            nextDay.setDate(nextDay.getDate() + 1);
            checkoutInput.setAttribute('min', nextDay.toISOString().split('T')[0]);
        }
    });
    
    // Validate on check-out change
    checkoutInput.addEventListener('change', validateDates);
    
    // Validate on form submit
    form.addEventListener('submit', function(e) {
        if (!validateDates()) {
            e.preventDefault();
            return false;
        }
    });
});