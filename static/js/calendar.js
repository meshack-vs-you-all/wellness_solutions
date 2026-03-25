// Calendar functionality
document.addEventListener('alpine:init', () => {
    Alpine.data('calendar', () => ({
        currentWeek: new Date(),
        timeSlots: [],
        selectedDate: null,
        selectedSlot: null,
        loading: false,
        error: null,

        init() {
            this.fetchTimeSlots();
        },

        async fetchTimeSlots() {
            this.loading = true;
            try {
                const startDate = this.getStartOfWeek(this.currentWeek);
                const endDate = this.getEndOfWeek(this.currentWeek);
                
                const response = await fetch(`/api/time-slots/?start=${startDate.toISOString()}&end=${endDate.toISOString()}`);
                const data = await response.json();
                
                this.timeSlots = data.map(slot => ({
                    ...slot,
                    start: new Date(slot.start_datetime),
                    end: new Date(slot.end_datetime)
                }));
            } catch (err) {
                this.error = 'Failed to load time slots';
                console.error('Error fetching time slots:', err);
            } finally {
                this.loading = false;
            }
        },

        getStartOfWeek(date) {
            const d = new Date(date);
            const day = d.getDay();
            const diff = d.getDate() - day + (day === 0 ? -6 : 1);
            return new Date(d.setDate(diff));
        },

        getEndOfWeek(date) {
            const startOfWeek = this.getStartOfWeek(date);
            const endOfWeek = new Date(startOfWeek);
            endOfWeek.setDate(startOfWeek.getDate() + 6);
            return endOfWeek;
        },

        formatTime(hour) {
            return new Date(2000, 0, 1, hour).toLocaleTimeString([], { hour: 'numeric' });
        },

        hasSlot(hour, dayIndex) {
            const date = new Date(this.getStartOfWeek(this.currentWeek));
            date.setDate(date.getDate() + dayIndex);
            date.setHours(hour, 0, 0, 0);
            
            return this.timeSlots.some(slot => 
                slot.start.getDate() === date.getDate() &&
                slot.start.getHours() === hour
            );
        },

        hasAvailableSlot(hour, dayIndex) {
            const date = new Date(this.getStartOfWeek(this.currentWeek));
            date.setDate(date.getDate() + dayIndex);
            date.setHours(hour, 0, 0, 0);
            
            return this.timeSlots.some(slot => 
                slot.start.getDate() === date.getDate() &&
                slot.start.getHours() === hour &&
                slot.status === 'available'
            );
        },

        hasBookedSlot(hour, dayIndex) {
            const date = new Date(this.getStartOfWeek(this.currentWeek));
            date.setDate(date.getDate() + dayIndex);
            date.setHours(hour, 0, 0, 0);
            
            return this.timeSlots.some(slot => 
                slot.start.getDate() === date.getDate() &&
                slot.start.getHours() === hour &&
                slot.status === 'booked'
            );
        },

        getSlotInfo(hour, dayIndex) {
            const date = new Date(this.getStartOfWeek(this.currentWeek));
            date.setDate(date.getDate() + dayIndex);
            date.setHours(hour, 0, 0, 0);
            
            const slot = this.timeSlots.find(slot => 
                slot.start.getDate() === date.getDate() &&
                slot.start.getHours() === hour
            );
            
            return slot ? (slot.status === 'booked' ? 'Booked' : 'Available') : '';
        },

        async selectSlot(hour, dayIndex) {
            const date = new Date(this.getStartOfWeek(this.currentWeek));
            date.setDate(date.getDate() + dayIndex);
            date.setHours(hour, 0, 0, 0);
            
            const slot = this.timeSlots.find(slot => 
                slot.start.getDate() === date.getDate() &&
                slot.start.getHours() === hour
            );
            
            if (slot && slot.status === 'available') {
                this.selectedSlot = slot;
                this.selectedDate = date;
                
                // Dispatch custom event for booking form
                window.dispatchEvent(new CustomEvent('slot-selected', {
                    detail: { slot: this.selectedSlot, date: this.selectedDate }
                }));
            }
        }
    }));
});
