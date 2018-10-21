//Allow content to be reordered in a list, drag and droppable
$( function()
{
    $( ".connection" ).sortable(
        {
            connectWith: ".connection"
        });

});

// Function to make Group Headings editable.
function editHeading(element) {

    $(element).parent("li").children("#group-title").attr("contenteditable", "true").focusout(function() {
        $(this).removeAttr("contenteditable").off("focusout");
    });
    $(element).parent("li").children("#group-title").focus();

    processCards();
}


// Function to change the color of the group headings based on the value in the color picker input
function changeHeadingColor()
{
    let new_color = $("#id_main_color").val();
    $(".active").css("background-color", new_color);
    $(".active").css("border-color", new_color);
}



function toggleGroupsInput()
{
    // called when the "let user name groups" checkbox state is changed
    // enables or disables the Groups formset depending on the state of the checkbox
    let checkbox = $('#id_user_defined_groups');
    console.log(document.getElementById('id_user_defined_groups'));
    let status = checkbox.prop("checked");
    let sec_status = checkbox.prop("value");
    console.log(status);
    console.log(sec_status);

    // get each of the text input fields for the group list
    let text_inputs = $('#id_group_list').children().children(':text');

    if(status === true)
    {
        text_inputs.each(function()
        {
            let text = "Click to Name";
            $(this).prop("value", text);
            $(this).prop("readonly", true);
        });
    }
    else
    {
        text_inputs.each(function()
        {
            // $(this).prop("value", null);
            $(this).prop("readonly", false);
        });
    }


}


function cloneItem(type)
{
    /* Clone a card or group from the list and append it to the list after updating
     the name and id values on the clone
    :param: type: indicates whether the item to clone and append is a card or group
    ALSO REQUIRES: that the formset prefix assigned by Django be 'card' or 'group' as expected,
    AND: that the formset is rendered so each form is an </li> within a </ul>,
    AND: that the #id of the </ul> is 'id_card_list' or 'id_group_list' as appropriate
     */
    let parent_list = $('#id_' + type + '_list');
    let item_number = parent_list[0].childElementCount;

    let new_item = $('#id_' + type + '_list li:last').clone(true);

    new_item.find(':text').each(function()
    {
        let name = $(this).attr('name').replace('-' + (item_number-1) + '-','-' + item_number + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });

    new_item.find('input[type=hidden]').each(function()
    {
        let name = $(this).attr('name').replace('-' + (item_number-1) + '-','-' + item_number + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id});
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

    parent_list.append(new_item);

    toggleGroupsInput();
}


function removeGroup(group_element)
{
    let parent_list = $('#id_group_list');
    let item_number = parent_list[0].childElementCount;

    //Ensure we don't remove the last item in the list.
    if ( item_number > 1) {
        // Remove the group from the group list
        let group_li = group_element.parentElement;
        $(group_li).remove();

        let li_list = parent_list[0].children

        // Refresh the IDs and Names for the items in the LIs so the form validation doesn't break.
        for (i = 0; i < (item_number-1) ;i++) {

            let group_input = li_list[i].children[0]
            let group_hidden = li_list[i].children[1]
            group_input.id = "id_group-"+i+"-title"
            group_input.name = "group-"+i+"-title"
            group_hidden.id = "id_group-"+i+"-id"
            group_hidden.name = "group-"+i+"-id"

        }

        // Decrement the total number of forms on the page so correct number of forms will be submitted
        let id_total_forms = '#id_group-TOTAL_FORMS';
        let total = $(id_total_forms).val();
        total--;
        $(id_total_forms).val(total);
    }
}


function removeCard(card_element)
{
    let parent_list = $('#id_card_list');
    let item_number = parent_list[0].childElementCount;

    //Ensure we don't remove the last item in the list.
    if ( item_number > 1) {
        // Remove the group from the group list
        let card_li = card_element.parentElement;
        $(card_li).remove();

        let li_list = parent_list[0].children

        // Refresh the IDs and Names for the items in the LIs so the form validation doesn't break.
        for (i = 0; i < (item_number-1) ;i++) {

            let card_input = li_list[i].children[0]
            let card_hidden = li_list[i].children[1]
            card_input.id = "id_card-"+i+"-text"
            card_input.name = "card-"+i+"-text"
            card_hidden.id = "id_card-"+i+"-id"
            card_hidden.name = "card-"+i+"-id"

        }


        // Decrement the total number of forms on the page so correct number of forms will be submitted
        let id_total_forms = '#id_card-TOTAL_FORMS';
        let total = $(id_total_forms).val();
        total--;
        $(id_total_forms).val(total);
     }

}


// Function runs on form submit and collects positions of cards
// Puts them in hidden input field per group
// Submits
function processCards()
{
    // !For each </ul> get .contents() and add card #id to ul.input!
    // Get parent items for cards by class (.connection)
    let ULists = $(".connection");

    for(i=0; i<ULists.length; i++)
    {
        let hiddenInput = ULists[i].getElementsByTagName("input")[0];   // Only ever going to be one hidden input at this point
        hiddenInput.value = "";
        let list_items = ULists[i].getElementsByClassName("list-group-item"); // Filter by class here because tag name doesn't work (don't know why)
        for(j=0; j<list_items.length; j++)
        {
            hiddenInput.value += (list_items[j].getAttribute("id") + ",");
        }
    }

    // Process Group Names and update hidden fields appropriately.
    let groups = $("span#group-title");

    for(i=0; i<groups.length; i++)
    {
        groupContainer = $(groups[i]).parent()[0];
        groupTitle = $(groups[i]).text();   //Retrieve the current text from the span
        hiddenInput = groupContainer.getElementsByTagName("input")[0];  // If we do this via Jquery objects it reports success, but doesn't work!
        hiddenInput.value = groupTitle;
    }
}