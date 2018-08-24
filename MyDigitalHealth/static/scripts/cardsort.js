// Javascript to control the dynamic creation of html Card and Category elements for the Admin Create Package
// and user viewing and completing package activity functionality

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

// Create-package functions
function addCard(parentId)
{
	// Adds a new card to the card list
	let cardList = document.getElementById(parentId);
	let newCard = document.createElement("div");
	newCard.setAttribute("class", "list-group-item");
	let newInput = document.createElement("input");
	newInput.setAttribute("type", "text");
	newInput.setAttribute("class", "form-control");
	newInput.setAttribute("placeholder", "Card text here");
	newInput.setAttribute("name", "card_text");
	let newRemoveButton = document.createElement("button");
	newRemoveButton.setAttribute("onclick", "removeCard(this)");
	newRemoveButton.setAttribute("type", "button");
	newRemoveButton.innerHTML = "Remove This Card";
	newCard.appendChild(newInput);
	newCard.appendChild(newRemoveButton);
	cardList.appendChild(newCard);

	// Add bootstrap container to </div>
    // $(cardList).attr("class","col-sm-7");
}


function removeCard(buttonObject)
{
	//Removes a card from the card list
	let thisCard = buttonObject.parentElement
	thisCard.remove();
}


function addCategory(parentId)
{
	// Add a new category to the category list
	let categoryList = document.getElementById(parentId);
	let newCategory = document.createElement("div");
	newCategory.setAttribute("class", "list-group-item");
	let newInput = document.createElement("input");
	newInput.setAttribute("type", "text");
	newInput.setAttribute("placeholder", "Category");
	newInput.setAttribute("name", "category_name");
	newInput.setAttribute("class", "form-control");
	let newRemoveButton = document.createElement("button");
	newRemoveButton.setAttribute("onclick", "removeCategory(this)");
	newRemoveButton.setAttribute("type", "button");
	newRemoveButton.innerHTML = "Remove This Category";
	newCategory.appendChild(newInput);
	newCategory.appendChild(newRemoveButton);
	categoryList.appendChild(newCategory);
}


function removeCategory(buttonObject) {
	// Remove the category from the category list
	let thisCategory = buttonObject.parentElement;
	thisCategory.remove();
}
