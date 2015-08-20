'use strict';

var Isotope = require('isotope-layout');
var FastClick = require('fastclick');

$(document).ready(function() {

  var ratio = 900/1440 ;
  var browserwidth = $(window).width();
  var browserheight = $(window).height();
  var browserXCenter = browserheight / 2;
  var browserYCenter = browserwidth / 2;
  var slideimages = $('.scale-me');
  var slides = $('.slide');


function fillemup(){

  $(slides).height(browserheight);
  $(slides).width(browserwidth);

  slideimages.each(function (index, bgImg) {
    if ((browserheight/browserwidth) > ratio) {
      if(browserwidth >= 500 ){
        $(bgImg).width(browserheight / ratio);
        $(bgImg).height(browserheight);
      } else {
        $(bgImg).width(browserheight / ratio);
        $(bgImg).height(browserheight);
      }
    } else {
      $(bgImg).width( browserwidth );
      $(bgImg).height( browserwidth * ratio );
    };

    // CENTER IMGS VERTICALLY + HORIZONTALLY
    var bgImgWidth = $(bgImg).width();
    var bgImgHeight = $(bgImg).height();
    var bgImgLeft = ( browserwidth - bgImgWidth) /2;
    var bgImgTop = ( browserheight - bgImgHeight) /2;
    $(bgImg).css('left', bgImgLeft);
    $(bgImg).css('top', bgImgTop);
  });
};


  var container = document.querySelector('.project-grid');

  var fc = FastClick(document.body);

  if (container) {
    var iso = new Isotope( container , {
      itemSelector: '.project-item',
      layoutMode: 'masonry',
      transitionDuration: 0,
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
  }

  $(window).resize(function () {
    browserwidth = $(window).width();
    browserheight = $(window).height();
    browserXCenter = browserheight / 2
    browserYCenter = browserwidth / 2
    fillemup();
  });

fillemup();

});

