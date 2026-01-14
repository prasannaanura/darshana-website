document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('bookingForm');
    const checkinInput = document.getElementById('checkin');
    const checkoutInput = document.getElementById('checkout');
    const errorDiv = document.getElementById('dateError');
    
    // Set minimum date to today
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayStr = today.toISOString().split('T')[0];
    
    checkinInput.setAttribute('min', todayStr);
    checkoutInput.setAttribute('min', todayStr);
    
    // Validate dates function
    function validateDates() {
        errorDiv.style.display = 'none';
        errorDiv.textContent = '';
        
        if (!checkinInput.value || !checkoutInput.value) {
            return true;
        }
        
        const checkinDate = new Date(checkinInput.value);
        const checkoutDate = new Date(checkoutInput.value);
        
        checkinDate.setHours(0, 0, 0, 0);
        checkoutDate.setHours(0, 0, 0, 0);
        
        // Check if check-in is in the past
        if (checkinDate < today) {
            errorDiv.textContent = '❌ Check-in date cannot be in the past';
            errorDiv.style.display = 'block';
            return false;
        }
        
        // ✅ CHECK IF DATES OVERLAP WITH BOOKED DATES
        if (typeof bookedDates !== 'undefined' && bookedDates.length > 0) {
            const selectedCheckin = checkinInput.value;
            const selectedCheckout = checkoutInput.value;
            
            let current = new Date(selectedCheckin);
            const end = new Date(selectedCheckout);
            
            while (current < end) {
                const dateStr = current.toISOString().split('T')[0];
                if (bookedDates.includes(dateStr)) {
                    errorDiv.textContent = '❌ Selected dates are not available. Please choose different dates.';
                    errorDiv.style.display = 'block';
                    return false;
                }
                current.setDate(current.getDate() + 1);
            }
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