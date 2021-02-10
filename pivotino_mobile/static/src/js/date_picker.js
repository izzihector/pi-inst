odoo.define('pivotino_mobile.datepicker', function (require) {
    "use strict";

    var core = require('web.core');
    var time = require('web.time');
    var web_datepicker = require('web.datepicker');
    var Dialog = require('web.Dialog');
    var FormRenderer = require('web.FormRenderer');
    var ListRenderer = require('web.ListRenderer');
    var ViewDialogs = require('web.view_dialogs');

    Dialog.include({
        renderElement: function () {
            this._super();
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                // Remove & Add nativeDatePicker element
                $('div.nativeWebViewDateTimePickerContainer').remove();
                this.$el.append("<div class='nativeWebViewDateTimePickerContainer '>" +
                  "<input type='date' class='nativeWebViewDatePicker' />" +
                  "<input type='datetime-local' class='nativeWebViewDateTimePicker' />" +
                  "</div>");
            }
        },

        _focusOnClose: function() {
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                // Remove & Add nativeDatePicker element
                $('div.nativeWebViewDateTimePickerContainer').remove();
                this.$el.append("<div class='nativeWebViewDateTimePickerContainer '>" +
                  "<input type='date' class='nativeWebViewDatePicker' />" +
                  "<input type='datetime-local' class='nativeWebViewDateTimePicker' />" +
                  "</div>");
            }
            return false;
        },
    });

    FormRenderer.include({
        _renderView: function () {
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                // Remove & Add nativeDatePicker element
                $('div.nativeWebViewDateTimePickerContainer').remove();
                $('body.o_web_client').append("<div class='nativeWebViewDateTimePickerContainer '>" +
                  "<input type='date' class='nativeWebViewDatePicker' />" +
                  "<input type='datetime-local' class='nativeWebViewDateTimePicker' />" +
                  "</div>");
            }
            return this._super();
        },
    });

    ListRenderer.include({
        _renderView: function () {
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                // Remove & Add nativeDatePicker element
                $('div.nativeWebViewDateTimePickerContainer').remove();
                $('body.o_web_client').append("<div class='nativeWebViewDateTimePickerContainer '>" +
                  "<input type='date' class='nativeWebViewDatePicker' />" +
                  "<input type='datetime-local' class='nativeWebViewDateTimePicker' />" +
                  "</div>");
            }
            return this._super();
        },
    });

    ViewDialogs.SelectCreateDialog.include({
        _focusOnClose: function() {
            this._super.apply(this, arguments);
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                // Remove & Add nativeDatePicker element
                $('div.nativeWebViewDateTimePickerContainer').remove();
                $('body.o_web_client').append("<div class='nativeWebViewDateTimePickerContainer '>" +
                  "<input type='date' class='nativeWebViewDatePicker' />" +
                  "<input type='datetime-local' class='nativeWebViewDateTimePicker' />" +
                  "</div>");
            }
        },
    });

    web_datepicker.DateWidget.include({
        /**
         * @override
         */
        start: function () {
            this.$input = this.$('input.o_datepicker_input');
            this.__libInput++;
            if (window.pivotinoMobile &&
              window.pivotinoMobile.nativeWebView &&
              window.pivotinoMobile.nativeWebView === 'nativeWebView') {
                this.$el.datetimepicker('destroy');
                this.__libInput--;
                this._setReadonly(true);
                this._invokePivotinoMobilePicker();
            } else {
                this.$el.datetimepicker(this.options);
                this.__libInput--;
                this._setReadonly(false);
            }
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _invokePivotinoMobilePicker: function () {
            var self = this;
            var moment_obj = false;
            this.$el.on('click', function (ev) {
                if(self.type_of_date === 'date') {
                    var dateFormat = time.getLangDateFormat();
                    moment_obj = moment(self.$el.find("input.o_datepicker_input").val());
                    var $nativeDatePicker = $('div.nativeWebViewDateTimePickerContainer input.nativeWebViewDatePicker');
                    $nativeDatePicker.val(moment_obj.format('YYYY-MM-DD'));
                    $nativeDatePicker.focus().click();
                    $nativeDatePicker.change(function (ev) {
                        if (!ev.target.value) {
                            self.$input.val('');
                        } else {
                            self.$input.val(moment(ev.target.value).format(dateFormat));
                        }
                        self.changeDatetime();
                    });
                }
                if(self.type_of_date === 'datetime') {
                    var datetimeFormat = time.getLangDatetimeFormat();
                    moment_obj = moment(self.$el.find("input.o_datepicker_input").val());
                    var $nativeDateTimePicker = $('div.nativeWebViewDateTimePickerContainer input.nativeWebViewDateTimePicker');
                    $nativeDateTimePicker.val(moment_obj.format('YYYY-MM-DD'));
                    $nativeDateTimePicker.focus().click();
                    $nativeDateTimePicker.change(function (ev) {
                        if (!ev.target.value) {
                            self.$input.val('');
                        } else {
                            self.$input.val(moment(ev.target.value).format(datetimeFormat));
                        }
                        self.changeDatetime();
                    });
                }

                /**
                 *  @todo > @bud-e <
                 *      [FIX] Need to handle above feature in proper way...
                 *      Above implementation is not good for long-term
                 */
                // var value = self.getValue() ? self.getValue().format("YYYY-MM-DD HH:mm:ss") : false,
                //     type = self.type_of_date,
                //     ignore_timezone = true;
                // var nativeDateTimePicker =
                //   window.pivotinoMobile.methods.nativeDateTimePicker(
                //     value, type, ignore_timezone);
                // console.log("nativeDateTimePicker>>>>>>>>>>>>>>", nativeDateTimePicker);
                // return new Date();
            });
        },
    });

});
