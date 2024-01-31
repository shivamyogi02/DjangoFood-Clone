$(document).ready(function(){
$.getJSON('/fetchallfoodtypes', function(data){
data.map((item)=>{

    $('#foodtype').append($('<option>').text(item.foodtype).val(item.foodtypeid))
})
})

$('#foodtype').change(function(){
    $.getJSON('/fetchallfooditems', {"foodtypeid": $('#foodtype').val()},function(data){
        $('#fooditem').empty()
        $('#fooditem').append($('<option>').text("-Select Food-"))
        data.map((item)=>{

            $('#fooditem').append($('<option>').text(item.fooditem).val(item.fooditemid))
        })           
        })
    })
})
   