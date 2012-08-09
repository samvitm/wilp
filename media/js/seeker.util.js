function createSelect( html, id, cls, opts, sel ) {
	html.append( '<select' );
	if( id != null )
		html.append( ' id="', id, '"' )
	if( cls != null )
		html.append( ' class="', cls, '"' )
	html.append( '>' );
	for( var k = 0; k < opts.length; k++ ) {
		html.append( '<option value="', opts[k][0], '"' );
		if( sel == opts[k][0] )
			html.append( ' selected="selected"' );
		html.append( '>', opts[k][1], '</option>' );
	}
	html.append( '</select>' );
};

function getOffsetCSS( container_id, obj ) {
	var parentOffset = $('#' + container_id).offset();
	var objOffset = $(obj).offset();
	return {
		'top': '' + (objOffset.top - parentOffset.top) + 'px',
		'left': '' + (objOffset.left - parentOffset.left) + 'px'
	};
};

var StringBuffer = function() {
	this._buffer = [];
	this._cache = null;
};

StringBuffer.prototype = {
	
	append: function() {
		this._cache = null;
		for( var k = 0; k < arguments.length; k++ )
			this._buffer.push( arguments[k] );
		return this;
	},
	
	toString: function() {
		if( this._cache == null )
			this._cache = this._buffer.join( "" );
		return this._cache;
	}
	
};

var Selector = function( id, values, selected, ok_callback ) {
	this.id = id;
	this.values = values;
	this.ok_callback = ok_callback;
	
	// keep a cache of selected values to avoid a nested loop
	this._hasValue = {};
	
	this.setSelected( selected );
	this._html = this.render();
};

Selector.prototype = {
	
	setSelected: function( selected ) {
		this._hasValue = {};
		for( var k = 0; k < selected.length; k++ )
			this._hasValue[ selected[k] ] = true;
	},
	
	render: function() {
		var html = new StringBuffer();
		html.append( '<div class="scrollable">' );
		for( var k = 0; k < this.values.length; k++ ) {
			var cls = (k % 2 == 0) ? 'even' : 'odd';
			html.append( '<div class="', cls, '"><input id="_sel_id_', k, '" type="checkbox" value="', this.values[k][0], '"' );
			if( this._hasValue[ this.values[k][0] ] )
				html.append( ' checked="checked"' );
			html.append( ' /> <label for="_sel_id_', k, '" rel="', this.values[k][0], '">', this.values[k][1], '</label></div>' );
		}
		html.append( '</div><div class="buttons">' );
		html.append( '<input type="text" id="selectorFilter" size="8" />' );
		html.append( '&nbsp;&nbsp;<input type="button" id="selectorCancelBtn" value="Cancel" />' );
		html.append( '&nbsp;<input type="button" id="selectorOkBtn" value="OK" />' );
		html.append( '</div>' );
		return html.toString();
	},
	
	show: function( css ) {
		$('#' + this.id).empty().append( this._html );
		var t = this;
		$('#' + this.id + ' input').removeAttr('checked').each( function(idx) {
			if( t._hasValue[ $(this).val() ] )
				$(this).attr( 'checked', 'checked' );
		} );
		$('#selectorCancelBtn').click( function() {
			t.hide();
		} );
		$('#selectorOkBtn').click( function() {
			t.hide();
			if( typeof(t.ok_callback) == 'function' ) {
				var selectedValues = [];
				$('#' + t.id + ' .scrollable input:checked').each( function(idx) {
					selectedValues.push( $(this).val() );
				} );
				t.ok_callback( selectedValues );
			}
		} );
		$('#selectorFilter').keyup( function(e) {
			var search = $(this).val().toLowerCase();
			$('#selector label').each( function() {
				var rel = $(this).attr( 'rel' ) || '';
				if( search.length > 0 && $(this).text().toLowerCase().indexOf(search) == -1 && rel.toLowerCase().indexOf(search) == -1 )
					$(this).parent().hide();
				else
					$(this).parent().show();
			} );
		} );
		$('#' + this.id).css( css ).show( 'fast', function() {
			$('#selectorFilter').focus();
		} );
	},
	
	hide: function() {
		$('#' + this.id).hide( 'fast' );
	}
};
