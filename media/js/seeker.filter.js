var Criteria = function( info, search, oper, values ) {
	this.search = search;
	this.field = info['field'];
	this.name = info['name'];
	this.type = info['type'];
	this.operators = info['operators'];
	this.operator = oper ? oper : this.operators[0][0];
	this.lookups = info['values'];
	this.values = values ? values : [null];
	this.tbody_id = 'filter_' + this.field + '_criteria';
	this.operator_id = 'filter_' + this.field + '_operator';
	this.value_class = 'filter_' + this.field + '_value';
	this.selector = null;
	// true after the tbody has been added to the filter table
	this._added = false;
};

Criteria.prototype = {
	
	saveValues: function() {
		var values = this.values;
		$('.' + this.value_class).each( function(k) {
			if( k < values.length )
				values[k] = $(this).val();
		} );
		this.operator = $('#' + this.operator_id).val();
	},
	
	addLine: function() {
		this.saveValues();
		this.values.push( null );
		this.redraw();
	},
	
	removeLine: function( index ) {
		this.saveValues();
		var newValues = [];
		for( var k = 0; k < this.values.length; k++ ) {
			if( k != index )
				newValues.push( this.values[k] );
		}
		this.values = newValues;
		if( this.values.length > 0 ) {
			this.redraw();
			return false;
		}
		else {
			$('#'+this.tbody_id).remove();
			return true;
		}
	},
	
	showSelector: function( obj ) {
		this.saveValues();
		if( this.selector == null ) {
			var t = this;
			this.selector = new Selector( 'selector', this.lookups, this.values, function(values) {
				t.values = values;
				t.redraw();
			} );
		}
		else {
			this.selector.setSelected( this.values );
		}
		this.selector.show( getOffsetCSS('search',obj) );
	},
	
	showImport: function( obj ) {
		var html = new StringBuffer();
		html.append( '<form action="', this.search.opts.url, 'import/" method="post" id="importForm" style="padding:6px;">' );
		html.append( '<input type="file" name="datafile" /><br /><br />' );
		html.append( '<input type="hidden" name="field" value="', this.field, '" />' );
		html.append( '<input type="submit" value="Import" /> ' );
		html.append( '<input id="importCancel" type="button" value="Cancel" />' );
		html.append( '</form>' );
		var css = getOffsetCSS( 'search', obj );
		$('#selector').empty().append( html.toString() ).css( css ).show( 'fast' );
		$('#importCancel').click( function() {
			$('#selector').hide( 'fast' );
		} );
		var t = this;
		$('#importForm').ajaxForm( {
			dataType: 'json',
			success: function(data) {
				$('#selector').hide( 'fast' );
				t.finishImport( data );
			}
		} );
	},
	
	finishImport: function( data ) {
		this.values = [ data ];
		this.redraw();
	},
	
	renderWidget: function( html, index, value ) {
		switch( this.type ) {
			case 'text':
				html.append( '<input type="text" class="', this.value_class, '" value="', value, '" />' );
				break;
			
			case 'numeric':
				html.append( '<input type="text" size="10" class="', this.value_class, '" value="', value, '" />' );
				break;
			
			case 'boolean':
				var bools = [['1','True'],['0','False']];
				createSelect( html, null, this.value_class, bools, value );
				break;
			
			case 'lookup':
				createSelect( html, null, this.value_class, this.lookups, value );
				break;
			
			case 'date':
				html.append( '<input type="text" size="11" class="', this.value_class, ' dateField" value="', value, '" />' );
				break;
		}
	},
	
	renderRow: function( html, index, value, is_last ) {
		html.append( '<tr>' );
		if( index == 0 ) {
			html.append( '<td class="field">', this.name, '</td><td class="operator">' );
			createSelect( html, this.operator_id, null, this.operators, this.operator );
			html.append( '</td>' );
		}
		else {
			html.append( '<td></td><td class="operator">or</td>' );
		}
		
		html.append( '<td class="value">' );
		this.renderWidget( html, index, value );
		html.append( '</td>' );
		
		if( index == 0 ) {
			if( this.type == 'text' || this.type == 'numeric' )
				html.append( '<td><img src="', this.search.opts.imageDir, 'import.gif" class="importBtn" /></td>' );
			else if( this.type == 'lookup' )
				html.append( '<td><img src="', this.search.opts.imageDir, 'select.gif" class="selectValuesBtn" /></td>' );
			else
				html.append( '<td></td>' );
		}
		else html.append( '<td></td>' );
		
		html.append( '<td>' );
		html.append( '<img src="', this.search.opts.imageDir, 'minus.gif" class="removeLineBtn" />' );
		if( is_last )
			html.append( '&nbsp;<img src="', this.search.opts.imageDir, 'plus.gif" class="addLineBtn" />' );
		html.append( '</td></tr>' );
	},
	
	render: function() {
		var html = new StringBuffer();
		html.append( '<tbody id="', this.tbody_id, '">' );
		for( var k = 0; k < this.values.length; k++ ) {
			this.renderRow( html, k, this.values[k], (k == (this.values.length - 1)) );
		}
		html.append( '</tbody>' );
		return html.toString();
	},
	
	redraw: function() {
		if( this._added )
			$('#' + this.tbody_id).replaceWith( this.render() );
		else {
			if( this.search.opts.insertAtTop )
				$('#filterTable').prepend( this.render() );
			else
				$('#filterTable').append( this.render() );
		}
		
		var t = this;
		$('#' + this.tbody_id + ' .dateField').datepicker( {
			showOn: 'button',
			buttonImage: t.search.opts.imageDir + 'calendar.gif',
			buttonImageOnly: true
		} );
		$('#' + this.tbody_id + ' .selectValuesBtn').click( function() {
			t.showSelector( this );
		} );
		$('#' + this.tbody_id + ' .importBtn').click( function() {
			t.showImport( this );
		} );
		$('#' + this.tbody_id + ' .addLineBtn').click( function() {
			t.addLine();
		} );
		$('#' + this.tbody_id + ' .removeLineBtn').each( function(idx) {
			$(this).click( function() {
				t.search.removeLine( t.field, idx );
			} );
		} );
		this._added = true;
	},
	
	toJSON: function( key ) {
		return {
			field: this.field,
			operator: this.operator,
			values: this.values
		};
	}
	
};

var Search = function( opts ) {
	this.criteria = [];
	this.opts = {
		'url': '/search/',
		'imageDir': '/static/images/seeker/',
		'insertAtTop': false,
		'collapseOnSearch': true
	};
	$.extend( this.opts, opts );
};

Search.prototype = {
	
	hasCriteria: function() {
		return this.criteria.length > 0;
	},
	
	addCriteria: function( info, oper, values ) {
		if( !this.addLine(info['field']) ) {
			var crit = new Criteria( info, this, oper, values );
			this.criteria.push( crit );
			crit.redraw();
		}
	},
	
	findCriteria: function( field ) {
		for( var k = 0; k < this.criteria.length; k++ ) {
			if( this.criteria[k].field == field )
				return this.criteria[k];
		}
		return null;
	},
	
	addLine: function( field ) {
		var crit = this.findCriteria( field );
		if( crit != null ) {
			crit.addLine();
			return true;
		}
		return false;
	},
	
	removeLine: function( field, index ) {
		var crit = this.findCriteria( field );
		if( crit != null ) {
			if( crit.removeLine( index ) ) {
				var newCrit = [];
				for( var k = 0; k < this.criteria.length; k++ ) {
					if( this.criteria[k] != crit )
						newCrit.push( this.criteria[k] );
				}
				this.criteria = newCrit;
			}
		}
	},
	
	clear: function() {
		this.criteria = [];
		$('#filterTable').empty();
	},
	
	count: function() {
		var params = {
			search: JSON.stringify( {criteria: this.criteria} )
		};
		$('#countSpan').hide();
		$('#searchLoading').show();
		$.post( this.opts.url + 'count/', params, function(data,status) {
			$('#searchCount').text( data );
			$('#searchLoading').hide();
			$('#countSpan').show();
		}, 'json' );
	},
	
	saveValues: function() {
		for( var k = 0; k < this.criteria.length; k++ )
			this.criteria[k].saveValues();
	},
	
	toJSON: function( key ) {
		return this.criteria;
	}

};
