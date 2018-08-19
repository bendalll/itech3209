
	//Allow content to be draggable and droppable. 
	$( function() 
	{
		$( ".cards" ).draggable();


	} );
	
	//Allow content to be reordered in a list.
	$( function() 
	{
		$( "#sortable" ).sortable();

	});
	
	$( function() 
	{
		$( ".connection" ).sortable(
			{
				connectWith: ".connection",
			});

	});
	
	