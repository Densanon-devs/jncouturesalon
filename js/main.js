/* ============================================
   Salon Studio Template — Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {

  // --- Mobile Menu Toggle ---
  var menuToggle = document.querySelector('.menu-toggle');
  var mainNav = document.querySelector('.main-nav');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
      this.classList.toggle('active');
      mainNav.classList.toggle('open');
      document.body.style.overflow = mainNav.classList.contains('open') ? 'hidden' : '';
    });
  }

  // --- Mobile Dropdown Toggle ---
  var dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(function(dropdown) {
    var link = dropdown.querySelector(':scope > a');
    if (link && window.innerWidth <= 768) {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        dropdown.classList.toggle('open');
      });
    }
  });

  // Re-bind dropdowns on resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      dropdowns.forEach(function(d) { d.classList.remove('open'); });
      if (mainNav) mainNav.classList.remove('open');
      if (menuToggle) menuToggle.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  // --- Header scroll effect ---
  var header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // --- FAQ Accordion ---
  var faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(function(item) {
    var question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', function() {
        var isOpen = item.classList.contains('open');
        // Close all others
        faqItems.forEach(function(other) { other.classList.remove('open'); });
        // Toggle current
        if (!isOpen) item.classList.add('open');
      });
    }
  });

  // --- Gallery Filter ---
  var filterBtns = document.querySelectorAll('.filter-btn');
  var galleryItems = document.querySelectorAll('.gallery-item');

  filterBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      filterBtns.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      var filter = this.getAttribute('data-filter');

      galleryItems.forEach(function(item) {
        if (filter === 'all' || item.getAttribute('data-category') === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // --- Contact Form Handling ---
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();

      var valid = true;
      var required = contactForm.querySelectorAll('[required]');
      required.forEach(function(field) {
        if (!field.value.trim()) {
          field.style.borderColor = 'var(--color-error)';
          valid = false;
        } else {
          field.style.borderColor = '';
        }
      });

      var emailField = contactForm.querySelector('input[type="email"]');
      if (emailField && emailField.value) {
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailField.value)) {
          emailField.style.borderColor = 'var(--color-error)';
          valid = false;
        }
      }

      if (!valid) return;

      var submitBtn = contactForm.querySelector('button[type="submit"]');
      var status = document.getElementById('form-status');
      var originalText = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';
      if (status) { status.textContent = ''; status.style.color = ''; }

      var data = {};
      new FormData(contactForm).forEach(function(v, k) { data[k] = v; });

      fetch('https://formsubmit.co/ajax/jncouturesalon@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function(r) { return r.json().catch(function() { return {}; }); })
        .then(function(res) {
          if (res && (res.success === true || res.success === 'true')) {
            contactForm.reset();
            submitBtn.textContent = 'Message Sent!';
            submitBtn.style.background = 'var(--color-success)';
            if (status) status.textContent = "Thanks! We got your message and will get back to you soon.";
            if (typeof gtag === 'function') gtag('event', 'generate_lead');
          } else {
            throw new Error((res && res.message) || 'send failed');
          }
        })
        .catch(function() {
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
          if (status) {
            status.style.color = 'var(--color-error)';
            status.innerHTML = 'Sorry, your message didn\'t go through. Please call us at <a href="tel:+12087624667">(208) 762-4667</a> or email <a href="mailto:jncouturesalon@gmail.com">jncouturesalon@gmail.com</a>.';
          }
        });
    });
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (mainNav) mainNav.classList.remove('open');
        if (menuToggle) menuToggle.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // --- Click to call tracking (placeholder) ---
  document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {
    link.addEventListener('click', function() {
      if (typeof gtag === 'function') {
        gtag('event', 'click_to_call', { event_category: 'engagement' });
      }
    });
  });

  // --- Active nav link highlighting ---
  var currentPath = window.location.pathname;
  document.querySelectorAll('.main-nav a').forEach(function(link) {
    var href = link.getAttribute('href');
    if (href && currentPath.includes(href) && href !== '/' && href !== '../') {
      link.classList.add('active');
    }
  });

});
