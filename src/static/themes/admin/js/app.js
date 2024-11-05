// let is_reload = 0
let modal_html = '\
    <!-- model container -->\
    <div class="modal-dialog" style="width: 90%;">\
        <div class="modal-content">\
            <div class="modal-header">\
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>\
                <h4 class="modal-title">&nbsp;</h4>\
            </div>\
            <div class="modal-body">\
                <div class="overlay">\
                    <i class="fa fa-refresh fa-spin"></i>\
                </div>\
            </div>\
        </div>\
    </div>';


$(function () {
    $("#modal_lg").on("show.bs.modal", function (e) {
        $(this).html(modal_html);
        let link = $(e.relatedTarget);
        $(this).load(link.attr("href"));
        // $(this).css('z-index', zIndex++);
    });
    $('#modal_lg').on('hidden.bs.modal', function () {
        if (is_reload > 0) {
            location.reload();
        }
    });
});
let ajax_post_upload = function (e, self) {
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
            $(self).button('loading');
            frm.find('input, textarea, select').prop('disabled', true);
        },
        success: function (result, status, xhr) {
            frm.find('input, textarea, select').prop('disabled', false);
            $(self).button('reset');
            if (xhr.status === 200) {
                // location.reload();
                window.location.href=frm.attr('redirect')
            }
        },
        error: function (data) {
            frm.find('input, textarea, select').prop('disabled', false);
            $(self).button('reset');
        }
    });
}

let confirm_delete = function (myself, e, mess) {
    e.preventDefault();
    alertify.confirm(mess, function (c) {
        if (c) location.assign(myself.attributes['href'].value);
    });
    return false;
}
let add_more_row = function (elm_id) {
    let elm_body = $(".box-body" + elm_id).first()
    let source = elm_body.find('.row:last');
    let clone = source.clone()
    clone.find('input, textarea, select').each(function () {
        $(this).val('');
    });
    clone.find('.hidden').removeClass('hidden');
    elm_body.append(clone);
}
let remove_row = function (elm_id) {
    $(elm_id).parent().parent().parent().remove();
}
let ajax_load = function (myself) {
    $.ajax({
        type: 'GET',
        url: $(myself).data('url'),
        beforeSend: function () {
            $(myself).html('Loading...');
        },
        success: function (data) {
            $(myself).html(data);
        },
        error: function (data) {
        }
    });
}

let ajax_post = function (elm, elm_form) {
    let frm = $(elm_form);
    let form_data = new FormData(frm[0]);
    $.ajax({
        type: 'POST',
        url: frm.attr('action'),
        processData: false,
        contentType: false,
        // async: false,
        cache: false,
        data: form_data,
        beforeSend: function () {
            $(elm).button('loading');
            $(elm).attr("disabled", true);
            $('#results').html("");
        },
        success: function (data) {
            $(elm).button('reset');
            $(elm).attr("disabled", false);
        },
        error: function (data) {
            $(elm).button('reset');
            $(elm).attr("disabled", false);
            console.log(data)
        }
    });
}

let ajax_btn_run = function (e, self) {
    e.preventDefault();
    let $this = $(self);
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
            $this.html('<i class="spinner-grow" role="status" aria-hidden="true"></i> | Running ...');
        },
        success: function (data) {
            $this.html(origin_html);
            // let jsonObj = JSON.parse(data);
            let jsonPretty = JSON.stringify(data, null, '\t');
            $('#test_run').html("<pre>"+ jsonPretty + "</pre>");
        },
        error: function (data) {
        }
    });
}