function addone(id, data) {
  cl = $('#sample').clone();
  cl.attr('id', id);
  cl.show();
  childs = cl.children().children();
  childs[0].innerHTML = data['name'];
  childs[1].innerHTML = data['counts'];
  childs[2].innerHTML = data['status'];
  childs[3].innerHTML = data['tw1'];
  childs[4].innerHTML = data['tw2'];
  childs[5].innerHTML = data['tw3'];
  if(data['status'] == 'status: active streaming')
    childs[6].innerHTML = '<span onclick="stream(this,0);"><a class="button radius secondary tiny"><i class="fa fa-pause"></i></a></span> <span onclick="unstream(this);"><a class="button radius alert tiny"><i class="fa fa-trash"></i></a></span>';
  else
    childs[6].innerHTML = '<span onclick="stream(this,1);"><a class="button radius success tiny"><i class="fa fa-play"></i></a></span> <span onclick="unstream(this);"><a class="button radius alert tiny"><i class="fa fa-trash"></i></a></span>';

  panel.append(cl);
}

function refresh() {
  $.get('/streamings?'+Math.random(), function (response) {
    panel.empty();
    for (var i = response.length-1; i >= 0; --i) {
      addone('id-'+i, response[i]);
    };
  }, "json");
}

function addkeyword() {
  $('#plus_button').prop({disabled:true});
  $('#content_button').attr('class', 'fa fa-lg fa-spinner fa-spin');
  $.post('/stream', {keyword: $('#keyword').val(), status: 1}, function(response){
    $('#plus_button').prop({disabled:false});
    $('#content_button').attr('class', 'fa fa-lg fa-plus');
    $('#message').text($('#keyword').val()+' has been added to streaming queue successfully');
    $('#keyword').val('');
    refresh();
  }, "json");
  return false;
}

function stream(node, status) {
  $.post('/stream', {keyword: node.parentNode.parentNode.children[0].innerHTML, status: status}, function(response){
    // console.log(response);
    refresh();
  }, "json");
}

function unstream(node) {
  $.post('/unstream', {keyword: node.parentNode.parentNode.children[0].innerHTML}, function(response){
    // console.log(response);
    refresh();
  }, "json");
}

$(function(){
  panel = $('#panel');
  function loop_refresh() {
    refresh();
    setTimeout(loop_refresh, 10000);
  }
  loop_refresh();
});