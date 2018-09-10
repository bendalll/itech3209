
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
		$(".connection").sortable(
			{
				connectWith: ".connection",
				update: function(event, ui)
				{
					var result = $(this).sortable('toArray', {attribute: 'value'});
					var test = $(".connection").sortable('toArray', {attribute: 'value'});
					//List Cards from Card Package into Array.
					var cardsText = [];
					$("#sortable li").each(function()
					{ 
						cardsText.push($(this).text()) 
					});
					//var cardString = cardsText.join(' ');

					document.getElementById("cardsList").value = cardsText;
					
					
					var length = $(".cardGroups").length

					
					var numberOfGroups = $(".cardGroups");
					
					
					$(numberOfGroups).each(function(i)
					{
						var optionTexts = [];
						optionTexts.push($(this).text()) 
						var cardString = optionTexts.map(str => str.trim());
						//console.log(Array.isArray(optionTexts));
						//document.getElementById("pe" + (i + 1)).innerHTML = cardString;
						document.getElementById('sortedCards' + (i + 1)).value = cardString;
					});
				}
			});

	});
	
	$( function() 
	{
		$(document).ready(function() 
		{
			$(".cardGroups").each(function(i) 
			{
				$(this).attr('id', "cardGroups" + (i + 1));
						
				//delete
				//var createInputHeading = document.createElement('p');
				//$(createInputHeading).attr("id", "pe" + (i + 1));
				//$("#forming").append(createInputHeading);

				var sortedCards = document.createElement('input');
				$(sortedCards).attr("id", "sortedCards" + (i + 1));
				$(sortedCards).attr("name", "sortedCards");
				$(sortedCards).attr("type","hidden");
				$("#submitForm").append(sortedCards);
				
			})
		})
	});
	
	