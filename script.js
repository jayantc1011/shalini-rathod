const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
const mobileLinks = mobileMenu ? Array.from(mobileMenu.querySelectorAll('.mobile-menu-links a, .mobile-actions a')) : [];
const mobileNavLinks = mobileMenu ? Array.from(mobileMenu.querySelectorAll('.mobile-menu-links a')) : [];
const mobileMenuBackdrop = mobileMenu ? mobileMenu.querySelector('.mobile-menu-backdrop') : null;

function setMenu(open) {
  if (!menuToggle || !mobileMenu) return;
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  mobileMenu.hidden = !open;
  document.body.classList.toggle('mobile-nav-open', open);
}

if (menuToggle && mobileMenu) {
  menuToggle.addEventListener('click', () => {
    setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
  });

  if (mobileMenuBackdrop) {
    mobileMenuBackdrop.addEventListener('click', () => setMenu(false));
  }

  mobileLinks.forEach((link) => {
    link.addEventListener('click', () => {
      if (link.closest('.mobile-menu-links')) {
        mobileNavLinks.forEach((item) => item.classList.toggle('active', item === link));
      }
      setMenu(false);
    });
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menuToggle.focus();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1080) setMenu(false);
  });
}

// Keep the active underline behavior feeling like the reference navigation.
const desktopLinks = document.querySelectorAll('.desktop-nav .nav-link');
desktopLinks.forEach((link) => {
  link.addEventListener('click', () => {
    desktopLinks.forEach((item) => item.classList.remove('active'));
    link.classList.add('active');
  });
});


// Never leave broken-image icons visible. Any image with data-fallback will
// automatically swap to the local fallback asset if its source cannot load.
document.querySelectorAll('img[data-fallback]').forEach((image) => {
  image.addEventListener('error', () => {
    const fallback = image.dataset.fallback;
    if (fallback && image.getAttribute('src') !== fallback) {
      image.src = fallback;
    }
  }, { once: true });
});

// Guest appearances carousel: arrows, dots, keyboard-friendly native scrolling.
const appearanceCarousel = document.querySelector('.appearance-carousel');
const appearancePrev = document.querySelector('.carousel-prev');
const appearanceNext = document.querySelector('.carousel-next');
const appearanceDots = Array.from(document.querySelectorAll('.carousel-dot'));

if (appearanceCarousel && appearancePrev && appearanceNext && appearanceDots.length) {
  const maxScroll = () => Math.max(0, appearanceCarousel.scrollWidth - appearanceCarousel.clientWidth);

  const setDot = (index) => {
    const safeIndex = Math.max(0, Math.min(index, appearanceDots.length - 1));
    appearanceDots.forEach((dot, i) => dot.classList.toggle('active', i === safeIndex));
  };

  const updateCarouselState = () => {
    const maximum = maxScroll();
    const progress = maximum > 0 ? appearanceCarousel.scrollLeft / maximum : 0;
    const dotIndex = Math.round(progress * (appearanceDots.length - 1));
    setDot(dotIndex);
    appearancePrev.disabled = appearanceCarousel.scrollLeft <= 2;
    appearanceNext.disabled = appearanceCarousel.scrollLeft >= maximum - 2;
  };

  const scrollByCard = (direction) => {
    const card = appearanceCarousel.querySelector('.appearance-card');
    if (!card) return;
    const gap = parseFloat(getComputedStyle(appearanceCarousel).gap) || 0;
    appearanceCarousel.scrollBy({
      left: direction * (card.getBoundingClientRect().width + gap),
      behavior: 'smooth'
    });
  };

  appearancePrev.addEventListener('click', () => scrollByCard(-1));
  appearanceNext.addEventListener('click', () => scrollByCard(1));

  appearanceDots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      const target = maxScroll() * (index / (appearanceDots.length - 1));
      appearanceCarousel.scrollTo({ left: target, behavior: 'smooth' });
      setDot(index);
    });
  });

  appearanceCarousel.addEventListener('scroll', () => {
    window.requestAnimationFrame(updateCarouselState);
  }, { passive: true });

  window.addEventListener('resize', updateCarouselState);
  updateCarouselState();
}


// Recognition marquee: pause at the exact current position while any card is hovered.
// Resume from the same point when the pointer leaves. Keyboard focus pauses it too.
const recognitionTrack = document.querySelector('.recognition-track');
const recognitionCards = document.querySelectorAll('.recognition-card');

if (recognitionTrack && recognitionCards.length) {
  const pauseRecognition = () => recognitionTrack.classList.add('is-paused');
  const resumeRecognition = () => recognitionTrack.classList.remove('is-paused');

  recognitionCards.forEach((card) => {
    card.addEventListener('mouseenter', pauseRecognition);
    card.addEventListener('mouseleave', resumeRecognition);
    card.addEventListener('focusin', pauseRecognition);
    card.addEventListener('focusout', resumeRecognition);
  });
}

// Direct inquiry form: keep the reference UI functional without requiring a backend.
const inquiryForm = document.querySelector('#inquiry-form');
const inquiryStatus = document.querySelector('#inquiry-status');

if (inquiryForm) {
  inquiryForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (!inquiryForm.checkValidity()) {
      inquiryForm.reportValidity();
      return;
    }

    const data = new FormData(inquiryForm);
    const subject = `${data.get('inquiryNature')} inquiry from ${data.get('fullName')}`;
    const body = [
      `Inquiry Nature: ${data.get('inquiryNature')}`,
      `Name: ${data.get('fullName')}`,
      `Email: ${data.get('email')}`,
      `Company / Organization / University: ${data.get('organization') || 'Not provided'}`,
      `Estimated Audience / Participants: ${data.get('audience')}`,
      `Desired Timeline: ${data.get('timeline')}`,
      '',
      'Message / Key Objectives:',
      data.get('message')
    ].join('\n');

    if (inquiryStatus) {
      inquiryStatus.textContent = 'Opening your email app with the inquiry details ready to send…';
    }

    window.location.href = `mailto:sreelpta@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
}

// Services page catalog: 30/60-minute consultation switching, search, and filters.
const durationButtons = Array.from(document.querySelectorAll('.calls-duration-toggle [data-duration]'));
const callCards = Array.from(document.querySelectorAll('.calls-grid .call-card'));

if (durationButtons.length && callCards.length) {
  const setDuration = (duration) => {
    durationButtons.forEach((button) => {
      const active = button.dataset.duration === duration;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    callCards.forEach((card) => {
      card.querySelectorAll('[data-duration-label]').forEach((label) => {
        label.textContent = `${duration}min`;
      });

      card.querySelectorAll('[data-duration-list]').forEach((list) => {
        list.hidden = list.dataset.durationList !== duration;
      });

      card.querySelectorAll('[data-duration-ideal]').forEach((ideal) => {
        ideal.hidden = ideal.dataset.durationIdeal !== duration;
      });

      const price = card.querySelector('.call-price');
      if (price) {
        price.textContent = duration === '60' ? price.dataset.price60 : price.dataset.price30;
      }
    });
  };

  durationButtons.forEach((button) => {
    button.addEventListener('click', () => setDuration(button.dataset.duration));
  });

  setDuration('30');
}

const servicesFilterTabs = Array.from(document.querySelectorAll('.services-filter-tab'));
const servicesSearchInput = document.querySelector('#services-search-input');
const servicesSearchEmpty = document.querySelector('#services-search-empty');
const callsSection = document.querySelector('[data-service-section="calls"]');
const packagesSection = document.querySelector('[data-service-section="packages"]');
const coursesSection = document.querySelector('[data-service-section="courses"]');
const packageCards = Array.from(document.querySelectorAll('.packages-grid .package-card'));
const courseCards = Array.from(document.querySelectorAll('.learning-grid .learning-card'));

if (servicesFilterTabs.length && (callsSection || packagesSection || coursesSection)) {
  let activeServiceFilter = 'all';

  const applyServiceFiltering = () => {
    const query = (servicesSearchInput?.value || '').trim().toLowerCase();
    let visibleTotal = 0;

    let visibleCalls = 0;
    callCards.forEach((card) => {
      const categoryMatch = activeServiceFilter === 'all' || activeServiceFilter === 'calls';
      const haystack = `${card.dataset.search || ''} ${card.textContent || ''}`.toLowerCase();
      const queryMatch = !query || haystack.includes(query);
      const show = categoryMatch && queryMatch;
      card.hidden = !show;
      if (show) {
        visibleCalls += 1;
        visibleTotal += 1;
      }
    });
    if (callsSection) callsSection.hidden = visibleCalls === 0;

    let visiblePackages = 0;
    packageCards.forEach((card) => {
      const categoryMatch = activeServiceFilter === 'all' || activeServiceFilter === 'packages';
      const haystack = `${card.dataset.search || ''} ${card.textContent || ''}`.toLowerCase();
      const queryMatch = !query || haystack.includes(query);
      const show = categoryMatch && queryMatch;
      card.hidden = !show;
      if (show) {
        visiblePackages += 1;
        visibleTotal += 1;
      }
    });
    if (packagesSection) packagesSection.hidden = visiblePackages === 0;

    let visibleCourses = 0;
    courseCards.forEach((card) => {
      const categoryMatch = activeServiceFilter === 'all' || activeServiceFilter === 'courses';
      const haystack = `${card.dataset.search || ''} ${card.textContent || ''}`.toLowerCase();
      const queryMatch = !query || haystack.includes(query);
      const show = categoryMatch && queryMatch;
      card.hidden = !show;
      if (show) {
        visibleCourses += 1;
        visibleTotal += 1;
      }
    });
    if (coursesSection) coursesSection.hidden = visibleCourses === 0;

    if (servicesSearchEmpty) servicesSearchEmpty.hidden = visibleTotal !== 0;
  };

  servicesFilterTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      activeServiceFilter = tab.dataset.serviceFilter || 'all';
      servicesFilterTabs.forEach((item) => {
        const active = item === tab;
        item.classList.toggle('active', active);
        item.setAttribute('aria-selected', String(active));
      });
      applyServiceFiltering();
    });
  });

  servicesSearchInput?.addEventListener('input', applyServiceFiltering);
  applyServiceFiltering();
}

// Services FAQ accordion: keep one answer open at a time, matching the reference interaction.
const serviceFaqItems = Array.from(document.querySelectorAll('.services-faq-item'));

if (serviceFaqItems.length) {
  const setFaqItem = (item, open) => {
    const button = item.querySelector('.services-faq-question');
    const answer = item.querySelector('.services-faq-answer');
    const chevronPath = item.querySelector('.services-faq-chevron path');
    if (!button || !answer) return;

    item.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', String(open));
    answer.hidden = !open;
    if (chevronPath) {
      chevronPath.setAttribute('d', open ? 'm5.5 12 4.5-4.5 4.5 4.5' : 'm5.5 8 4.5 4.5 4.5-4.5');
    }
  };

  serviceFaqItems.forEach((item) => {
    const button = item.querySelector('.services-faq-question');
    if (!button) return;

    button.addEventListener('click', () => {
      const isOpen = button.getAttribute('aria-expanded') === 'true';
      serviceFaqItems.forEach((otherItem) => setFaqItem(otherItem, false));
      if (!isOpen) setFaqItem(item, true);
    });
  });
}

// Services booking modal: multi-step consultation / package / course reservation flow.
const bookingModal = document.querySelector('#booking-modal');

if (bookingModal) {
  const bookingDialog = bookingModal.querySelector('.booking-dialog');
  const bookingBackdrop = bookingModal.querySelector('.booking-modal-backdrop');
  const bookingClose = bookingModal.querySelector('.booking-close');
  const bookingTriggers = Array.from(document.querySelectorAll('.booking-trigger'));
  const bookingSteps = Array.from(bookingModal.querySelectorAll('[data-booking-step]'));
  const bookingStepCount = bookingModal.querySelector('#booking-step-count');
  const offeringSelect = bookingModal.querySelector('#booking-offering');
  const durationWrap = bookingModal.querySelector('#booking-duration-wrap');
  const durationOptions = Array.from(bookingModal.querySelectorAll('[data-booking-duration]'));
  const scheduleBox = bookingModal.querySelector('#booking-schedule-box');
  const scheduleDateLabel = bookingModal.querySelector('#booking-date-label');
  const bookingDate = bookingModal.querySelector('#booking-date');
  const bookingTime = bookingModal.querySelector('#booking-time');
  const bookingTotal = bookingModal.querySelector('#booking-total');
  const bookingContinue = bookingModal.querySelector('#booking-continue');
  const bookingBack = bookingModal.querySelector('#booking-back');
  const bookingForm = bookingModal.querySelector('.booking-step-two');
  const bookingName = bookingModal.querySelector('#booking-name');
  const bookingEmail = bookingModal.querySelector('#booking-email');
  const bookingPhone = bookingModal.querySelector('#booking-phone');
  const bookingChallenge = bookingModal.querySelector('#booking-challenge');
  const summaryTitle = bookingModal.querySelector('#booking-summary-title');
  const summaryDate = bookingModal.querySelector('#booking-summary-date');
  const summaryPrice = bookingModal.querySelector('#booking-summary-price');
  const confirmLabel = bookingModal.querySelector('#booking-confirm-label');
  const confirmationName = bookingModal.querySelector('#booking-confirmation-name');
  const confirmationSummary = bookingModal.querySelector('#booking-confirmation-summary');
  const sendRequest = bookingModal.querySelector('#booking-send-request');
  const bookingDone = bookingModal.querySelector('#booking-done');

  const offerings = {
    discovery: {
      label: '15-Min Discovery Call',
      fullLabel: '15-Min Discovery Call (Free · Direct with Shalini)',
      type: 'discovery',
      price: 0,
      duration: 15,
      needsSchedule: true
    },
    'comm-call': {
      label: '1:1 Call: Communication & Confidence',
      fullLabel: '1:1 Communication & Confidence',
      type: 'call',
      prices: { '30': 3499, '60': 5999 },
      needsSchedule: true
    },
    'style-call': {
      label: '1:1 Call: Image Styling & Confidence',
      fullLabel: '1:1 Image Styling & Confidence',
      type: 'call',
      prices: { '30': 3499, '60': 5999 },
      needsSchedule: true
    },
    'comm-package': {
      label: 'Communication Skills & Confidence Makeover',
      fullLabel: 'Communication Skills & Confidence Makeover (7 Sessions)',
      type: 'package',
      price: 34999,
      duration: '7 Sessions',
      needsSchedule: true
    },
    'style-package': {
      label: 'Image & Styling Makeover',
      fullLabel: 'Image & Styling Makeover (7 Sessions)',
      type: 'package',
      price: 38999,
      duration: '7 Sessions',
      needsSchedule: true
    },
    speakathon: {
      label: '21-Day Speakathon Challenge',
      fullLabel: '21-Day Speakathon Challenge',
      type: 'course',
      price: 2999,
      duration: 'Lifetime Access',
      needsSchedule: false
    },
    'styling-course': {
      label: 'Power Dressing / Styling',
      fullLabel: 'Power Dressing / Styling',
      type: 'course',
      price: 3499,
      duration: 'Lifetime Access',
      needsSchedule: false
    },
    'power-bundle': {
      label: 'The Power Bundle',
      fullLabel: 'The Power Bundle',
      type: 'course',
      price: 4999,
      duration: 'Lifetime Access',
      needsSchedule: false
    }
  };

  let selectedDuration = '60';
  let lastBookingTrigger = null;

  const formatMoney = (amount) => amount === 0
    ? 'Free'
    : `₹${Number(amount).toLocaleString('en-IN')}`;

  const getOffering = () => offerings[offeringSelect?.value] || offerings['comm-call'];

  const getPrice = () => {
    const offering = getOffering();
    if (offering.type === 'call') return offering.prices[selectedDuration];
    return offering.price;
  };

  const setBookingStep = (step) => {
    bookingSteps.forEach((panel) => {
      panel.hidden = panel.dataset.bookingStep !== String(step);
    });
    if (bookingStepCount) bookingStepCount.textContent = `STEP ${step} OF 3`;
    if (bookingDialog) bookingDialog.scrollTop = 0;
  };

  const setDuration = (duration) => {
    selectedDuration = String(duration);
    durationOptions.forEach((button) => {
      const active = button.dataset.bookingDuration === selectedDuration;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    updateBookingUI();
  };

  const updateBookingUI = () => {
    const offering = getOffering();
    const price = getPrice();

    if (durationWrap) durationWrap.hidden = offering.type !== 'call';
    if (scheduleBox) scheduleBox.hidden = !offering.needsSchedule;
    if (bookingDate) bookingDate.required = Boolean(offering.needsSchedule);
    if (bookingTime) bookingTime.required = Boolean(offering.needsSchedule);

    if (scheduleDateLabel) {
      scheduleDateLabel.textContent = offering.type === 'package'
        ? 'SELECT PREFERRED START DATE & TIME:'
        : 'SELECT PREFERRED DATE & TIME:';
    }

    if (bookingTotal) bookingTotal.textContent = formatMoney(price);

    const durationText = offering.type === 'call'
      ? `${selectedDuration}min`
      : offering.duration || '';
    const summaryLabel = durationText ? `${offering.label} (${durationText})` : offering.label;

    if (summaryTitle) summaryTitle.textContent = summaryLabel;
    if (summaryPrice) summaryPrice.textContent = formatMoney(price);

    if (confirmLabel) {
      confirmLabel.textContent = offering.type === 'course'
        ? `Continue Enrollment (${formatMoney(price)})`
        : `Confirm & Reserve Slot (${formatMoney(price)})`;
    }
  };

  const setDefaultDate = () => {
    if (!bookingDate) return;
    const today = new Date();
    const min = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const preferred = new Date(min);
    preferred.setDate(preferred.getDate() + 2);
    const toIso = (date) => {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const d = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    };
    bookingDate.min = toIso(min);
    if (!bookingDate.value || bookingDate.value < bookingDate.min) {
      bookingDate.value = toIso(preferred);
    }
  };

  const openBooking = (offerKey = 'comm-call') => {
    const safeOffer = offerings[offerKey] ? offerKey : 'comm-call';
    if (offeringSelect) offeringSelect.value = safeOffer;

    if (safeOffer === 'comm-call' || safeOffer === 'style-call') {
      if (lastBookingTrigger?.classList.contains('call-book-btn')) {
        const activeCallDuration = document.querySelector('.calls-duration-toggle [data-duration].active');
        selectedDuration = activeCallDuration?.dataset.duration || '60';
      } else {
        // Generic "Book a Session" buttons follow the reference and start on the 60-minute deep dive.
        selectedDuration = '60';
      }
    } else {
      selectedDuration = '60';
    }

    durationOptions.forEach((button) => {
      const active = button.dataset.bookingDuration === selectedDuration;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });

    setDefaultDate();
    updateBookingUI();
    setBookingStep(1);
    bookingModal.hidden = false;
    bookingModal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('booking-open');
    window.requestAnimationFrame(() => bookingClose?.focus());
  };

  const closeBooking = () => {
    bookingModal.hidden = true;
    bookingModal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('booking-open');
    setBookingStep(1);
    lastBookingTrigger?.focus?.();
  };

  const getReadableDateTime = () => {
    const offering = getOffering();
    if (!offering.needsSchedule) return 'Lifetime access · Start after enrollment';
    const date = bookingDate?.value || '';
    const time = bookingTime?.value || '';
    const shortTime = time.split(' - ')[0] || time;
    return date ? `${date} at ${shortTime}` : shortTime;
  };

  bookingTriggers.forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      lastBookingTrigger = trigger;
      if (menuToggle?.getAttribute('aria-expanded') === 'true') setMenu(false);
      openBooking(trigger.dataset.bookingOffer || 'comm-call');
    });
  });

  durationOptions.forEach((button) => {
    button.addEventListener('click', () => setDuration(button.dataset.bookingDuration || '60'));
  });

  offeringSelect?.addEventListener('change', updateBookingUI);

  bookingContinue?.addEventListener('click', () => {
    const offering = getOffering();
    if (offering.needsSchedule && bookingDate && !bookingDate.value) {
      bookingDate.focus();
      bookingDate.showPicker?.();
      return;
    }
    updateBookingUI();
    if (summaryDate) summaryDate.textContent = getReadableDateTime();
    setBookingStep(2);
    bookingName?.focus();
  });

  bookingBack?.addEventListener('click', () => {
    setBookingStep(1);
    offeringSelect?.focus();
  });

  bookingForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!bookingForm.checkValidity()) {
      bookingForm.reportValidity();
      return;
    }

    const offering = getOffering();
    const price = getPrice();
    const contactName = bookingName?.value.trim() || 'there';
    const schedule = getReadableDateTime();
    const durationText = offering.type === 'call'
      ? `${selectedDuration} Minutes`
      : offering.duration || '';

    if (confirmationName) confirmationName.textContent = contactName;
    if (confirmationSummary) {
      confirmationSummary.innerHTML = [
        `<strong>${offering.fullLabel}</strong>`,
        durationText ? `<span>${durationText}</span>` : '',
        `<span>${schedule}</span>`,
        `<span>Total: ${formatMoney(price)}</span>`
      ].filter(Boolean).join('<br />');
    }

    const subject = `Booking request — ${offering.fullLabel}`;
    const body = [
      `Offering: ${offering.fullLabel}`,
      durationText ? `Duration / Access: ${durationText}` : '',
      offering.needsSchedule ? `Preferred date & time: ${schedule}` : '',
      `Investment: ${formatMoney(price)}`,
      '',
      `Name: ${bookingName?.value.trim() || ''}`,
      `Email: ${bookingEmail?.value.trim() || ''}`,
      `Phone / WhatsApp: ${bookingPhone?.value.trim() || ''}`,
      '',
      'Primary challenge / notes:',
      bookingChallenge?.value.trim() || 'Not provided'
    ].filter(Boolean).join('\n');

    if (sendRequest) {
      sendRequest.href = `mailto:contact@shalinirathod.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    }

    setBookingStep(3);
  });

  bookingBackdrop?.addEventListener('click', closeBooking);
  bookingClose?.addEventListener('click', closeBooking);
  bookingDone?.addEventListener('click', closeBooking);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !bookingModal.hidden) closeBooking();
  });

  // Keep tab focus inside the open modal.
  bookingModal.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab' || bookingModal.hidden) return;
    const focusable = Array.from(bookingDialog.querySelectorAll(
      'button:not([disabled]):not([hidden]), a[href]:not([hidden]), input:not([disabled]):not([hidden]), select:not([disabled]):not([hidden]), textarea:not([disabled]):not([hidden])'
    )).filter((el) => el.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  setDefaultDate();
  updateBookingUI();
}
