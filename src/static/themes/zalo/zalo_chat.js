mQuery = $;
var ZaloChat = {
    base_url: '',
    base_url_socket: '',
    list_api_url: {},
    protocol: '',
    protocalSocket: '',
    domain: '',
    socket: null,
    user_id: '',
    user_current: {},
    is_information_user: true
    ,
    tmp_direct_msg:
        "<div class=\"section-item {position}\">\n" +
        "    <div class=\"avatar\">\n" +
        "        <span class=\"avatar-img\" style=\"background-image: url('{from_avatar}');\"></span>\n" +
        "    </div>\n" +
        "    <div class=\"item-content\">\n" +
        "        <div class=\"item-headline-container\">\n" +
        "            <div class=\"item-headline\">{name}</div>\n" +
        "            <div class=\"snippet\">\n" +
        "                <div class=\"item-message\"><span class=\"Linkify\"><span>{message}</span></span>\n" +
        "                    <div class=\"section-ts\"><span>{time}</span></div>\n" +
        "                </div>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>"
    ,
    tmp_list_user:
        "<div class=\"item-message {active}\" id='{uid}' data-uid='{uid}' onclick=\"ZaloChat.start('{uid}')\">\n" +
        "    <div class=\"avatar\">\n" +
        "       <span class=\"avatar-img\" style=\"background-image: url('{avatar}');\"></span>\n" +
        "    </div>\n" +
        "    <div class=\"snippet\">\n" +
        "       <div class=\"item-title\">\n" +
        "           <span>{name}</span>\n" +
        "       </div>\n" +
        "       <div class=\"item-content\">\n" +
        "           <i class='fa'></i>\n" +
        "           <span></span>\n" +
        "       </div>\n" +
        "       <div class=\"item-tags\"></div>" +
        "    </div>\n" +
        "    <div class=\"item-timestamp\">{time}</div>\n" +
        "</div>"
    ,
    tmp_user_header:
        "<div class=\"avatar\">\n" +
        "    <span class=\"avatar-img\" style=\"background-image: url('{avatar}')\"></span>\n" +
        "</div>\n" +
        "<div class=\"snippet\">\n" +
        "    <div class=\"item-title nickname\"><span>{name}</span></div>\n" +
        "</div>\n" +
        "<div class=\"user-infor\">\n" +
        "    <i class=\"fa fa-info-circle fa-lg\" id=\"btn_user_infor\"></i>\n" +
        "</div>"
    ,
    tmp_information_current_user:
        "<div class=\"sidebar-infor-user\">\n" +
        "    <div class=\"sidebar-container\">\n" +
        "        <div class=\"heading\">Thông tin cá nhân</div>\n" +
        "        <div class=\"sidebar-setting\">\n" +
        "            <div class=\"avatar avatar-side\">\n" +
        "                <span class=\"avatar-side-img\" style=\"background-image: url('{avatar}')\"></span>\n" +
        "            </div>\n" +
        "            <div class=\"buddy-name\">\n" +
        "                <span>{display_name}</span>\n" +
        "            </div>\n" +
        "            <div class=\"buddy-info\">\n" +
        "                <i class=\"fa fa-venus-mars fa-2x\"></i>\n" +
        "                <span>{user_gender}</span>\n" +
        "            </div>\n" +
        "            <div class=\"buddy-info\">\n" +
        "                <i class=\"fa fa-birthday-cake fa-2x\"></i>\n" +
        "                <span>{birth_date}</span>\n" +
        "            </div>\n" +
        "        </div>\n" +
        "        <div class=\"sidebar-detail\">\n" +
        "            <a href='#' class='btn btn-default btn-sm'>Xem thông tin chi tiết</a>\n" +
        "        </div>\n" +
        "    </div>\n" +
        "</div>"
    ,

    init: function (fullDomain, listApiUrl) {
        $this = this;
        $this.list_api_url = listApiUrl;

        $this.pre_processing(fullDomain);
        $this.render_list_user();

        mQuery('.btn-send').click(function (e) {
            $this.post_message(e);
        });
        mQuery('#message_send').bind('keypress', function (e) {
            if (e.keyCode == 13) {
                $this.post_message(e);
            }
        });

        mQuery('#btn_search_follower').click(function (e) {
            $this.search_followers(e);
        });
        mQuery('#txt_search_follower').keyup(function (e) {
            $this.search_followers(e);
        });
    },
    start: function (uid) {
        $this = this;
        if (uid.length > 0) {
            mQuery('.content .context-welcome-slider').addClass('hide');
            mQuery('.content .content-conversation').removeClass('hide');
            mQuery('.list-item>.item-message').each(function (index, value) {
                if (mQuery(value).data('uid') == uid) {
                    mQuery(value).addClass('active');
                    mQuery('#' + uid + ' .snippet').removeClass('font-weight-bold');
                } else {
                    mQuery(value).removeClass('active');
                }
            });

            $this.user_id = uid;
            $this.render_user_header();
            $this.get_conversation_first();
            $this.listen_message_from_socket();

        }
    },
    pre_processing: function (fullDomain) {
        $this = this;
        var splitFullDomain = fullDomain.split("://");
        $this.protocol = splitFullDomain[0];
        $this.domain = splitFullDomain[1];
        if ($this.protocol == 'http') {
            $this.protocalSocket = 'ws';
        } else if ($this.protocol == 'https') {
            $this.protocalSocket = 'wss';
        }

        $this.base_url = $this.protocol + '://' + $this.domain;
        $this.base_url_socket = $this.protocalSocket + '://' + $this.domain;
    },
    render_list_user: function () {
        $this = this;
        var endPoint = $this.base_url + $this.list_api_url['get_followers'];

        mQuery.ajax({
            type: 'GET',
            url: endPoint,
            contentType: 'json',
            async: true,
            cache: false,
            data: {'user_id': $this.user_id, 'offset': 0, 'count': 10},
            beforeSend: function (xhr) {
            },
            success: function (result, status, xhr) {
                mQuery('.list-item').empty();
                result.data.followers.forEach(function (element) {
                    var clone_templete = $this.tmp_list_user;
                    if ($this.user_id == element.user_id) {
                        clone_templete = clone_templete.replace('{active}', 'active');
                    }
                    clone_templete = clone_templete.replaceAll('{uid}', element.user_id);
                    clone_templete = clone_templete.replace('{avatar}', element.avatar);
                    clone_templete = clone_templete.replace('{name}', element.display_name);
                    clone_templete = clone_templete.replace('{time}', "");
                    mQuery('.list-item').append(clone_templete);
                });
            },
            error: function (data) {

            }
        });
    },
    render_user_header: function () {
        $this = this;
        var endPoint = $this.base_url + $this.list_api_url['get_profile'];
        mQuery.ajax({
            type: 'GET',
            url: endPoint,
            contentType: 'json',
            async: true,
            cache: false,
            data: {'user_id': $this.user_id},
            beforeSend: function (xhr) {
            },
            success: function (result, status, xhr) {
                var clone_templete = $this.tmp_user_header;
                clone_templete = clone_templete.replace('{avatar}', result.avatar);
                clone_templete = clone_templete.replace('{name}', result.display_name);
                $this.user_current = result;
                mQuery('.user-current').html(clone_templete);

                $this.is_information_user = true;
                $this.get_information_follow();
                mQuery('#btn_user_infor').click(function (e) {
                    $this.display_information_follow(e);
                });
            },
            error: function (xhr) {
                console.log('Error', xhr.statusText);
                console.log(endPoint);
            }
        });
    },
    render_elements: function (message, type) {
        $this = this;
        var event_name = message.event_name;
        message.data.forEach(function (element) {
            if (event_name == 'user_follow') {

            } else if (event_name == 'user_unfollow') {

            } else {
                $this.render_message_of_conversation(element, type);
            }
        });
    },
    render_message_of_conversation: function (element, type) {
        $this = this;
        var direct_msg_c = $this.tmp_direct_msg;
        var position = '';
        var message = '';
        var message_reply = '';
        console.log(element.type);
        if (element.type == 'text') {
            message = element.message;
            message_reply = element.message;
        } else if (element.type == 'photo') {
            message = '<img class="message-img" src="' + element.thumb + '"/>';
            message_reply = '[Photo]';
        } else if (element.type == 'image') {
            message = '<img class="message-img" src="' + element.thumb + '"/>';
            message_reply = '[Image]';
        } else if (element.type == 'sticker') {
            message = '<img class="message-sticker" src="' + element.url + '"/>';
            message_reply = '[Sticker]'
        } else if (element.type == 'location') {
            message = '<img src="' + element.url + '"/>';
            message_reply = '[Location]';
        }

        if (element.src == 0) {
            position = 'me';
        }

        direct_msg_c = direct_msg_c.replace('{name}', element.from_display_name);
        direct_msg_c = direct_msg_c.replace('{message}', message);
        direct_msg_c = direct_msg_c.replace('{from_avatar}', element.from_avatar);
        direct_msg_c = direct_msg_c.replace('{time}', element.time);
        direct_msg_c = direct_msg_c.replace('{position}', position);
        if (type == 'prepend') {
            mQuery('.section-content').prepend(direct_msg_c);
        } else {
            mQuery('.section-content').append(direct_msg_c);
        }
        $this.render_reply_message(message_reply, element);
    },
    render_reply_message: function (message, element) {
        $this = this;
        var msg = "";
        if (element.src == 0) {
            msg = "<i class=\"fa fa-reply\"></i><span> " + message + "</span>";
            mQuery('#' + element.to_id + ' .item-content').html(msg);
        } else {
            msg = "<span> " + message + "</span>";
            mQuery('#' + element.from_id + ' .item-content').html(msg);
            mQuery('#' + element.from_id + ' .snippet').addClass('font-weight-bold');
        }
    },
    get_conversation_first: function () {
        $this = this;
        var endPoint = $this.base_url + $this.list_api_url['get_conversation'];
        mQuery.ajax({
            type: 'GET',
            url: endPoint,
            contentType: 'json',
            async: true,
            cache: false,
            data: {'user_id': $this.user_id, 'offset': 0, 'count': 10},
            beforeSend: function (xhr) {
            },
            success: function (result, status, xhr) {
                mQuery('.section-content').empty();
                $this.render_elements(result, 'prepend');
                $this.scrollBottom();
            },
            error: function (data) {
            }
        });
    },
    post_message: function (e) {
        $this = this;
        e.preventDefault();
        var endPoint = $this.base_url + $this.list_api_url['save_message'];
        var msg = mQuery('#message_send').val();
        var current_date = new Date();
        if (msg.length > 0) {
            mQuery.ajax({
                type: 'POST',
                url: endPoint,
                contentType: 'application/json',
                async: true,
                cache: false,
                data: JSON.stringify({'user_id': $this.user_id, 'message': msg, 'time': current_date.getTime()}),
                beforeSend: function (xhr) {
                    mQuery('#message_send').val('');
                },
                success: function (result, status, xhr) {
                    $this.scrollBottom();
                },
                error: function (xhr) {
                    console.log('Error', xhr.statusText);
                }
            });
            mQuery('#message_send').focus();
        }
    },
    listen_message_from_socket: function () {
        $this = this;
        if ($this.socket != null) {
            $this.socket.close();
        }

        var endPoint = $this.base_url_socket + $this.list_api_url['hook_message'] + $this.user_id + "/";
        $this.socket = new ReconnectingWebSocket(endPoint);
        $this.socket.debug = true;
        $this.socket.onopen = function (e) {
            console.log("open", e);
        };
        $this.socket.onmessage = function (e) {
            var data = JSON.parse(e.data);
            var message = data.message;
            $this.render_elements(message, 'append');
            $this.scrollBottom();
            console.log(JSON.stringify(data));
        };
        $this.socket.onclose = function (e) {
            console.log("close", e)
        };
        $this.socket.onerror = function (e) {
            console.log("error", e)
        }
    },
    scrollBottom: function () {
        mQuery('.section-chatbox').scrollTop(1000000);
    },
    search_followers: function (e) {
        $this = this;
        var search_text = mQuery('#txt_search_follower').val();
        var endPoint = $this.base_url + $this.list_api_url['search_followers'];
        mQuery.ajax({
            type: 'GET',
            url: endPoint,
            contentType: 'json',
            async: true,
            cache: false,
            data: {'name': search_text, 'offset': 0, 'count': 10},
            beforeSend: function (xhr) {
            },
            success: function (result, status, xhr) {
                mQuery('.list-item').empty();
                result.data.forEach(function (element) {
                    var clone_templete = $this.tmp_list_user;
                    element = mQuery.parseJSON(element);
                    clone_templete = clone_templete.replaceAll('{uid}', element.user_id);
                    clone_templete = clone_templete.replace('{avatar}', element.avatar);
                    clone_templete = clone_templete.replace('{name}', element.display_name);
                    clone_templete = clone_templete.replace('{time}', "");
                    mQuery('.list-item').append(clone_templete);
                });
            },
            error: function (data) {
            }
        });
    },
    get_information_follow: function () {
        $this = this;
        mQuery('.sidebar-infor-user').remove();
        if ($this.is_information_user) {
            var clone_templete = $this.tmp_information_current_user;
            clone_templete = clone_templete.replace('{avatar}', $this.user_current.avatar);
            clone_templete = clone_templete.replace('{display_name}', $this.user_current.display_name);
            clone_templete = clone_templete.replace('{user_gender}', $this.user_current.user_gender == 1 ? 'Nam' : 'Nữ');
            clone_templete = clone_templete.replace('{birth_date}', $this.user_current.birth_date == 0 ? 'Chưa công khai' : $this.user_current.birth_date);
            mQuery('.page-message-inside').append(clone_templete);
        }
    },
    display_information_follow: function (e) {
        $this = this;
        $this.is_information_user = $this.is_information_user ? false : true;
        $this.get_information_follow();
    }
};

