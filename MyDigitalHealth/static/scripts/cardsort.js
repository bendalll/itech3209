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


// global variable to count numbers of cards and categories
// initially 4 cards and 2 categories are rendered with the form
var num_cards = 4;
var num_categories = 2;


// Create-package functions
function addCard(parent_id)
{
	// Adds a new card to the card list
    // :param: parent_id: the id of the <div> to add new card to
	let card_list = document.getElementById(parent_id);
	let new_card = document.createElement("input");
	new_card.setAttribute("type", "text");
	new_card.setAttribute("maxlength", "200");

	// increment global num_cards and append to new card id
    num_cards += 1;
    new_card.setAttribute("name", "form-" + num_cards + "-card_text");
	new_card.setAttribute("id", "id_form-" + num_cards + "-card_text");

	//create a new label for the new card and append both to div
    let new_label = document.createElement("label");
    new_label.setAttribute("for", "id_card_text_" + num_cards);
    new_label.innerHTML = "Card text:";
    card_list.appendChild(new_label);
    card_list.appendChild(new_card);
}


function removeCard(card_id)
{
	//Removes a card from the card list
	// TODO
}


function addCategory(parent_id)
{
	// Add a new category to the category list
    // :param: parent_id: the id of the <div> to add new category to
	let category_list = document.getElementById(parent_id);
	let new_category = document.createElement("input");
	new_category.setAttribute("type", "text");
	new_category.setAttribute("maxlength", "200");

	// increment the global num_categories and append to new category id
    num_categories += 1;
    new_category.setAttribute("name", "form-" + num_categories + "-category_name");
    new_category.setAttribute("id", "id_form-" + num_categories + "-category_name");

    let new_label = document.createElement("label");
    new_label.setAttribute("for", "id_form-" + num_categories + "-category_name");
    new_label.innerHTML = "Category name:";
    category_list.appendChild(new_label);
    category_list.appendChild(new_category);
}


function removeCategory(category_id)
{
	// Remove the category from the category list
    // TODO
}
