function openBookingModal(startTime, endTime) {
    document.getElementById('modalStartTime').value = startTime;
    document.getElementById('modalEndTime').value = endTime;
    
    // Format time for display (simple approach)
    const start = startTime.split(':');
    let hours = parseInt(start[0]);
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    document.getElementById('modalTimeDisplay').innerText = hours + ':' + start[1] + ' ' + ampm;
    
    document.getElementById('bookingModal').classList.add('active');
}

function closeBookingModal() {
    document.getElementById('bookingModal').classList.remove('active');
}
