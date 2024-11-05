if (typeof jQuery === 'undefined') {
  throw new Error('AdminLTE requires jQuery');
}
let is_reload = 0;
let ajax_btn_delete = function (myself) {
  let $this = $(myself);
  let origin_html = '';
  let url = $this.data('href');
  $.ajax({
    type: 'GET',
    url: url,
    processData: false,
    contentType: false,
    // async: false,
    cache: false,
    beforeSend: function () {
      origin_html = $this.html();
      $this.html('<i class="spinner-border spinner-border" role="status" aria-hidden="true"></i> | Deleting ...');
      is_reload = 1;
    },
    success: function (data) {
      if (is_reload > 0) {
        $this.html(origin_html);
        location.reload();
      }
    },
    error: function (data) {
    }
  });
}
let ajax_load_event = function (myself) {
  let $this = $(myself);
  let origin_html = '';
  let url = $this.data('href');
  $.ajax({
    type: 'GET',
    url: url,
    processData: true,
    contentType: false,
    async: true,
    cache: false,
    beforeSend: function () {
      origin_html = $this.html();
      $this.html('<i class="spinner-border spinner-border" role="status" aria-hidden="true"></i> | loading ...');
    },
    success: function (data) {
      $this.html(data);
    },
    error: function (data) {
    }
  });
}

let ajax_submit_form = function (e, myself) {
  e.preventDefault();
  let frm = $('#admin_form');
  let form_data = new FormData(frm[0]);
  $.ajax({
    type: 'POST',
    url: frm.attr('action'),
    processData: false,
    contentType: false,
    async: false,
    cache: false,
    data: form_data,
    beforeSend: function () {
      $(myself).button('loading');
      frm.find('input, textarea, select').prop('disabled', true);
    },
    success: function (result, status, xhr) {
      frm.find('input, textarea, select').prop('disabled', false);
      $(myself).button('reset');
      if (xhr.status === 200) {
        location.reload();
      }
    },
    error: function (data) {
      frm.find('input, textarea, select').prop('disabled', false);
      $(myself).button('reset');
    }
  });

  return false;
}
