!function(e,t){var n=function(e){var t={};function n(a){if(t[a])return t[a].exports;var o=t[a]={i:a,l:!1,exports:{}};return e[a].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=e,n.c=t,n.d=function(e,t,a){n.o(e,t)||Object.defineProperty(e,t,{configurable:!1,enumerable:!0,get:a})},n.r=function(e){Object.defineProperty(e,"__esModule",{value:!0})},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=415)}({414:function(e,t){!function(e){"use strict";e.event.special.destroyed||(e.event.special.destroyed={remove:function(e){e.handler&&e.handler()}}),e.fn.extend({maxlength:function(t,n){var a=e("body");function o(e){var n=e.val();return n=t.twoCharLinebreak?n.replace(/\r(?!\n)|\n(?!\r)/g,"\r\n"):n.replace(new RegExp("\r?\n","g"),"\n"),t.utf8?function(e){for(var t=0,n=0;n<e.length;n++){var a=e.charCodeAt(n);a<128?t++:t+=a>127&&a<2048?2:3}return t}(n):n.length}function r(e,t){var n=t-o(e);return n}function s(e,t){t.css({display:"block"}),e.trigger("maxlength.shown")}function i(e,n,a){var o="";return t.message?o="function"==typeof t.message?t.message(e,n):t.message.replace("%charsTyped%",a).replace("%charsRemaining%",n-a).replace("%charsTotal%",n):(t.preText&&(o+=t.preText),t.showCharsTyped?o+=a:o+=n-a,t.showMaxLength&&(o+=t.separator+n),t.postText&&(o+=t.postText)),o}function l(e,n,a,r){r&&(r.html(i(n.val(),a,a-e)),e>0?function(e,n,a){var r=!0;return!t.alwaysShow&&a-o(e)>n&&(r=!1),r}(n,t.threshold,a)?s(n,r.removeClass(t.limitReachedClass).addClass(t.warningClass)):function(e,t){t.css({display:"none"}),e.trigger("maxlength.hidden")}(n,r):s(n,r.removeClass(t.warningClass).addClass(t.limitReachedClass))),t.allowOverMax&&(e<0?n.addClass("overmax"):n.removeClass("overmax"))}function c(n,a){var o=function(t){var n=t[0];return e.extend({},"function"==typeof n.getBoundingClientRect?n.getBoundingClientRect():{width:n.offsetWidth,height:n.offsetHeight},t.offset())}(n);if("function"!==e.type(t.placement))if(e.isPlainObject(t.placement))!function(n,a){if(n&&a){var o={};e.each(["top","bottom","left","right","position"],function(e,n){var a=t.placement[n];void 0!==a&&(o[n]=a)}),a.css(o)}}(t.placement,a);else{var r=n.outerWidth(),s=a.outerWidth(),i=a.width(),l=a.height();switch(t.appendToParent&&(o.top-=n.parent().offset().top,o.left-=n.parent().offset().left),t.placement){case"bottom":a.css({top:o.top+o.height,left:o.left+o.width/2-i/2});break;case"top":a.css({top:o.top-l,left:o.left+o.width/2-i/2});break;case"left":a.css({top:o.top+o.height/2-l/2,left:o.left-i});break;case"right":a.css({top:o.top+o.height/2-l/2,left:o.left+o.width});break;case"bottom-right":a.css({top:o.top+o.height,left:o.left+o.width});break;case"top-right":a.css({top:o.top-l,left:o.left+r});break;case"top-left":a.css({top:o.top-l,left:o.left-s});break;case"bottom-left":a.css({top:o.top+n.outerHeight(),left:o.left-s});break;case"centered-right":a.css({top:o.top+l/2,left:o.left+r-s-3});break;case"bottom-right-inside":a.css({top:o.top+o.height,left:o.left+o.width-s});break;case"top-right-inside":a.css({top:o.top-l,left:o.left+r-s});break;case"top-left-inside":a.css({top:o.top-l,left:o.left});break;case"bottom-left-inside":a.css({top:o.top+n.outerHeight(),left:o.left})}}else t.placement(n,a,o)}function p(e){var n="maxlength";return t.allowOverMax&&(n="data-bs-mxl"),e.attr(n)||e.attr("size")}return e.isFunction(t)&&!n&&(n=t,t={}),t=e.extend({showOnReady:!1,alwaysShow:!1,threshold:10,warningClass:"label label-success",limitReachedClass:"label label-important label-danger",separator:" / ",preText:"",postText:"",showMaxLength:!0,placement:"bottom",message:null,showCharsTyped:!0,validate:!1,utf8:!1,appendToParent:!1,twoCharLinebreak:!0,allowOverMax:!1},t),this.each(function(){var n,o,s=e(this);function f(){var f=i(s.val(),n,"0");n=p(s),o||(o=e('<span class="bootstrap-maxlength"></span>').css({display:"none",position:"absolute",whiteSpace:"nowrap",zIndex:1099}).html(f)),s.is("textarea")&&(s.data("maxlenghtsizex",s.outerWidth()),s.data("maxlenghtsizey",s.outerHeight()),s.mouseup(function(){s.outerWidth()===s.data("maxlenghtsizex")&&s.outerHeight()===s.data("maxlenghtsizey")||c(s,o),s.data("maxlenghtsizex",s.outerWidth()),s.data("maxlenghtsizey",s.outerHeight())})),t.appendToParent?(s.parent().append(o),s.parent().css("position","relative")):a.append(o);var h=r(s,p(s));l(h,s,n,o),c(s,o)}e(window).resize(function(){o&&c(s,o)}),t.allowOverMax&&(e(this).attr("data-bs-mxl",e(this).attr("maxlength")),e(this).removeAttr("maxlength")),t.showOnReady?s.ready(function(){f()}):s.focus(function(){f()}),s.on("maxlength.reposition",function(){c(s,o)}),s.on("destroyed",function(){o&&o.remove()}),s.on("blur",function(){o&&!t.showOnReady&&o.remove()}),s.on("input",function(){var e=p(s),a=r(s,e),i=!0;return t.validate&&a<0?(function(e,n){var a=e.val(),o=0;t.twoCharLinebreak&&"\n"===(a=a.replace(/\r(?!\n)|\n(?!\r)/g,"\r\n")).substr(a.length-1)&&a.length%2==1&&(o=1),e.val(a.substr(0,n-o))}(s,e),i=!1):l(a,s,n,o),"bottom-right-inside"!==t.placement&&"top-right-inside"!==t.placement||c(s,o),i})})}})}(jQuery)},415:function(e,t,n){n(414)}});if("object"==typeof n){var a=["object"==typeof module&&"object"==typeof module.exports?module.exports:null,"undefined"!=typeof window?window:null,e&&e!==window?e:null];for(var o in n)a[0]&&(a[0][o]=n[o]),a[1]&&"__esModule"!==o&&(a[1][o]=n[o]),a[2]&&(a[2][o]=n[o])}}(this);