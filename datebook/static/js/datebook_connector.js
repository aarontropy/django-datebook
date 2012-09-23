
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
					buttons: [
						{	// --==SAVE==--
							id: "button-save-event",
							text: "Save",
							click: function() {
								var data = formToObject($(this).find("form"));
								var plugin = $(this).data('plugin');
								data['datebook'] = plugin.data('options').datebook_id;

								if (data['id'] == '') {
									var url = plugin.data('options').create_url;
								} else {
									var url = plugin.data('options').update_url;
								}
								console.log(data);

								plugin.django_datebook_connector('postEvent', data, url);
								$( this ).dialog('close');
							},
						},
						{	// --==CANCEL==--
							id: "button-cancel-event",
							text: "Cancel",
							click: function() {
								$( this ).dialog('close');
							}
						},
						{	// --==DELETE==--
							id: "button-delete-event",
							text: "Delete",
							click: function() {
								var data = formToObject($(this).find("form"));
								var url = $(this).data('plugin').data('options').delete_url;
								var dlg = $( this );
								post(url, data, function(answer) {
									$.event.trigger('postEvent-success', [answer]);
									dlg.dialog('close');
								});
							}
						}

					],
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
			var formurl = $(this).data('options').event_form_url;
			var url = $(this).data('options').update_url;
			var csrf = $(this).data('options').csrfmiddlewaretoken;
			var data = {
				'csrfmiddlewaretoken': csrf,
				'start': calEvent.start.toLocaleString(),
				'end': calEvent.end.toLocaleString(),
				'event_id': calEvent.event_id,
			};
			post(formurl, data, function(answer) {
				var data = {'csrfmiddlewaretoken': csrf};
				$.extend(data, formToObject($(answer.as_table)));
				post(url, data, function(answer2){});

			} );
			// get a form with all the data in the right places
			// serialize the formdata and post
			//revert if fail
		},
		//----------------------------------------------------------------------
		showCreate: function(event, start, end, allDay) {
			// update form html

			
			var data = { 
				'start': start.toLocaleString(), //.toISOString(),
				'end': end.toLocaleString(), //.toISOString(),
				'allDay': allDay,
			};

			var dlg = $(this).data('dialog');
			$(this).django_datebook_connector('getFormHTML',data);
			// There should be no delete button since this is a new event
			$("#button-delete-event").button('disable');

			dlg.dialog('open').show();

		},
		//----------------------------------------------------------------------
		showUpdate: function(event, calEvent) {
			// update form html
			var dlg = $(this).data('dialog');
			$(this).django_datebook_connector('getFormHTML',calEvent.event_id);
			// Make sure the delete button is enabled
			$("#button-delete-event").button('enable');

			dlg.dialog('open').show();

		},
		setFormHTML: function(html) {
//			var html = methods.getFormHTML(init, init2);
			$(this).data('dialog').find("table").html( html );
		},
		getFormHTML: function(init, init2) {
			var data = {'csrfmiddlewaretoken': $(this).data('options').csrfmiddlewaretoken};
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

			post(url, data, function(answer) {
				dlg.find("table").html( answer.as_table );
			});
		},
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

	//==========================================================================
	// FUNCTIONS
	var post = function(url, data, callback) {
		$.post(url, data, function(answer) {
			if (answer.error) {
				alert(answer.error + "\n-----\n" + answer.message);
			} else {
				callback(answer);
			}
		});

	};

	var formToObject = function($form) {
		data = {};
		$form.find("input, select").each(function(idx, el) {
			var n = el.name, v = el.value;
			data[n] = data[n] === undefined ? v 
				: $.isArray( data[n] ) ? data[n].concat(v)
				: [obj[n], v ];
		});
		return data;
	};

     
})(jQuery);