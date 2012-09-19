
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
				$(this).bind('event-drop', methods.updateEvent );

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
		updateEvent: function(event, calEvent) {
			// make sure there is an event_id in calEvent
			if (calEvent.hasOwnProperty('event_id')) {
				// get a form with all the right initial values in all the right places

			}
		},
		//----------------------------------------------------------------------
		showCreate: function(event, start, end, allDay) {
			// update form html
			var data = { 
				'start': start.toISOString(),
				'end': end.toISOString(),
				'offset': start.getTimezoneOffset(),
				'allDay': allDay,
			};

			var dlg = $(this).data('dialog');
			$(this).django_datebook_connector('getFormHTML',data);
			dlg.dialog('open').show();

		},
		//----------------------------------------------------------------------
		showUpdate: function(event, calEvent) {
			// update form html
			var dlg = $(this).data('dialog');
			$(this).django_datebook_connector('getFormHTML',calEvent.event_id);
			dlg.dialog('open').show();

		},
		getFormHTML: function(init, init2) {
			var data = {'csrfmiddlewaretoken': $(this).data('options').csrfmiddlewaretoken};
			var html = '';
			if(init) {
				if (typeof(init) === 'object') $.extend(data, init);
				else if (typeof(init) === 'number') data['event_id'] = init;
			}
			if(init2) {
				if (typeof(init2) === 'object') $.extend(data, init2);
				else if (typeof(init2) === 'number') data['event_id'] = init2;
			}
			var url = $(this).data("options").event_form_url;
			var dlg = $(this).data('dialog');
			console.log(data);
			$.post(url, data, function(answer) {
				if (answer.error) {
					alert(answer.error + "\n-----\n" + answer.message);
				} else {
					dlg.find("table").html( answer.as_table );
				}
			});
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