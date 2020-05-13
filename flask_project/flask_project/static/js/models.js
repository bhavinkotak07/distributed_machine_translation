$(document).ready(function() {
    console.log('this is to be executed')
    $.get( "/api/list_models", function( data ) {

        $(data).each(function(index, o) {
            res = `<br>
            <div class="row">
            <div class="col-sm-1" style="font-weight:200;background-color:lavenderblush">${index + 1}</div>
            <div class="col-sm-2" style="font-weight:200;background-color:lavenderblush">${o.from_language}</div>
            <div class="col-sm-2" style="font-weight:200;background-color:lavenderblush">${o.to_language}</div>
            <div class="col-sm-1" style="font-weight:200;background-color:lavenderblush">${o.status}</div>
            
            `
            if(o.status == 'UPLOADED' || o.status == 'STOPPED'){
                res += `<div class="col-sm-1" > <input type="number" id="instances_${o.model}"  min="1" max="5" value=1> </div>`;
                res += `<div class="col-sm-1" > <button type="button" class="btn btn-primary btn-xs" onclick="deploy(this)" id="${o.model}" style="background-color:green">Deploy</button></div>`;
            }
            else{
                res += `<div class="col-sm-1" > <p id="instances_${o.model}" > ${o.instances}</div>`;
                res += `<div class="col-sm-1" > <button type="button" class="btn btn-primary btn-xs" onclick="deploy(this)" id="${o.model}" style="background-color:red">Stop</button></div>`;

            }
           res += `<br></div>`;
        
            $( "#models" ).append( res );
            console.log( index );

            //alert('id: ' + element.id + ', name: ' + element.name);
        });
      });
});


function deploy(btn){
    console.log( $('#'+btn.id).text() );
    console.log(btn.id);
    var deploy_url = "/api/stop";
    var payload = {'button_id':btn.id, 'instances': $('#instances_'+btn.id).val() };
    console.log(payload);
    if($('#'+btn.id).text() == "Deploy"){
        deploy_url = "/api/deploy";

    }
    console.log(deploy_url);
    /*
    $.get( deploy_url, function( data ) {
        console.log(data);
        location.reload()
    });
    */
   $.post( deploy_url,payload).done( function( data ) {
    console.log(data);
    location.reload();
  });
}