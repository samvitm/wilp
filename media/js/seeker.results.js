Table = function( opts ) {
	this.opts = {
		url: '/search/',
		model: [],
		initial: [],
		imageDir: '/static/images/seeker/'
	};
	$.extend( this.opts, opts );
	
	this.fields = this.opts.model;
	this.fieldMap = {};
	
	for( var k = 0; k < this.fields.length; k++ )
		this.fieldMap[ this.fields[k].field ] = this.fields[k];
	
	this.sortField = null;
	this.sortDir = '';
	
	this.setDisplayFields( this.opts.initial, false );
	
	this.page = 0;
	this.pageSize = 25;
	this.table_id = 'resultsTable';
	
	// this is a local copy of the JSON string representation of a Search object
	// it is cached here, since we don't want a count operation to affect results paging
	this._criteria = null;
	
	this._rows = [];
	this._dragging = false;
	this._startIndex = -1;
	this._endIndex = -1;
};

Table.prototype = {
	
	setDisplayFields: function( initial, unformatByDefault ) {
		this.displayed = [];
		for( var k = 0; k < initial.length; k++ ) {
			var name = initial[k];
			if( name.charAt(0) == '+' ) {
				name = name.substr( 1 );
				this.fieldMap[name].formatted = true;
			}
			else if( unformatByDefault ) {
				this.fieldMap[name].formatted = false;
			}
			this.displayed.push( this.fieldMap[name] );
		}
	},
	
	getDisplayFields: function() {
		var display_fields = [];
		for( var k = 0; k < this.displayed.length; k++ ) {
			var name = this.displayed[k].field;
			if( this.displayed[k].formatted )
				name = '+' + name;
			display_fields.push( name );
		}
		return display_fields;
	},
	
	setSortField: function( field ) {
		this.sortDir = '';
		this.sortField = field;
		if( (field.charAt(0) == '-') || (field.charAt(0) == '+') ) {
			this.sortDir = field.charAt( 0 );
			this.sortField = field.substr( 1 );
		}
	},
	
	getSortField: function() {
		if( this.sortField != null )
			return this.sortDir + this.sortField;
		return null;
	},
	
	takeCriteriaFrom: function( from ) {
		this._criteria = JSON.stringify( from );
	},
	
	toJSON: function() {
		return {
			criteria: JSON.parse(this._criteria),
			display_fields: this.getDisplayFields(),
			sort_field: this.getSortField()
		};
	},
	
	toggleDisplay: function( field ) {
		for( var k = 0; k < this.displayed.length; k++ ) {
			if( this.displayed[k].field == field ) {
				var name = this.displayed[k].label;
				this.displayed.splice( k, 1 );
				return name;
			}
		}
		for( k = 0; k < this.fields.length; k++ ) {
			if( this.fields[k].field == field ) {
				this.displayed.push( this.fields[k] );
				return String.fromCharCode(8226) + ' ' + this.fields[k].label;
			}
		}
	},
	
	renderHeader: function( html ) {
		html.append( '<thead><tr>' );
		for( var k = 0; k < this.displayed.length; k++ ) {
			html.append( '<th id="header_', this.displayed[k].field, '"' );
			if( this.displayed[k].field == this.sortField )
				html.append( ' class="sort"' );
			html.append( '><img class="thumb" src="', this.opts.imageDir, 'thumb.gif" />' );
			html.append( '<a href="#">', this.displayed[k].label, '</a>' );
			if( this.displayed[k].field == this.sortField ) {
				var ch = (this.sortDir == '-') ? String.fromCharCode(9660) : String.fromCharCode(9650);
				html.append( '&nbsp;', ch );
			}
			if( this.displayed[k].type == 'lookup' ) {
				html.append( '<input type="checkbox" value="', this.displayed[k].field, '"' );
				if( this.displayed[k].formatted )
					html.append( ' checked="checked"' );
				html.append( ' />' );
			}
			html.append( '</th>' )
		}
		html.append( '</tr></thead>' )
	},
	
	renderRow: function( html, index, row ) {
		var cls = (index % 2 == 0) ? 'even' : 'odd';
		html.append( '<tr class="', cls, '">' );
		for( var k = 0; k < this.displayed.length; k++ ) {
			var vals = row[ this.displayed[k].field ];
			var value = vals[0];
			if( this.displayed[k].formatted && (vals.length > 1) )
				value = vals[1];
			html.append( '<td' );
			if( this.displayed[k].field == this.sortField )
				html.append( ' class="sort"' );
			html.append( '>', value, '</td>' );
		}
		html.append( '</tr>' );
	},
	
	_attachDragHandlers: function() {
		var t = this;
		$('#' + t.table_id + ' th .thumb').mousedown( function() {
			t.dragStart( this.parentNode );
			return false;
		} );
		$('#' + t.table_id + ' th').mouseover( function() {
			if( t._dragging ) t.dragEnter( this );
		} ).mouseout( function() {
			if( t._dragging ) t.dragLeave( this );
		} );
	},
	
	redraw: function() {
		var html = new StringBuffer();
		html.append( '<table id="', this.table_id, '" cellpadding="0" cellspacing="0">' );
		this.renderHeader( html );
		html.append( '<tbody>' );
		for( var k = 0; k < this._rows.length; k++ ) {
			this.renderRow( html, k, this._rows[k] );
		}
		if( this._rows.length == 0 ) {
			html.append( '<tr><td class="message" colspan="', this.displayed.length, '">Please select your search criteria above and press Search.</td></tr>' );
		}
		html.append( '</tbody></table>' );
		$('#' + this.table_id).replaceWith( html.toString() );
		$('#' + this.table_id + ' th').each( function(idx) {
			$(this).attr( 'index', '' + idx );
		} );
		var t = this;
		$('#' + this.table_id + ' th input').click( function() {
			for( var k = 0; k < t.displayed.length; k++ ) {
				if( t.displayed[k].field == $(this).val() ) {
					t.displayed[k].formatted = this.checked;
					if( t._rows.length > 0 )
						t.redraw();
				}
			}
		} );
		$('#' + this.table_id + ' th a').each( function(idx) {
			var field = t.displayed[idx].field;
			$(this).click( function() {
				t.sort( field );
			} );
		} );
		this._attachDragHandlers();
	},
	
	sort: function( field ) {
		if( field == this.sortField ) {
			this.sortDir = (this.sortDir == '') ? '-' : '';
		}
		else {
			this.sortField = field;
			this.sortDir = '';
		}
		if( this._rows.length > 0 ) {
			$('#pageInput').val( 1 );
			this.reload();
		}
		else
			this.redraw();
	},
	
	saveValues: function() {
		this.page = parseInt( $('#pageInput').val() );
		this.pageSize = parseInt( $('#pageSize').val() );
	},
	
	reload: function() {
		this.saveValues();
		var params = {
			search: JSON.stringify( this ),
			page: this.page,
			page_size: this.pageSize
		};
		var t = this;
		$('#resultCount').hide();
		$('#resultLoading').show();
		$.post( this.opts.url + 'render/', params, function(data,status) {
			t._rows = data.rows;
			$('#pageInput').val( data.page );
			$('#pageCount').text( data.pages );
			$('#rowStart').text( data.start );
			$('#rowEnd').text( data.end );
			$('#rowTotal').text( data.count );
			$('#pagerForm').show();
			data.has_next ? $('#nextPageBtn').show() : $('#nextPageBtn').hide();
			data.has_prev ? $('#prevPageBtn').show() : $('#prevPageBtn').hide();
			$('#resultLoading').hide();
			$('#resultCount').show();
			t.redraw();
		}, 'json' );
	},
	
	save: function( name ) {
		var params = {
			search: JSON.stringify( this ),
			name: name
		};
		$('#resultCount').hide();
		$('#resultLoading').show();
		$.post( this.opts.url + 'save/', params, function(data,status) {
			$('#resultLoading').hide();
			$('#resultCount').show();
			$('#saveForm').hide();
			$('#saveBtn').replaceWith( '<span>Search saved.</span>' );
		}, 'json' );
	},
	
	nextPage: function() {
		$('#pageInput').val( this.page + 1 );
		this.reload();
	},
	
	prevPage: function() {
		$('#pageInput').val( this.page - 1 );
		this.reload();
	},
	
	dragStart: function( th ) {
		var offset = $(th).offset();
		this._startIndex = parseInt( $(th).attr('index') );
		var html = '<div id="drag">' + $(th).text() + '</div>';
		$(html).css( {
			top: '' + (offset.top + 1) + 'px',
			left: '' + (offset.left + 1) + 'px'
		} ).appendTo( 'body' );
		this._dragging = true;
		var t = this;
		$('body').mousemove( function(e) {
			t.dragTo( e );
		} ).mouseup( function() {
			t.dragEnd();
		} );
	},
	
	dragTo: function( e ) {
		if( this._dragging ) {
			$('#drag').css( {
				top: '' + (e.pageY + 1) + 'px',
				left: '' + (e.pageX + 1) + 'px'
			} );
		}
	},
	
	dragEnd: function() {
		this._dragging = false;
		$('body').unbind( 'mousemove' ).unbind( 'mouseup' );
		$('#drag').remove();
		if( (this._endIndex >= 0) && (this._startIndex != this._endIndex) ) {
			var tmp = this.displayed[ this._startIndex ];
			this.displayed.splice( this._startIndex, 1 );
			this.displayed.splice( this._endIndex, 0, tmp );
/*
			var tmp = this.displayed[ this._endIndex ];
			this.displayed[ this._endIndex ] = this.displayed[ this._startIndex ];
			this.displayed[ this._startIndex ] = tmp;
*/
			this.redraw();
		}
		else {
			$('#' + this.table_id + ' th').removeClass( 'dropCol' );
		}
	},
	
	dragEnter: function( th ) {
		$(th).addClass( 'dropCol' );
		this._endIndex = parseInt( $(th).attr('index') );
	},
	
	dragLeave: function( th ) {
		$(th).removeClass( 'dropCol' );
		this._endIndex = -1;
	}
	
};
