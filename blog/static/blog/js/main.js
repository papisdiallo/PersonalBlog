AOS.init({
	duration: 800,
	easing: 'slide'
});

(function ($) {

	"use strict";

	$(window).stellar({
		responsive: true,
		parallaxBackgrounds: true,
		parallaxElements: true,
		horizontalScrolling: false,
		hideDistantElements: false,
		scrollProperty: 'scroll'
	});


	var fullHeight = function () {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function () {
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	// loader
	var loader = function () {
		setTimeout(function () {
			if ($('#ftco-loader').length > 0) {
				$('#ftco-loader').removeClass('show');
			}
		}, 1);
	};
	loader();

	// Scrollax
	$.Scrollax();


	var burgerMenu = function () {

		$('.js-colorlib-nav-toggle').on('click', function (event) {
			event.preventDefault();
			var $this = $(this);

			if ($('body').hasClass('offcanvas')) {
				$this.removeClass('active');
				$('body').removeClass('offcanvas');


			} else {
				$this.addClass('active');
				$('body').addClass('offcanvas');

			}
		});
	};
	burgerMenu();

	//Logo display
	var displayLogo = function () {

		$(window).on('click', function () {

			if ($('body').hasClass('offcanvas')) {
				if ($('#myLogo').hasClass('profile')) {
					$('#myLogo').removeClass('profile');
				}
				$('#myLogo').addClass('non-profile');


			} else {
				if ($('#myLogo').hasClass('non-profile')) {
					$('#myLogo').removeClass('non-profile')
				}
				$('#myLogo').addClass('profile')

			}
		});
	};

	displayLogo()

	// Click outside of offcanvass
	var mobileMenuOutsideClick = function () {

		$(document).click(function (e) {
			var container = $("#colorlib-aside, .js-colorlib-nav-toggle");
			if (!container.is(e.target) && container.has(e.target).length === 0) {

				if ($('body').hasClass('offcanvas')) {

					$('body').removeClass('offcanvas');
					$('.js-colorlib-nav-toggle').removeClass('active');

				}
			}
		});

		$(window).scroll(function () {
			if ($('body').hasClass('offcanvas')) {

				$('body').removeClass('offcanvas');
				$('.js-colorlib-nav-toggle').removeClass('active');


			}
		});

	};
	mobileMenuOutsideClick();

	var carousel = function () {
		$('.home-slider').owlCarousel({
			loop: true,
			autoplay: true,
			margin: 0,
			animateOut: 'fadeOut',
			animateIn: 'fadeIn',
			nav: false,
			autoplayHoverPause: false,
			items: 1,
			navText: ["<span class='ion-md-arrow-back'></span>", "<span class='ion-chevron-right'></span>"],
			responsive: {
				0: {
					items: 1
				},
				600: {
					items: 1
				},
				1000: {
					items: 1
				}
			}
		});

		$('.author-slider').owlCarousel({
			autoplay: true,
			loop: true,
			items: 1,
			margin: 30,
			stagePadding: 0,
			nav: true,
			dots: true,
			navText: ['<span class="ion-ios-arrow-back">', '<span class="ion-ios-arrow-forward">'],
			responsive: {
				0: {
					items: 1
				},
				600: {
					items: 1
				},
				1000: {
					items: 1
				}
			}
		});

	};
	carousel();



	var contentWayPoint = function () {
		var i = 0;
		$('.ftco-animate').waypoint(function (direction) {

			if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

				i++;

				$(this.element).addClass('item-animate');
				setTimeout(function () {

					$('body .ftco-animate.item-animate').each(function (k) {
						var el = $(this);
						setTimeout(function () {
							var effect = el.data('animate-effect');
							if (effect === 'fadeIn') {
								el.addClass('fadeIn ftco-animated');
							} else if (effect === 'fadeInLeft') {
								el.addClass('fadeInLeft ftco-animated');
							} else if (effect === 'fadeInRight') {
								el.addClass('fadeInRight ftco-animated');
							} else {
								el.addClass('fadeInUp ftco-animated');
							}
							el.removeClass('item-animate');
						}, k * 50, 'easeInOutExpo');
					});

				}, 100);

			}

		}, { offset: '95%' });
	};
	contentWayPoint();

	var counter = function () {

		$('#section-counter').waypoint(function (direction) {

			if (direction === 'down' && !$(this.element).hasClass('ftco-animated')) {

				var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
				$('.number').each(function () {
					var $this = $(this),
						num = $this.data('number');
					console.log(num);
					$this.animateNumber(
						{
							number: num,
							numberStep: comma_separator_number_step
						}, 7000
					);
				});

			}

		}, { offset: '95%' });

	}
	counter();


	// magnific popup
	$('.image-popup').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		closeBtnInside: false,
		fixedContentPos: true,
		// mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
		},
		image: {
			verticalFit: true
		},
		zoom: {
			enabled: true,
			duration: 300 // don't foget to change the duration also in CSS
		}
	});

	$('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
		disableOn: 700,
		type: 'iframe',
		mainClass: 'mfp-fade',
		removalDelay: 160,
		preloader: false,

		fixedContentPos: false
	});




})(jQuery);


$('#username').click(function (e) {
	console.log('clicked');
	var profiles = $("#profiles");
	e.preventDefault();

	profiles.hasClass('non-profile') ? profiles.removeClass('non-profile').addClass('profile') :
		profiles.removeClass('profile').addClass('non-profile')
})

// get the submit btn parent and add eventlistener to it
console.log($("#contactForm").parent())
$("#contactForm").parent().on('click', (e) => {
	if (e.target.getAttribute("id") !== "submit-id-contact-me") return;
	e.preventDefault();
	e.target.setAttribute("disabled", true);
	$.ajax({
		url: "/contact/",
		method: "POST",
		data: $("#contactForm").serialize(),
		success: (response) => {
			$(e.target).prop("disabled", false)
			if (response.success) {
				$("#contactForm")[0].reset();
				$("#contact-me-alert").show('slide', { direction: 'right' }, 300);
				setTimeout(() => {
					$("#contact-me-alert").hide('slide', { direction: 'left' }, 300);
				}, 2000)
			} else {
				$("#contactForm").replaceWith(response.formErrors);
			}

		},
		error: (error) => {
			console.log(error);
		}

	})
})
// create a view to handle the form valid and return the form with errors if the form is not valid
// if the for is valid send and email to psdiallo200 
// on success jusst alert the user