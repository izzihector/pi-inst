odoo.define('ks_dashboard_ninja_list.ks_dashboard_graph_preview', function(require) {
    "use strict";

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var utils = require('web.utils');
    var config = require('web.config');
    var field_utils = require('web.field_utils');
    var KsGlobalFunction = require('ks_dashboard_ninja.KsGlobalFunction');

    var QWeb = core.qweb;

    var MAX_LEGEND_LENGTH = 25 * (Math.max(1, config.device.size_class));

    var KsGraphPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],

        resetOnAnyFieldChange: true,

        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
            '/ks_dashboard_ninja/static/lib/js/chartjs-plugin-datalabels.js',
            '/ks_dashboard_ninja/static/lib/js/gauge.min.js',
            '/ks_dashboard_ninja/static/lib/js/chart.funnel.js',
            '/ks_dashboard_ninja/static/lib/js/chartjs-plugin-style.js',
        ],
        cssLibs: [
            '/ks_dashboard_ninja/static/lib/css/Chart.min.css'
        ],

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
        },

        start: function() {
            var self = this;
            self.ks_set_default_chart_view();
            core.bus.on("DOM_updated", this, function() {
                if (self.shouldRenderChart && $.find('#ksMyChart').length > 0) self.renderChart();
            });
            Chart.plugins.unregister(ChartDataLabels);
            return this._super();
        },

        ks_set_default_chart_view: function() {
            Chart.plugins.register({
                afterDraw: function(chart) {
                    if (chart.data.labels.length === 0 && chart.config.type != 'tsgauge') {
                        // No data is present
                        var ctx = chart.chart.ctx;
                        var width = chart.chart.width;
                        var height = chart.chart.height
                        chart.clear();

                        ctx.save();
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.font = "3rem 'Lucida Grande'";
                        ctx.fillText('No data available', width / 2, height / 2);
                        ctx.restore();
                    }
                }
            });

            Chart.Legend.prototype.afterFit = function() {
                var chart_type = this.chart.config.type;
                if (chart_type === "pie" || chart_type === "doughnut") {
                    this.height = this.height;
                } else {
                    this.height = this.height + 20;
                };
            }
        },

        _render: function() {
            this.$el.empty()
            if (this.recordData.ks_dashboard_item_type !== 'ks_tile' && this.recordData.ks_dashboard_item_type !== 'ks_kpi' && this.recordData.ks_dashboard_item_type !== 'ks_list_view') {
                if (this.recordData.ks_model_id) {
                    if (this.recordData.ks_dashboard_item_type == 'ks_tsgauge'){
                        if (!this.recordData.ks_model_id_2) {
                            return this.$el.append($('<div>').text("Select Second Model in Data #2"));
                        } else if (this.recordData.ks_record_count_type_2 !== 'count' && !this.recordData.ks_record_field_2){
                            return this.$el.append($('<div>').text("Select Second Model Field in Data #2"));
                        }else {
                            this._getChartData();
                        }
                    } else {
                        if (this.recordData.ks_chart_groupby_type == 'date_type' && !this.recordData.ks_chart_date_groupby) {
                            return this.$el.append($('<div>').text("Select Group by date to create chart based on date groupby"));
                        } else if (this.recordData.ks_chart_data_count_type === "count" && !this.recordData.ks_chart_relation_groupby) {
                            this.$el.append($('<div>').text("Select Group By to create chart view"));
                        } else if (this.recordData.ks_chart_data_count_type !== "count" && (this.recordData.ks_chart_measure_field.count === 0 || !this.recordData.ks_chart_relation_groupby)) {
                            this.$el.append($('<div>').text("Select Measure and Group By to create chart view"));
                        } else if (!this.recordData.ks_chart_data_count_type) {
                            this.$el.append($('<div>').text("Select Chart Data Count Type"));
                        } else {
                            this._getChartData();
                        }
                    }
                } else {
                    this.$el.append($('<div>').text("Select a Model first."));
                }

            }

        },

        _getChartData: function() {
            var self = this;
            self.shouldRenderChart = true;
            var field = this.recordData;
            var ks_chart_name;
            if (field.name) ks_chart_name = field.name;
            else if (field.ks_model_name) ks_chart_name = field.ks_model_id.data.display_name;
            else ks_chart_name = "Name";

            this.chart_type = this.recordData.ks_dashboard_item_type.split('_')[1];
            this.chart_data = JSON.parse(this.recordData.ks_chart_data);

            var $chartContainer = $(QWeb.render('ks_chart_form_view_container', {
                ks_chart_name: ks_chart_name
            }));
            this.$el.append($chartContainer);

            switch (this.chart_type) {
                case "pie":
                case "doughnut":
                case "funnel":
                case "polarArea":
                    this.chart_family = "circle";
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                case "area":
                    this.chart_family = "square"
                    break;
                default:
                    this.chart_family = "none";
                    break;
            }

            if (this.chart_family === "circle") {
                if (this.chart_data && this.chart_data['labels'].length > 30) {
                    this.$el.find(".card-body").empty().append($("<div style='font-size:20px;'>Too many records for selected Chart Type. Consider using <strong>Domain</strong> to filter records or <strong>Record Limit</strong> to limit the no of records under <strong>30.</strong>"));
                    return;
                }
            }
            if ($.find('#ksMyChart').length > 0) {
                this.renderChart();
            }
        },

        renderChart: function() {
            var self = this;
            if (this.recordData.ks_chart_measure_field_2.count && this.recordData.ks_dashboard_item_type === 'ks_bar_chart') {
                var self = this;
                var scales = {}
                scales.yAxes = [{
                        type: "linear",
                        display: true,
                        position: "left",
                        id: "y-axis-0",
                        gridLines: {
                            display: true
                        },
                        labels: {
                            show: true,
                        }
                    },
                    {
                        type: "linear",
                        display: true,
                        position: "right",
                        id: "y-axis-1",
                        labels: {
                            show: true,
                        },
                        ticks: {
                            beginAtZero: true,
                            callback: function(value, index, values) {
                                var ks_selection = self.chart_data.ks_selection;
                                if (ks_selection === 'monetary') {
                                    var ks_currency_id = self.chart_data.ks_currency;
                                    var ks_data = KsGlobalFunction.ksNumFormatter(value, 4);
                                    ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                                    return ks_data;
                                } else if (ks_selection === 'custom') {
                                    var ks_field = self.chart_data.ks_field;
                                    return KsGlobalFunction.ksNumFormatter(value, 4) + ' ' + ks_field;
                                } else {
                                    return KsGlobalFunction.ksNumFormatter(value, 4);
                                }
                            },
                        }
                    }
                ]

            }
            if (this.recordData.ks_dashboard_item_type === 'ks_tsgauge'){
                this.ksMyChart = new Chart($.find('#ksMyChart')[0], {
                    type: "tsgauge",
                    data: {
                        datasets: this.chart_data.datasets,
                    },
                    options: {
                        borderWidth: 0,
                        maintainAspectRatio: false,
                        events: [],
                        showMarkers: true,
                        gaugeLayout: this.chart_data.ks_gauge_layout,
                        arrowAnimation: this.chart_data.arrow_animation,
                        fontColor: this.chart_data.font_color,
                        cutoutPercentage: this.chart_data.thickness,
                        labelUnit: this.chart_data.ks_field,
                        gaugeDP: this.chart_data.ks_gauge_dp,
                        arrowColor: this.chart_data.ks_arrow_color,
                        limitPercent: this.chart_data.ks_gauge_limits_percent,
                        gaugeColors: this.chart_data.ks_gauge_colors,
                        showMinMaxOnly: this.chart_data.ks_show_min_max_only,
                        layout: {
                            padding: {
                                top: 50,
                                bottom: 30,
                            }
                        }
                    }
                });
            } else {
                var chart_plugin = [];
                if (this.recordData.ks_show_data_value) {
                    chart_plugin.push(ChartDataLabels);
                }
                this.ksMyChart = new Chart($.find('#ksMyChart')[0], {
                    type: this.chart_type === "area" ? "line" : this.chart_type,
                    plugins: chart_plugin,
                    data: {
                        labels: this.chart_data['labels'],
                        datasets: this.chart_data.datasets,
                    },
                    options: {
                        maintainAspectRatio: false,
                        labelUnit: this.chart_data.ks_field,
                        cutoutPercentage: 70,
                        animation: {
                            easing: 'easeInQuad',
                        },
                        legend: {
                                onClick: function(e){
                                     e.stopPropagation();
                                 },
                                display: this.recordData.ks_hide_legend
                            },
                        layout: {
                            padding: {
                                bottom: 0,
                            }
                        },
                        scales: scales,
                        plugins: {
                            datalabels: {
                                backgroundColor: function(context) {
                                    return context.dataset.backgroundColor;
                                },
                                borderRadius: 4,
                                color: 'white',
                                font: {
                                    weight: 'bold'
                                },
                                anchor: 'center',
                                textAlign: 'center',
                                display: 'auto',
                                clamp: true,
                                formatter: function(value, ctx) {
                                    let sum = 0;
                                    let dataArr = ctx.dataset.data;
                                    dataArr.map(data => {
                                        sum += data;
                                    });
                                    let percentage = sum === 0 ? 0 + "%" : (value * 100 / sum).toFixed(2) + "%";
                                    return percentage + ' (' + value +')';;
                                },
                            },
                        },

                    }
                });
            }
            if (this.chart_data && this.chart_data["datasets"].length > 0) {
                self.ksChartColors(this.recordData.ks_chart_item_color, this.ksMyChart, this.chart_type, this.chart_family, this.recordData.ks_show_data_value);
            }
        },

        ksHideFunction: function(options, recordData, ksChartFamily, chartType) {
            return options;
        },

        ksChartColors: function(palette, ksMyChart, ksChartType, ksChartFamily, ks_show_data_value) {
            var self = this;
            var currentPalette = "cool";
            if (!palette) palette = currentPalette;
            currentPalette = palette;

            /*Gradients
              The keys are percentage and the values are the color in a rgba format.
              You can have as many "color stops" (%) as you like.
              0% and 100% is not optional.*/
            var gradient;
            switch (palette) {
                case 'cool':
                    var color_set = ['#4570d7', '#95aee9', '#9e5193', '#d5bcfc', '#fcad2a', '#fdd086', '#26dedd', '#b1f3f3', '#c02f70', '#e8a2c2', '#11cb75', '#76f6c3']
                    break;
                case 'warm':
                    var color_set = ['#45ada8', '#9de0ad', '#70a4d8', '#4166c1', '#fd769f', '#e086f4', '#dd4dab', '#b10ed6', '#1e778b', '#ff9c00', '#f9c36e', '#f1f49f']
                    break;
                case 'neon':
                    var color_set = ['#e52db1', '#04dce8', '#a67afc', '#42eda3', '#f16bef', '#526eee', '#6f87bc', '#23d948', '#ffcf00', '#5d4157', '#ff9900', '#f65a98']
                    break;
                case 'scheme_four':
                    var color_set = ['#e81760', '#dd3a99', '#bb5fc7', '#867ce4', '#3c92ec', '#00c9f3', '#31e0e8', '#27b2b8', '#00caa7', '#62dd7c', '#b8e73e', '#e6e80e']
                    break;
                case 'scheme_five':
                    var color_set = ['#926be7', '#b39cf9', '#6ebcf4', '#fccffc', '#fe7fd3', '#75f7d9', '#31e0e8', '#27b2b8', '#e894b5', '#fee741', '#b8e73e', '#50e45e']
                    break;
                case 'scheme_six':
                    var color_set = ['#255c99', '#2d6b57', '#618b25', '#b0b939', '#ffe74c', '#ff9933', '#cb4d26', '#ff0054', '#da627d', '#ffa5ab', '#582c4d', '#033f63']
                    break;
                case 'scheme_seven':
                    var color_set = ['#983e95', '#8539a1', '#6734ab', '#3f2eb5', '#1e6ec8', '#15a7d1', '#00e58f', '#26b780', '#4c8972', '#5f726b', '#725b63', '#85445c']
                    break;
                case 'scheme_eight':
                    var color_set = ['#faa307', '#e85d04', '#dc2f02', '#9d0208', '#740839', '#f75590', '#ce2c80', '#dc758f', '#96d3d2', '#2ca6a4', '#1b7c7d', '#166364']
                    break;
                case 'default':
                    var color_set = ['#f04f65', '#f69032', '#fdc233', '#53cfce', '#36a2ec', '#8a79fd', '#b1b5be', '#1c425c', '#8c2620', '#71ecef', '#0b4295', '#f2e6ce', '#1379e7']
            }



            //Find datasets and length
            var chartType = ksMyChart.config.type;

            switch (chartType) {
                case "pie":
                case "doughnut":
                case "funnel":
                case "polarArea":
                    var datasets = ksMyChart.config.data.datasets[0];
                    var setsCount = datasets.data.length;
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                    var datasets = ksMyChart.config.data.datasets;
                    var setsCount = datasets.length;
                    break;
            }

            //Calculate colors
            var chartColors = [];

            for (var i = 0, counter = 0; i < setsCount; i++, counter++) {
                    if (counter >= color_set.length) counter = 0; // reset back to the beginning

                    chartColors.push(color_set[counter]);
                }


            var datasets = ksMyChart.config.data.datasets;
            var options = ksMyChart.config.options;

            options.legend.labels.usePointStyle = true;
            if (ksChartFamily == "circle") {
                if (ks_show_data_value) {
                    options.legend.position = 'bottom';
                    options.layout.padding.top = 10;
                    options.layout.padding.bottom = 20;
                } else {
                    options.legend.position = 'bottom';
                }

                options = this.ksHideFunction(options, this.recordData, ksChartFamily, chartType);
                options.plugins.datalabels.align = 'center';
                options.plugins.datalabels.anchor = 'end';
                options.plugins.datalabels.borderColor = 'white';
                options.plugins.datalabels.borderRadius = 25;
                options.plugins.datalabels.borderWidth = 2;
                options.plugins.datalabels.clamp = true;
                options.plugins.datalabels.clip = false;
                options.tooltips.callbacks = {
                    title: function(tooltipItem, data) {
                        var ks_self = self;
                        var k_amount = data.datasets[tooltipItem[0].datasetIndex]['data'][tooltipItem[0].index];
                        var ks_selection = ks_self.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            var ks_currency_id = ks_self.chart_data.ks_currency;
                            k_amount = KsGlobalFunction.ks_monetary(k_amount, ks_currency_id);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        } else if (ks_selection === 'custom') {
                            var ks_field = ks_self.chart_data.ks_field;
                            //                                                        ks_type = field_utils.format.char(ks_field);
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount + " " + ks_field;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        }
                    },
                    label: function(tooltipItem, data) {
                        return data.labels[tooltipItem.index];
                    },

                }
                for (var i = 0; i < datasets.length; i++) {
                    datasets[i].backgroundColor = chartColors;
                    datasets[i].borderColor = "rgba(255,255,255,1)";
                }
                if (this.recordData.ks_semi_circle_chart && (chartType === "pie" || chartType === "doughnut")) {
                    options.rotation = 1 * Math.PI;
                    options.circumference = 1 * Math.PI;
                }
            } else if (ksChartFamily == "square") {
                options = this.ksHideFunction(options, this.recordData, ksChartFamily, chartType);

                options.scales.xAxes[0].gridLines.display = false;
                options.scales.yAxes[0].ticks.beginAtZero = true;
                options.plugins.datalabels.align = 'end';

                options.plugins.datalabels.formatter = function(value, ctx) {
                    var ks_self = self;
                    var ks_selection = ks_self.chart_data.ks_selection;
                    if (ks_selection === 'monetary') {
                        var ks_currency_id = ks_self.chart_data.ks_currency;
                        var ks_data = KsGlobalFunction.ksNumFormatter(value, 4);
                        ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                        return ks_data;
                    } else if (ks_selection === 'custom') {
                        var ks_field = ks_self.chart_data.ks_field;
                        return KsGlobalFunction.ksNumFormatter(value, 4) + ' ' + ks_field;
                    } else {
                        return KsGlobalFunction.ksNumFormatter(value, 4);
                    }
                };

                if (chartType === "line") {
                    options.plugins.datalabels.backgroundColor = function(context) {
                        return context.dataset.borderColor;
                    };
                }


                if (chartType === "horizontalBar") {
                    options.scales.xAxes[0].ticks.callback = function(value, index, values) {
                        var ks_self = self;
                        var ks_selection = ks_self.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            var ks_currency_id = ks_self.chart_data.ks_currency;
                            var ks_data = KsGlobalFunction.ksNumFormatter(value, 4);
                            ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                            return ks_data;
                        } else if (ks_selection === 'custom') {
                            var ks_field = ks_self.chart_data.ks_field;
                            return KsGlobalFunction.ksNumFormatter(value, 4) + ' ' + ks_field;
                        } else {
                            return KsGlobalFunction.ksNumFormatter(value, 4);
                        }
                    }
                    options.scales.xAxes[0].ticks.beginAtZero = true;
                } else {
                    options.scales.yAxes[0].ticks.callback = function(value, index, values) {
                        var ks_self = self;
                        var ks_selection = ks_self.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            var ks_currency_id = ks_self.chart_data.ks_currency;
                            var ks_data = KsGlobalFunction.ksNumFormatter(value, 4);
                            ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                            return ks_data;
                        } else if (ks_selection === 'custom') {
                            var ks_field = ks_self.chart_data.ks_field;
                            return KsGlobalFunction.ksNumFormatter(value, 4) + ' ' + ks_field;
                        } else {
                            return KsGlobalFunction.ksNumFormatter(value, 4);
                        }
                    }
                }
                options.tooltips.callbacks = {
                    label: function(tooltipItem, data) {
                        var ks_self = self;
                        var k_amount = data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem.index];
                        var ks_selection = ks_self.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            var ks_currency_id = ks_self.chart_data.ks_currency;
                            k_amount = KsGlobalFunction.ks_monetary(k_amount, ks_currency_id);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount
                        } else if (ks_selection === 'custom') {
                            var ks_field = ks_self.chart_data.ks_field;
                            // ks_type = field_utils.format.char(ks_field);
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount + " " + ks_field;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array);
                            return data.datasets[tooltipItem.datasetIndex]['label'] + " : " + k_amount
                        }
                    }
                }

                for (var i = 0; i < datasets.length; i++) {
                    switch (ksChartType) {
                        case "bar":
                        case "horizontalBar":
                            if (datasets[i].type && datasets[i].type == "line") {
                                datasets[i].borderColor = chartColors[i];
                                datasets[i].backgroundColor = "rgba(255,255,255,0)";
                                datasets[i]['datalabels'] = {
                                    backgroundColor: chartColors[i],
                                }

                            } else {
                                datasets[i].backgroundColor = chartColors[i];
                                datasets[i].borderColor = "rgba(255,255,255,0)";
                                options.scales.xAxes[0].stacked = this.recordData.ks_bar_chart_stacked;
                                options.scales.yAxes[0].stacked = this.recordData.ks_bar_chart_stacked;
                            }
                            break;
                        case "line":
                            datasets[i].borderColor = chartColors[i];
                            datasets[i].backgroundColor = "rgba(255,255,255,0)";
                            break;
                        case "area":
                            datasets[i].borderColor = chartColors[i];
                            break;
                    }
                }

            }
            ksMyChart.update();
            if (this.$el.find('canvas').height() < 250) {
                this.$el.find('canvas').height(250);
            }
        },


    });
    registry.add('ks_dashboard_graph_preview', KsGraphPreview);

    return {
        KsGraphPreview: KsGraphPreview,
    };

});