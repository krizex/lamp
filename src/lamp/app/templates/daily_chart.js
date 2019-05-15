    <div id="{{r.TYPE}}_{{r.code}}" style="width: 550px; height: 400px; margin: 0 auto"></div>
    <script language = "JavaScript">
    $(document).ready(function() {
        var title = {
            text: null
        };
        var chart = {
            zoomType: 'xy'
        };
        var xAxis = {
            categories: {{r.last_n_days_date | safe }},
            crosshair: true
        };
        var yAxis = [
            { // Primary yAxis
                title: {
                    text: 'Price',
                },
            }, 
            { // Secondary yAxis
                title: {
                    text: 'Vol',
                },
                opposite: true
            }
        ];
        var tooltip = {
            shared: true
        };
        var legend = {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,

            backgroundColor: (
                Highcharts.theme && Highcharts.theme.legendBackgroundColor)
                || '#FFFFFF'
        };
        var series = [
            {
                name: 'Vol',
                type: 'column',
                yAxis: 1,
                data: {{r.last_n_days_vol | safe}},
            },
            {
                name: 'Price',
                type: 'spline',
                yAxis: 0,
                data: {{r.last_n_days_price | safe}},
            },
        ];   

        var json = {};   
        json.title = title;
        json.chart = chart;       
        json.xAxis = xAxis;
        json.yAxis = yAxis;
        json.tooltip = tooltip;  
        json.legend = legend;  
        json.series = series;
        $('#{{r.TYPE}}_{{r.code}}').highcharts(json);  
    });
</script>
