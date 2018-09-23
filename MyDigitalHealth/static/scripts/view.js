
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
                    //List Cards from Card Package into Array.
                    var cardsText = [];
                    $("#sortable li").each(function()
                    {
                        cardsText.push($(this).val())
                    });
                    //var cardString = cardsText.join(' ');

                    document.getElementById("cardsList").value = cardsText;

                    $(".cardGroups").each(function(i)
                    {
                        var test = $(this).val()
                        var sortedCard = [];

                        $(this).find("li").each(function()
                        {
                            sortedCard.push($(this).val())
                        });
                        document.getElementById('sortedCards' + (i + 1)).value = [sortedCard];
                    });

                    $(".sortedCardGroups").each(function(i)
                    {
                        var test = $(this).val()
                        var sortedCardList = [];

                        $(this).find("li").each(function()
                        {
                            sortedCardList.push($(this).val())
                        });
                        document.getElementById('sortedCardList' + (i + 1)).value = [sortedCardList];
                    });
                }
            });

    });

    $( function()
    {
        $(document).ready(function()
        {
            $("#cardGroupsDiv .cardGroups").each(function(i)
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
                $(submitForm).append(sortedCards);

            });

            $(".sortedCardGroups").each(function(i)
            {
                $(this).attr('id', "sortedCardGroups" + (i + 1));

                //delete
                //var createInputHeading = document.createElement('p');
                //$(createInputHeading).attr("id", "pe" + (i + 1));
                //$("#forming").append(createInputHeading);

                var sortedCardList = document.createElement('input');
                $(sortedCardList).attr("id", "sortedCardList" + (i + 1));
                $(sortedCardList).attr("name", "sortedCardList");
                $(sortedCardList).attr("type","hidden");
                $(submitForm).append(sortedCardList);

            });

            var sortedCardGroup = $('#cardGroupsDiv');
            var sortedCardGroupsList = sortedCardGroup.children('.cards').get();
            sortedCardGroupsList.sort(function(a, b)
            {
                return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
            })
        })
    });

