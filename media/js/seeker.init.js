$(document).ready( function() {
	table.redraw();
	
	$('#addBtn').click( function() {
		var field = $('#filterField').val();
		if( typeof(field_info[field]) == 'undefined' ) {
			$('#countSpan').hide();
			$('#searchLoading').show();
			$.getJSON( base_url + 'info/', {'field':field}, function(data,status) {
				field_info[data.field] = data;
				search.addCriteria( data );
				$('#searchLoading').hide();
			} );
		}
		else search.addCriteria( field_info[field] );
	} );
	
	$('#clearBtn').click( function() {
		search.clear();
	} );
	
	$('#collapseBtn').toggle(
		function() {
			$('#filters').hide( 'fast' )
		},
		function() {
			$('#filters').show( 'fast' )
		}
	);
	
	$('#searchBtn').click( function() {
		search.saveValues();
		if( search.hasCriteria() ) {
			$('#pageInput').val( '1' );
			table.takeCriteriaFrom( search );
			table.reload();
		}
	} );
	
	$('#countBtn').click( function() {
		search.saveValues();
		if( search.hasCriteria() )
			search.count();
	} );
	
	$('#saveBtn').click( function() {
		$(this).hide();
		$('#saveForm').css( 'display', 'inline' );
		$('#searchName').focus();
	} );
	
	$('#doSaveBtn').click( function() {
		search.saveValues();
		if( search.hasCriteria() ) {
			table.takeCriteriaFrom( search );
			table.save( $('#searchName').val() );
		}
	} );
	
	$('#cancelSaveBtn').click( function() {
		$('#saveForm').hide();
		$('#saveBtn').show();
	} );
	
	$('#loadSearchBtn').click( function() {
		var id = $('#savedSearchSelect').val();
		if( id.length > 0 )
			window.location = base_url + '?id=' + id;
	} );
	
	$('#pageSize').change( function() {
		if( table._criteria != null ) {
			$('#pageInput').val( '1' );
			table.reload();
		}
	} );
	
	$('#pagerForm').submit( function() {
		table.reload();
		return false;
	} );
	
	$('#displaySelect').change( function() {
		var opt = $('option:selected',this);
		var txt = table.toggleDisplay( opt.val() );
		table.redraw();
		opt.text( txt );
		$(this).val( '' );
	} );
	
	$('#exportBtn').click( function() {
		$('#exportFormat').val( $('#exportFormatSelect').val() );
		$('#exportSearch').val( JSON.stringify(table) );
		$('#exportForm').submit();
	} );
	
	$('#prevPageBtn').click( function() {
		table.prevPage();
	} );
	
	$('#nextPageBtn').click( function() {
		table.nextPage();
	} );
} );
