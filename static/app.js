// scroll to fix header
$(window) .scroll(function(){
    if ($(this).scrollTop() > 135) {
        $('#task_flyout').addClass('fixed');
    } else {
        $('#task_flyout').removeClass('fixed');
    }
});


// drop down change
$(document).ready( function()  {

	// set selected
	var selectedItem = sessionStorage.getItem("SelectedItem");  
   $('.dropdown').val(selectedItem);

   $('.dropdown').change( function() {

   	    var item = $(this).val(); 

   	    // persist selected
   	    sessionStorage.setItem("SelectedItem", item );

   	    path = 'spending/' + item
   	    window.location = window.location.protocol + "//" + window.location.host + "/" + path
   });

   // format amount 
   // $(".amount").each( function() {

   //     var val = $(this);
   //     $(this).text( parseFloat( val.text() ).toFixed(2) ); 
   // })

});