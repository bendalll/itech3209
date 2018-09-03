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


// Global variables to count numbers of cards and categories
// Initially the form consists of 4 cards and 2 categories
var num_cards = 4;
var num_categories = 2;


// Create-package functions
function cloneItem(type)
{
    /* Clone a card or category from the list and append it to the list after updating
     the name and id values on the clone
    :param: type: indicates whether the item to clone and append is a card or category
    ALSO REQUIRES: that the formset prefix assigned by Django be 'card' or 'category' as expected,
    AND: that the formset is rendered so each form is an </li> within a </ul>,
    AND: that the #id of the </ul> is 'id_card_list' or 'id_category_list' as appropriate
     */
    let item_number = 0; // currently used so later code will fail gracefully if param is somehow incorrect
    if(type === 'card') {
        item_number = num_cards;
        num_cards += 1;
    }
    else if (type === 'category') {
        item_number = num_categories;
        num_categories += 1;
    }

    let new_item = $('#id_' + type + '_list li:last').clone(true);
    new_item.find(':input').each(function()
    {
        let name = $(this).attr('name').replace('-' + (item_number-1) + '-','-' + item_number + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    new_item.find('label').each(function()
    {
        let newFor = $(this).attr('for').replace('-' + (item_number-1) + '-','-' + item_number + '-');
        $(this).attr('for', newFor);
    });

    // Increment the total number of forms on the page so all forms will be submitted
    let id_total_forms = '#id_' + type + '-TOTAL_FORMS';
    let total = $(id_total_forms).val();
    total++;
    $(id_total_forms).val(total);

    $('#id_' + type + "_list").append(new_item);
}


function removeCategory(category_id)
{
	// Remove the category from the category list
    // TODO
}


function removeCard(card_id)
{
	//Removes a card from the card list
	// TODO
}