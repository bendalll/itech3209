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


// Global variable card #ID counter - need to find a better way to handle this
var id_num = 10; //start at 10 just in case?

// Create-package functions
function addCard(parentId)
{
	// Adds a new card to the card list
	let cardList = document.getElementById(parentId);
	let newCard = document.createElement("div");
	newCard.setAttribute("class", "card");
	newCard.setAttribute("id", id_num);
	id_num = id_num + 1; //increment the #id count
	let newTextArea = document.createElement("textarea");
	newTextArea.setAttribute("maxlength", "200");
	let newAddButton = document.createElement("button");
	newAddButton.setAttribute("onclick", "addCard('cardList')");
	newAddButton.setAttribute("type", "button");
	newAddButton.innerHTML = "+";
	let newRemoveButton = document.createElement("button");
	newRemoveButton.setAttribute("onclick", "removeCard(this)");
	newRemoveButton.setAttribute("type", "button");
	newRemoveButton.innerHTML = "-";
	newCard.appendChild(newTextArea);
	newCard.appendChild(newAddButton);
	newCard.appendChild(newRemoveButton);
	cardList.appendChild(newCard);
	window.scrollTo(0, cardList.scrollHeight);

	//Add bootstrap container to </div>
    $(cardList).attr("class","col-sm-7");
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
	newCategory.setAttribute("class", "category");
	let newText = document.createElement("p");
	let newLabel = document.createTextNode("Category Name:");
	newText.appendChild(newLabel);
	let newInput = document.createElement("input");
	newInput.setAttribute("type", "text");
	let newAddButton = document.createElement("button");
	newAddButton.setAttribute("onclick", "addCategory('categoryList')");
	newAddButton.setAttribute("type", "button");
	newAddButton.innerHTML = "+";
	let newRemoveButton = document.createElement("button");
	newRemoveButton.setAttribute("onclick", "removeCategory(this)");
	newRemoveButton.setAttribute("type", "button");
	newRemoveButton.innerHTML = "-";
	newCategory.appendChild(newText);
	newCategory.appendChild(newInput);
	newCategory.appendChild(newAddButton);
	newCategory.appendChild(newRemoveButton);
	categoryList.appendChild(newCategory);

	//Add bootstrap container to </div>
    $(categoryList).attr("class","col-sm-5");
}

function removeCategory(buttonObject) {
	// Remove the category from the category list
	let thisCategory = buttonObject.parentElement;
	thisCategory.remove();
}
