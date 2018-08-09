
	//Allow content to be draggable and droppable. 
	$( function() 
	{
		$( ".cards" ).draggable();


	} );
	
	//Allow content to be reordered in a list.
	$( function() 
	{
		$( ".connection" ).sortable(
			{
				connectWith: ".connection"
			});

	});
	
	//Create Cards on Screen
	function appendCard()
	{
		//Find all Input values from the form and put them into an array
		var groupInputValues = $("#groupForm").find('.form-control').map(function() 
		{
			//Remove whitespace from both sides of string
			return $(this).val().trim();
		}).toArray();
		
		for(i=0;i<groupInputValues.length;i++)
		{
			//Find value of each form input
			groupText = groupInputValues[i];
			//Ignore empty inputs
			if(groupText != "")
			{
				//Create </div> for Group Headings
				var tableDiv = document.createElement('div');
				//Add class attributes to </div>
				$(tableDiv).attr("class","cards");
				//Allow content to be draggable and droppable. 
				$(tableDiv).draggable();
				//Create </ul> for Group Headings
				var createUl = document.createElement('ul');
				//Add class attributes to </ul>
				$(createUl).attr("class","list-group");
				//Create </input> for Group Headings
				var createInputHeading = document.createElement('input');
				//Add attributes to </input>
				$(createInputHeading).attr("type","hidden");
				$(createInputHeading).attr("name","title");
				$(createInputHeading).attr("value",groupText);
				//Create </li> for Group Headings
				var createLiHeading = document.createElement('li');
				//Add class attributes to </li>
				$(createLiHeading).attr("class","list-group-item active").text(groupText);
				//Create </li> to allow sorting between Group Headings
				var createLi = document.createElement('li');
				//Add class attributes to </li>
				$(createLi).attr("class","connection");
				//Allow content to be reordered in a list.
				$(createLi).sortable(
				{
					connectWith: ".connection"
				});
				$(createLi).append(createInputHeading);
				//Append elements to </ul>
				$(createUl).append(createLiHeading, createLi);
				//Append elements to </div>
				$(tableDiv).append(createUl);
				//Append elements to page
				$("#listOfCards").append(tableDiv);
				document.getElementById("cardPackageName").value = document.getElementById("nameOfCardPackage").value;
			}
		}
	
		//Find all Input values from the form and put them into an array
		var cardInputValues = $("#cardForm").find('.form-control').map(function() 
		{
			//Remove whitespace from both sides of string
			return $(this).val().trim();
		}).toArray();
		
		//Create cards with input from the form
		for(i=0;i<cardInputValues.length;i++)
		{
			//Find value of each form input
			cardText = cardInputValues[i];
			//Ignore empty inputs
			if(cardText != "")
			{
				//Append form input into a list
				//Create </input> for Group Headings
				var createCardText = document.createElement('input');
				//Add attributes to </input>
				$(createCardText).attr("type","hidden");
				$(createCardText).attr("name","text");
				$(createCardText).attr("value",cardText);
				//Create </li> for Cards
				var cardLi = document.createElement('li');
				//Add class attributes to </li>
				$(cardLi).attr("class","list-group-item").text(cardText);
				$(cardLi).append(createCardText);
				$("#sortable").append(cardLi);
			}
		}
		$("#cards").show();
	};
	
	//Determine the number of Groups and Cards
	$( function()
	{
		$("#createElements").click(function()
		{
			//Number of Groups to Create
			var numberOfGroups = $("#numberOfGroups").val().trim();
			//Number of Cards to Create
			var numberOfCards = $("#numberOfCards").val().trim();
			
			//Create form for Group Headings
			var groupForm = document.createElement('form');
			//Create form for Cards
			var cardForm = document.createElement('form');
			
			//Create new </div> for Group Headings
			var group = document.createElement('div');
			//Add bootstrap container to </div>
			$(group).attr("class","col-sm-5");
			$(group).attr("id","groupForm");
			//Create new </div> for Cards
			var card = document.createElement('div');
			//Add bootstrap container to </div>
			$(card).attr("class","col-sm-7");
			$(card).attr("id","cardForm");
		
			//Create Group Headings
			for(i=0;i<numberOfGroups;i++)
			{
				//Ignore empty inputs
				if(numberOfGroups != "" && numberOfCards != "")
				{
					//Create new </div> for Group Headings
					var groupDiv = document.createElement('div');
					//Add class and id attributes to </div>
					$(groupDiv).attr("class","form-group");
					$(groupDiv).attr("id","group" + (i + 1));
					//Create label attributes 
					groupLabel = $("<label></label>");
					$(groupLabel).attr("class","fb-text-label").text("Group " + (i + 1) + " Heading");
					//Create input attributes 
					groupInput = $("<input></input>");
					$(groupInput).attr("class","form-control");	
					groupInput.type = "text";
					//Add label and input attributes to </div>
					$(groupDiv).append(groupLabel, groupInput);
					//Add </div> to webpage
					$(groupForm).append(groupDiv);
				}
			}
			//Create Cards
			for(j=0;j<numberOfCards; j++)
			{
				//Ignore empty inputs
				if(numberOfGroups != "" && numberOfCards != "")
				{
					//Create new </div> for Cards
					var cardDiv = document.createElement('div');
					//Add class and id attributes to </div>
					$(cardDiv).attr("class","form-group");
					$(cardDiv).attr("id","card" + (j + 1));
					//Create label attributes 
					cardLabel = $("<label></label>");
					$(cardLabel).attr("class","fb-text-label").text("Card " + (j + 1));
					//Create input attributes 
					cardInput = $("<input></input>");
					$(cardInput).attr("class","form-control");	
					cardInput.type = "text";
					//Add label and input attributes to </div>
					$(cardDiv).append(cardLabel, cardInput);
					//Add </div> to webpage
					$(cardForm).append(cardDiv);
				}
			}
			//Hide Initial Form and Create button if input valid
			if(numberOfGroups != "" && numberOfCards != "")
			{
				//Hide inital creation form 
				$("#create").hide();
				//Hide inital buttons 
				$("#createElements").hide();
			
				//Create button to Create Group Headings and Cards
				var createButton = document.createElement('button');
				//Add id, type and onclick attributes to </div>
				$(createButton).attr("id","createCards").text("Make");
				createButton.type = "button";
				$(createButton).attr("onclick","appendCard()");
							
				//Create new </div> for Cards
				var buttonDiv = document.createElement('div');
				//Add class and id attributes to </div>
				$(buttonDiv).attr("class","btn-group");
				//Append buttons to </div>
				$(buttonDiv).append(createButton);
				
			}
			//Append form for Group Headings to Group Headings </div>
			$(group).append(groupForm);
			//Append form for Card  to Cards </div>
			$(card).append(cardForm);
			//Append Group Headings </div> and Card </div> to pageRows </div>
			$("#pageRows").append(group, card);
			$("#buttons").append(buttonDiv);
		});
	});
