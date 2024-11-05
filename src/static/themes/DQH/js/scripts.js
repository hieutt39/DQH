/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

  // Navbar shrink function
  var navbarShrink = function () {
    const navbarCollapsible = document.body.querySelector('#mainNav');
    if (!navbarCollapsible) {
      return;
    }
    if (window.scrollY === 0) {
      navbarCollapsible.classList.remove('navbar-shrink')
    } else {
      navbarCollapsible.classList.add('navbar-shrink')
    }

  };

  // Shrink the navbar
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink);

  //  Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector('#mainNav');
  if (mainNav) {
    new bootstrap.ScrollSpy(document.body, {
      target: '#mainNav',
      rootMargin: '0px 0px -40%',
    });
  }
  ;

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector('.navbar-toggler');
  const responsiveNavItems = [].slice.call(
      document.querySelectorAll('#navbarResponsive .nav-link')
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener('click', () => {
      if (window.getComputedStyle(navbarToggler).display !== 'none') {
        navbarToggler.click();
      }
    });
  });
});



let meg_html_bot = '\
    <div class="d-flex justify-content-between">\
        <p class="small mb-1">DQH Bot</p>\
        <p class="small mb-1 text-muted">{{datetime}}</p>\
    </div>\
    <div class="d-flex flex-row justify-content-start">\
        <img src="assets/doopage.png"\
             alt="avatar 1" style="width: 45px; height: 100%;">\
        <div>\
            <p class="small p-2 ms-3 mb-3 rounded-3 bg-body-tertiary">{{content}}</p>\
        </div>\
    </div>';

let msg_html = '\
    <div class="d-flex justify-content-between">\
        <p class="small mb-1 text-muted">{{datetime}}</p>\
        <p class="small mb-1">{{name}}</p>\
    </div>\
    <div class="d-flex flex-row justify-content-end mb-4 pt-1">\
        <div>\
            <p class="small p-2 me-3 mb-3 text-white rounded-3 bg-warning">{{content}}</p>\
        </div>\
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"\
             alt="avatar 1" style="width: 45px; height: 100%;">\
    </div>';

let botReceiver = function () {
  let textArray = [
    'Xin lỗi, tôi đang trong giai đoạn phát triển sẽ trả lời bạn sớm!',
    'Xin lỗi, tôi chưa thể trả lời bạn ngay lúc này.',
    'Xin lỗi, hệ thống đang trong giai đoạn phát triển.'
  ];
  let randomNumber = Math.floor(Math.random()*textArray.length);
  let now = new Date();
  let now_str = now.getUTCFullYear().toString() + "/" +
          (now.getUTCMonth() + 1).toString() +
          "/" + now.getUTCDate() + " " + now.getUTCHours() +
          ":" + now.getUTCMinutes() + ":" + now.getUTCSeconds();
  let msg_html_get = meg_html_bot.replace('{{content}}', textArray[randomNumber]).replace('{{datetime}}', now_str);
  msg_html_get = msg_html_get.replace('{{name}}', 'Anonymous');
  setTimeout(
      function() {
        $('#rcw-conversation-container').find('.card-body').append(msg_html_get);
      },
      1000
  )
}
let sendMsg = function (e, self) {
  e.preventDefault();
  let $this = $(self);
  let origin_html = '';
  let url = $this.data('href');
  let input_obj = $('#rcw-conversation-input')
  let input_msg = input_obj.val();
  const now = new Date();
  let now_str = now.getUTCFullYear().toString() + "/" +
          (now.getUTCMonth() + 1).toString() +
          "/" + now.getUTCDate() + " " + now.getUTCHours() +
          ":" + now.getUTCMinutes() + ":" + now.getUTCSeconds();
  let msg_html_send = msg_html.replace('{{content}}', input_msg).replace('{{datetime}}', now_str);
  msg_html_send = msg_html_send.replace('{{name}}', 'Anonymous');
  if (input_msg.length > 0) {
    $.ajax({
      type: 'GET',
      url: url,
      processData: false,
      contentType: false,
      // async: false,
      cache: false,
      beforeSend: function () {
        origin_html = $this.html();
        $this.html('...');
      },
      success: function (data) {
        $this.html(origin_html);
        // let jsonObj = JSON.parse(data);
        input_obj.val('');
        $('#rcw-conversation-container').find('.card-body').append(msg_html_send);
        botReceiver();
        console.log(msg_html)
        let jsonPretty = JSON.stringify(data, null, '\t');
      },
      error: function (data) {

      }
    });
  }
}

$(function () {
  $('[aria-controls="rcw-chat-container"]').on('click', function (e) {
    if ($('.rcw-conversation-container').hasClass('active')) {
      $('.rcw-conversation-container').removeClass('active')
    } else {
      $('.rcw-conversation-container').addClass('active')
    }
    e.preventDefault()
  });
});


