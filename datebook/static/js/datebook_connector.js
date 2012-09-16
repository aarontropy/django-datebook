
(function($){
 
    //Attach this new method to jQuery
    $.fn.extend({ 
         
        //This is where you write your plugin's name
        django-datebook-connector: function(options) {

        	var defaults = {
        		datepicker-options: {},
        		timepicker-options: {},

        	}
        	var options = $.extend(defaults,options);
 
            //Iterate over the current set of matched elements
            return this.each(function() {
             
                //code to be inserted here
             
            });
        }
    });
     
//pass jQuery to the function, 
//So that we will able to use any valid Javascript variable name 
//to replace "$" SIGN. But, we'll stick to $ (I like dollar sign: ) )       
})(jQuery);