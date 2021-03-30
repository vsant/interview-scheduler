$(document).ready(function() {
  $('#txt').focus()
  
  $('#btn').click(function () {
    var t = $("#txt").val();
    $.ajax({
      type: "POST",
      url: "scheduler.php",
      data: { txt: t },
      success: function(data) {
        $('#calendar').remove();
        $('#divbody').append("<div id='calendar'></div>");
        cal_data = $.trim(data.split("|")[0]);
        def_date = $.trim(data.split("|")[1]);
        nomatches = data.split("|").slice(2).filter(function(e){return (e!="\n")});
        $('#calendar').fullCalendar({
          defaultDate: def_date,
          editable: true,
          events: eval(cal_data)
        });
        $('#nomatch').remove();
        if (nomatches.length != 0) {
          $('#calendar').before("<div id='nomatch'>Not scheduled (too many conflicts): <b>" + nomatches.join(', ') + "</b></div></center>");
        }
      }
    })
  });

  $.ajax({
    url: "prog-dates.txt",
    success: function(data) {
      $('#txt').val(data);
      $('#btn').click();
    }
  })
});
