/**
 * CarCraft: Automotive Inventory & Dealership Suite
 * Client-Side Enhancements & AJAX Handlers
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Photo Gallery Switcher (Vehicle Detail Page)
    const mainGalleryImage = document.getElementById('mainGalleryImage');
    const galleryThumbs = document.querySelectorAll('.gallery-thumb-btn');

    if (mainGalleryImage && galleryThumbs.length > 0) {
        galleryThumbs.forEach(btn => {
            btn.addEventListener('click', () => {
                const newSrc = btn.getAttribute('data-img-src');
                if (newSrc) {
                    mainGalleryImage.style.opacity = '0.4';
                    setTimeout(() => {
                        mainGalleryImage.src = newSrc;
                        mainGalleryImage.style.opacity = '1';
                    }, 120);

                    galleryThumbs.forEach(t => t.classList.remove('active', 'border-warning'));
                    btn.classList.add('active', 'border-warning');
                }
            });
        });
    }

    // 2. Real-Time Service Bay Availability Checker
    const bookingDateInput = document.getElementById('id_date');
    const bookingSlotInput = document.getElementById('id_time_slot');
    const availabilityBadge = document.getElementById('bayAvailabilityBadge');
    const availabilityDetails = document.getElementById('bayAvailabilityDetails');
    const bookingSubmitBtn = document.getElementById('bookingSubmitBtn');

    function checkSlotAvailability() {
        if (!bookingDateInput || !bookingSlotInput || !availabilityBadge) return;

        const dateVal = bookingDateInput.value;
        const slotVal = bookingSlotInput.value;

        if (!dateVal || !slotVal) return;

        availabilityBadge.innerHTML = `<span class="spinner-border spinner-border-sm text-warning me-1"></span> Checking bay capacity...`;
        availabilityBadge.className = 'badge bg-dark border border-secondary text-warning';

        fetch(`/service/api/availability/?date=${encodeURIComponent(dateVal)}&slot=${encodeURIComponent(slotVal)}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.is_fully_booked) {
                availabilityBadge.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> FULLY BOOKED (${data.total_bays}/${data.total_bays} Bays Occupied)`;
                availabilityBadge.className = 'badge bg-danger text-white p-2';
                if (availabilityDetails) {
                    availabilityDetails.innerHTML = `<div class="alert alert-danger mt-2 py-2 small mb-0"><i class="bi bi-exclamation-triangle-fill me-1"></i> All workshop bays are booked for this time slot. Please choose another slot or day.</div>`;
                }
                if (bookingSubmitBtn) {
                    bookingSubmitBtn.disabled = true;
                }
            } else {
                availabilityBadge.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> ${data.available_count} of ${data.total_bays} Bays Available`;
                availabilityBadge.className = 'badge bg-success text-white p-2';
                if (availabilityDetails) {
                    if (data.suggested_bay) {
                        availabilityDetails.innerHTML = `<div class="text-success small mt-1"><i class="bi bi-cpu-fill me-1"></i> Auto-assigning: <strong>${data.suggested_bay.name}</strong> (${data.suggested_bay.technician})</div>`;
                    } else {
                        availabilityDetails.innerHTML = '';
                    }
                }
                if (bookingSubmitBtn) {
                    bookingSubmitBtn.disabled = false;
                }
            }
        })
        .catch(err => {
            console.warn('Availability check error:', err);
            availabilityBadge.innerHTML = `<span class="text-muted">Bay auto-assignment active</span>`;
        });
    }

    if (bookingDateInput && bookingSlotInput) {
        bookingDateInput.addEventListener('change', checkSlotAvailability);
        bookingSlotInput.addEventListener('change', checkSlotAvailability);
        // Initial check on load
        if (bookingDateInput.value && bookingSlotInput.value) {
            checkSlotAvailability();
        }
    }

    // 3. AJAX Quick Add to Cart
    document.querySelectorAll('.ajax-add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = this.getAttribute('action');
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Adding...`;
            }

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Update all cart count badges across the page
                    document.querySelectorAll('.cart-count-badge').forEach(badge => {
                        badge.textContent = data.cart_count;
                        badge.classList.remove('d-none');
                    });

                    // Flash button state
                    if (submitBtn) {
                        submitBtn.innerHTML = `<i class="bi bi-check-lg me-1"></i> Added!`;
                        submitBtn.classList.remove('btn-apex', 'btn-workshop');
                        submitBtn.classList.add('btn-success');
                        setTimeout(() => {
                            submitBtn.innerHTML = originalBtnHtml;
                            submitBtn.disabled = false;
                            submitBtn.classList.remove('btn-success');
                            submitBtn.classList.add('btn-apex');
                        }, 1400);
                    }
                }
            })
            .catch(err => {
                console.error('Cart add error:', err);
                if (submitBtn) {
                    submitBtn.innerHTML = originalBtnHtml;
                    submitBtn.disabled = false;
                }
            });
        });
    });

    // 4. Quick Status Changer for Vehicles (AJAX)
    document.querySelectorAll('.quick-vehicle-status-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const vehicleId = this.getAttribute('data-vehicle-id');
            const statusVal = this.getAttribute('data-status');
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

            if (!vehicleId || !statusVal) return;

            const formData = new FormData();
            formData.append('status', statusVal);
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken);
            }

            fetch(`/inventory/${vehicleId}/quick-status/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken || ''
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const badgeElem = document.getElementById(`vehicle-badge-${vehicleId}`);
                    if (badgeElem) {
                        badgeElem.className = `badge ${data.badge_class}`;
                        badgeElem.textContent = data.status_display;
                    }
                }
            })
            .catch(err => console.error('Status change error:', err));
        });
    });
});
