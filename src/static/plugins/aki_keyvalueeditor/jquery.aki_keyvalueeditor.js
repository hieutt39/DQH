(function ($) {
    var methods = {
        //Not sure if this is needed
        settings: function () {
        },

        //Initialization
        init: function (options) {
            methods.settings = $.extend({}, $.fn.aka_keyvalueeditor.defaults, options);

            return this.each(function () {
                var $this = $(this);
                var data = $this.data('keyvalueeditor');
                // Not already initialized
                if (!data) {
                    data = {
                        settings: methods.settings,
                        editor: $this
                    };
                    data.settings.temp_row = $(data.editor).find('.keyvalueeditor-row:last').clone();
                    // methods.debug($this)
                    $this.on("focus.keyvalueeditor", '.keyvalueeditor-row:last', data, methods.focusEventHandler);
                    $this.on("blur.keyvalueeditor", '.keyvalueeditor-row input', data, methods.blurEventHandler);
                    $this.on("click.keyvalueeditor", '.keyvalueeditor-delete', data, methods.deleteRowHandler);
                    $this.on("blur.keyvalueeditor", '#keyvalueeditor-textarea', data, methods.blurEventHandlerTextArea);
                    $this.on("change.keyvalueeditor", '.keyvalueeditor-valueTypeSelector', data, methods.valueTypeSelectEventHandler);

                    $(this).data('keyvalueeditor', data);
                }
            });
        },
        getLastRow: function (state) {
            var lastrow = state.settings.temp_row;
            var h;
            h = '<div class="form-group keyvalueeditor-row">';
            h += lastrow.html();
            h += '</div>';
            return h;
        },
        focusEventHandler: function (event) {
            var editableKeys = event.data.settings.editableKeys;

            if (!editableKeys) {
                return;
            }

            $(this).removeClass('keyvalueeditor-last');
            var row = methods.getLastRow(event.data);
            $(this).after(row);
        },

        rowFocusEventHandler: function (event) {
            var data = event.data;
            data.settings.onFocusElement(event);
            methods.debug(data)
        },
        blurEventHandler: function (event) {
            var data = event.data;
            var delegateTarget = event.delegateTarget;
            data.settings.onBlurElement();
            var currentFormFields = methods.getValues($(delegateTarget));
            $("#keyvalueeditor-textarea").val(methods.settings.formToTextFunction(currentFormFields));
        },
        deleteRowHandler: function (event) {
            var parentDiv = $(this).parent().parent().parent();
            var delegateTarget = event.delegateTarget;
            parentDiv.remove();
            var data = event.data;
            data.settings.onDeleteRow();
            var currentFormFields = methods.getValues($(delegateTarget));
            $("#keyvalueeditor-textarea").val(methods.settings.formToTextFunction(currentFormFields));

        },
        valueTypeSelectEventHandler: function (event) {
            var target = event.currentTarget;
            var valueType = $(target).val();
            var valueTypes = event.data.settings.valueTypes;
            for (var i = 0; i < valueTypes.length; i++) {
                $(target).parent().find('.keyvalueeditor-value').css("display", "none");
            }
            $(target).parent().find('input[type="' + valueType + '"]').css("display", "inline-block");
        },
        blurEventHandlerTextArea: function (event) {
            var data = event.data;
            var text = $(this).val();
            var newFields = data.settings.textToFormFunction(text);
            data.editor.aka_keyvalueeditor('reset', newFields)
        },
        getValues: function (parentDiv) {
            if (parentDiv == null) {
                parentDiv = $(this);
            }
            var pairs = [];
            parentDiv.find('.keyvalueeditor-row').each(function () {
                // var isEnabled = $(this).find('.keyvalueeditor-rowcheck').is(':checked');
                // if(!isEnabled) {
                //     return true;
                // }
                var key = $(this).find('.keyvalueeditor-key').val();
                var value = $(this).find('.keyvalueeditor-value').val();
                var type = $(this).find('.keyvalueeditor-valueTypeSelector').val();

                if (type === undefined) {
                    type = "text";
                }

                if (key) {
                    var pair = {
                        key: key.trim(),
                        value: value.trim(),
                        type: type,
                        name: key
                    };

                    pairs.push(pair);
                }
            });

            return pairs;
        },
        //For external use
        addParam: function (param, state) {
            if (typeof param === "object") {
                var lastrow = state.settings.temp_row.clone();
                $(lastrow).find('.keyvalueeditor-key').val(param.key)
                $(lastrow).find('.keyvalueeditor-value').val(param.value)
                $(state.editor).append(lastrow)
            }
        },
        //Check for duplicates here
        addParams: function (params, state) {
            if (!state) {
                state = $(this).data('keyvalueeditor');
            }

            var count = params.length;
            for (var i = 0; i < count; i++) {
                var param = params[i];
                methods.addParam(param, state);
            }
        },
        clear: function (state) {
            $(state.editor).find('.keyvalueeditor-row').each(function () {
                $(this).remove();
            });
            $("#keyvalueeditor-form-div").val("");
            if (state.settings.editableKeys) {
                var h = methods.getLastRow(state);
                $(state.editor).find("#keyvalueeditor-form-div").after(h);
            }

        },
        reset: function (params, state) {
            if (state == null) {
                state = $(this).data('keyvalueeditor');
            }
            methods.clear(state);
            if (params) {
                methods.addParams(params, state);
            }

            state.settings.onReset();
        },
        debug: function (msg) {
            if (methods.settings.show_debug) {
                console.log(msg);
            }
        }
    };
    $.fn.aka_keyvalueeditor = function (method) {
        // Method calling logic
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on jQuery.aka_keyvalueeditor');
        }
    };
    $.fn.aka_keyvalueeditor.defaults = {
        type: "normal",
        fields: 2,
        deleteButton: "Delete",
        toggleButton: "Toggle view",
        placeHolderKey: "Key",
        placeHolderValue: "Value",
        valueTypes: ["text"],
        editableKeys: true,
        show_debug: false,
        temp_row: '',
        onInit: function () {
        },
        onReset: function () {
        },
        onFocusElement: function () {
        },
        onBlurElement: function () {
        },
        onDeleteRow: function () {
        },
        onAddedParam: function () {
        },
        textToFormFunction: function (text) {
            var lines = text.split("\n");
            var numLines = lines.length;
            var newHeaders = [];
            var i;
            for (i = 0; i < numLines; i++) {
                var newHeader = {};
                var thisPair = lines[i].split(":");
                if (thisPair.length != 2) {
                    console.log("Incorrect format for " + lines[i]);
                    continue;
                }
                newHeader["key"] = newHeader["name"] = thisPair[0].trim();
                newHeader["type"] = "text";
                newHeader["value"] = thisPair[1].trim();
                newHeaders.push(newHeader);
            }
            return newHeaders;
        },
        formToTextFunction: function (arr) {
            var text = "";
            var len = arr.length;
            var i = 0;
            for (i = 0; i < len; i++) {
                text += arr[i]["key"] + ": " + arr[i]["value"] + "\n";
            }
            return text;
        }
    };
})(jQuery);