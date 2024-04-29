(function($) {
    "use strict";

    $(document).on('ready', function() {
		
	/* Header scroll on fixed */
	
	var NavBar = $('nav.navbar');
    var didScroll;
    var lastScrollTop = 0;
    var navbarHeight = NavBar.outerHeight();
    $(document).ready(function(event) {
        didScroll = true;
    });
    $(window).scroll(function(event) {
        didScroll = true;
    });
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 100);

    function hasScrolled() {
        var st = $(document).scrollTop();
        if (st + $(window).height() < $(document).height()) {
            NavBar.addClass('fixed-header');
            if (st == 0) {
                NavBar.removeClass('fixed-header');
            }
        }
        lastScrollTop = st;
    }


        /* ==================================================
            # Smooth Scroll
         ===============================================*/
        $("body").scrollspy({
            target: ".navbar-collapse",
            offset: 200
        });
        $('a.smooth-menu').on('click', function(event) {
            var $anchor = $(this);
            var headerH = '75';
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - headerH + "px"
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        });
		
		
		
		$('[data-toggle="tooltip"]').tooltip();
		
		$('[data-toggle="popover"]').popover();
		
		$(".owl-style").owlCarousel({
		    center: true,
		    items:2,
		    lazyLoad:true,
		    loop:true,
		    margin:40,
		    autoplay:true,
		    dots:true,
		    smartSpeed:800,
		    autoplayTimeout:3500,
		    autoplayHoverPause:false
		});

    // screenshot slider
    if ($('.screen-shot-slider').length > 0) {
      var owl = $('.screen-shot-slider');
      owl.owlCarousel({
        margin: 10,
        nav: true,
        loop: true,
        margin: 30,
        nav: false,
        responsive: {
          0: {
            items: 1
          },
          600: {
            items: 1
          },
          768: {
            items: 2
          },
          1000: {
            items: 3
          }
        }
      });
    }

    if ($('#lightgallery').length > 0) {
      $('#lightgallery').lightGallery({
    thumbnail: true,
    selector: 'a'
  });
  }

  if ($('#view_tabs').length > 0) {
		
		$('#view_tabs').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTab', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTab = localStorage.getItem('lastTab');
		if (lastTab) {
			$('[href="' + lastTab + '"]').tab('show');
			$(lastTab+" iframe").attr("src",$(lastTab).attr('data-src'));
		}else{
			$("#mobile_tab iframe").attr("src",$('#mobile_tab').attr('data-src'));
		}
	}
	
	if ($('#view_tabs2').length > 0) {
		
		$('#view_tabs2').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs2 a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs2 a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTabs', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTabs = localStorage.getItem('lastTabs');
		if (lastTabs) {
			$('[href="' + lastTabs + '"]').tab('show');
			$(lastTabs+" iframe").attr("src",$(lastTabs).attr('data-src'));
		}else{
			$("#mobile_tab2 iframe").attr("src",$('#mobile_tab2').attr('data-src'));
		}
	}

	if ($('#view_tabs3').length > 0) {
		
		$('#view_tabs3').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs3 a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs3 a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTabs', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTabs = localStorage.getItem('lastTabs');
		if (lastTabs) {
			$('[href="' + lastTabs + '"]').tab('show');
			$(lastTabs+" iframe").attr("src",$(lastTabs).attr('data-src'));
		}else{
			$("#mobile_tab3 iframe").attr("src",$('#mobile_tab3').attr('data-src'));
		}
	}

	if ($('#view_tabs4').length > 0) {
		
		$('#view_tabs4').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs4 a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs4 a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTabs', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTabs = localStorage.getItem('lastTabs');
		if (lastTabs) {
			$('[href="' + lastTabs + '"]').tab('show');
			$(lastTabs+" iframe").attr("src",$(lastTabs).attr('data-src'));
		}else{
			$("#mobile_tab4 iframe").attr("src",$('#mobile_tab4').attr('data-src'));
		}
	}

	if ($('#view_tabs5').length > 0) {
		
		$('#view_tabs5').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs5 a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs5 a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTabs', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTabs = localStorage.getItem('lastTabs');
		if (lastTabs) {
			$('[href="' + lastTabs + '"]').tab('show');
			$(lastTabs+" iframe").attr("src",$(lastTabs).attr('data-src'));
		}else{
			$("#mobile_tab5 iframe").attr("src",$('#mobile_tab5').attr('data-src'));
		}
	}

	if ($('#view_tabs6').length > 0) {
		
		$('#view_tabs6').click('show', function(e) {  
			paneID = $(e.target).attr('href'); 
			src = $(paneID).attr('data-src');
			// if the iframe hasn't already been loaded once
			if($(paneID+" iframe").attr("src")=="")
			{
				$(paneID+" iframe").attr("src",src);
			}
		});
	}
	
	if ($('#view_tabs6 a[data-toggle="tab"]').length > 0) {
	
		$('#view_tabs6 a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
			// save the latest tab; use cookies if you like 'em better:
			localStorage.setItem('lastTabs', $(this).attr('href'));
		});
		
		// go to the latest tab, if it exists:
		var lastTabs = localStorage.getItem('lastTabs');
		if (lastTabs) {
			$('[href="' + lastTabs + '"]').tab('show');
			$(lastTabs+" iframe").attr("src",$(lastTabs).attr('data-src'));
		}else{
			$("#mobile_tab6 iframe").attr("src",$('#mobile_tab6').attr('data-src'));
		}
	}
		
	
    $(window).on ('load', function (){ // makes sure the whole site is loaded
		
		$('#loader').delay(100).fadeOut('slow');
		$('#loader-wrapper').delay(500).fadeOut('slow');
		$('body').delay(500).css({'overflow':'visible'});
		
		AOS.init({
          duration: 1000,
		  disable: 'mobile',
          mirror: true
        });


    });

    }); // end document ready function
})(jQuery); // End jQuery


/*for forms*/
$(function () {
    $('#contact-form').on('submit', function (e) {
            console.log("baasss")
        if (!e.isDefaultPrevented()) {
            console.log("Sasas")
            var re = /^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/;
            var emailFormat = re.test($("#form_email").val());// this return result in boolean type
            if (emailFormat) {
                $('#alert_message').css({ 'display': 'none' })
                var url = "contact.php";
                $.ajax({
                    type: "POST",
                    url: url,
                    data: $(this).serialize(),
                    success: function (data) {
                        var messageAlert = 'alert-' + data.type;
                        var messageText = data.message;
                        var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                        if (messageAlert && messageText) {
                            $('#contact-form').find('.messages').html(alertBox);
                            $('#contact-form')[0].reset();
                        }
                    }
                });
            }
            else {
                $('#alert_message').css({ 'display': 'block' });
                $('#form_email').focus();
                return false;
            }
            return false;
        }
    })
});


/*particle js*/
particlesJS("particles-js", {
  particles: {
    number: {
      value: 20,
      density: {
        enable: true,
        value_area: 800
      }
    },
    color: {
      value: ["#fe7096", "#9a55ff", "#07cdae", "#ffd500"]
    },
    shape: {
      type: ["circle"],
      stroke: {
        width: 0,
        color: "#fff"
      },
      polygon: {
        nb_sides: 5
      },
      image: {
        src: "https://cdn.freebiesupply.com/logos/large/2x/slack-logo-icon.png",
        width: 100,
        height: 100
      }
    },
    opacity: {
      value: 1,
      random: false,
      anim: {
        enable: false,
        speed: 1,
        opacity_min: 0.1,
        sync: false
      }
    },
    size: {
      value: 8,
      random: true,
      anim: {
        enable: false,
        speed: 10,
        size_min: 10,
        sync: false
      }
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#808080",
      opacity: 0.4,
      width: 1
    },
    move: {
      enable: true,
      speed: 5,
      direction: "none",
      random: false,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: {
        enable: false,
        rotateX: 600,
        rotateY: 1200
      }
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "grab"
      },
      onclick: {
        enable: true,
        mode: "push"
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 140,
        line_linked: {
          opacity: 1
        }
      },
      bubble: {
        distance: 400,
        size: 40,
        duration: 2,
        opacity: 8,
        speed: 3
      },
      repulse: {
        distance: 200,
        duration: 0.4
      },
      push: {
        particles_nb: 4
      },
      remove: {
        particles_nb: 2
      }
    }
  },
  retina_detect: true
});