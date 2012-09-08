function prettyDateTime(d) {
	
	var days = new Array("Sunday", "Monday", "Tuesday"," Wednesday", "Thursday", "Friday", "Saturday");
	var months = new Array("January","February","March","April","May","June","July","August","September","October","November","December");

	var day = days[d.getDay()];
	var dayofmonth = d.getDate();
	var month = months[d.getMonth()];
	var hours = d.getHours();
	var minutes = d.getMinutes();

	if (minutes < 10)
		minutes = "0" + minutes;

	var suffix = "AM";
	if (hours >= 12) {
		suffix = "PM";
		hours = hours - 12;
	}
	if (hours == 0) {
		hours = 12;
	}

	return day + ", " + month + " " + dayofmonth + ", " + hours + ":" + minutes + " " + suffix;
}

/*!
 * jQuery serializeObject - v0.2 - 1/20/2010
 * http://benalman.com/projects/jquery-misc-plugins/
 * 
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */

// Whereas .serializeArray() serializes a form into an array, .serializeObject()
// serializes a form into an (arguably more useful) object.

(function($,undefined){
  '$:nomunge'; // Used by YUI compressor.
  
  $.fn.serializeObject = function(){
    var obj = {};
    
    $.each( this.serializeArray(), function(i,o){
      var n = o.name,
        v = o.value;
        
        obj[n] = obj[n] === undefined ? v
          : $.isArray( obj[n] ) ? obj[n].concat( v )
          : [ obj[n], v ];
    });

    //added by ARJ
    //obj['POST'] = this.serialize();
    
    return obj;
  };
  
})(jQuery);