
(function($){
 
	//==========================================================================
	// METHODS
	var methods = {
		//----------------------------------------------------------------------
		init: function(options){		
	    	var defaults = {
	    		datepicker: {},
	    		timepicker: {},
	    		create_url: '',				// url used to create new events
	    		update_url: '',				// url used to edit events
	    		delete_url: '',				// url used to delete events
	    		event_url: '',				// retrieves form and model data for event
	    		event_form: '',				// gets form html for event
	    		series_form: '',			// gets form html for series
	    		event_fields: [],
	    		series_fields: [],
	    		datebook_id: 0,
	    		csrfmiddlewaretoken: '',

	    	}
	    	var options = $.extend(defaults,options);

			return this.each(function() {
				$(this).append('<div class="dialog"><form><input type="hidden" name="csrfmiddlewaretoken" id="id_csrfmiddlewaretoken" value="' + options.csrfmiddlewaretoken + '" /><table></table></form></div>')
				var $dlg = $(this).find(".dialog");
				$(this).data('options', options);
				$(this).data('dialog', $dlg);
				$dlg.data('plugin', $(this));

				
				$(this).data("dialog").dialog({
					autoOpen: false,
					width: 450,
					buttons: {
						Save: function() {
							var data = $(this).django_datebook_connector('formToObject');
							var plugin = $(this).data('plugin');
							data['datebook'] = plugin.data('options').datebook_id;
							plugin.django_datebook_connector('postEvent', data, plugin.data('options').create_url);
							$( this ).dialog('close');
						},
						Cancel: function() {
							$( this ).dialog('close');
						},
					},
				});


				$(this).bind('timeslot-click', methods.showCreate );
				$(this).bind('event-click', methods.showUpdate );

				// dialog









			});

		},
		//----------------------------------------------------------------------
		postEvent: function(data, url) {
			$.post(url, data, function(answer) {
				if (answer.error) {
				 	alert(answer.error + "\n-----\n" + answer.message);
				 	return false;
				} else {
					$.event.trigger('postEvent-success', [answer]);
					return true;
				}
			});
		},
		//----------------------------------------------------------------------
		postCreate: function(data) {
			alert('postCreate');
		},
		//----------------------------------------------------------------------
		postUpdate: function(data) {
			// get form data
			//post data
			alert('postUpdate');
		},
		//----------------------------------------------------------------------
		postDelete: function(data) {
			alert('postDelete');
		},
		//----------------------------------------------------------------------
		showCreate: function(event, start, end, allDay) {
			// update form html
			var data = { 
				'csrfmiddlewaretoken': $(this).data('options').csrfmiddlewaretoken,
				'start': start.toISOString(),
				'end': end.toISOString(),
				'offset': start.getTimezoneOffset(),
				'allDay': allDay,
			};

			var dlg = $(this).data('dialog');
			$.post($(this).data("options").event_form_url, data, function(answer) {
				if (answer.error) {
					alert("Error: " + answer.error);
				} else {
					dlg.find("table").html(answer.as_table);
					dlg.dialog('open').show();
					// $( this ).dialog( "close" );
				}

			});

		},
		//----------------------------------------------------------------------
		showUpdate: function(calEvent) {
			// get event data
			console.log(calEvent);
			var data = {
				'csrfmiddlewaretoken': $(this).data('options').csrfmiddlewaretoken,
				'event_id': calEvent.event_id,
			};
			// update form html
			var dlg = $(this).data('dialog');
			$.post($(this).data("options").event_form_url, data, function(answer) {
				if (answer.error) {
					alert("Error: " + answer.error);
				} else {
					dlg.find("table").html(answer.as_table);
					dlg.dialog('open').show();
				}

			});
			// initialize form data
			// show popup
		},
		formToObject: function() {
			data = {};
			$(this).find("form").find("input").each(function(idx, el) {
				var n = el.name, v = el.value;
				data[n] = data[n] === undefined ? v 
					: $.isArray( data[n] ) ? data[n].concat(v)
					: [obj[n], v ];
			});
			return data;
		}
	};

	//==========================================================================
	// PLUGIN
    $.fn.extend( {
    	django_datebook_connector: function( method ) { 
	    	if ( methods[method] ) {
		      return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
		    } else if ( typeof method === 'object' || ! method ) {
		      return methods.init.apply( this, arguments );
		    } else {
		      $.error( 'Method ' +  method + ' does not exist' );
		    }
		}
    });
     
})(jQuery);