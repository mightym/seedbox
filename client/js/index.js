'use strict';

var Isotope = require('isotope-layout');
var FastClick = require('fastclick');

$(document).ready(function() {

  var browserwidth = $(window).width();
  var browserheight = $(window).height();
  var container = document.querySelector('.project-grid');

  var fc = FastClick(document.body);

  var iso = new Isotope( container , {
    itemSelector: '.project-item',
    layoutMode: 'masonry',
    // transitionDuration: 0,
    masonry: {
      columnWidth: 60
    },
    getSortData: {
      name: '.name',
      symbol: '.symbol',
      number: '.number parseInt',
      category: '[data-slug]',
    }
  });


  $(window).resize(function () {
    browserwidth = $(window).width();
    browserheight = $(window).height();
  });

});

