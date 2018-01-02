$(document).ready(function () {
  var category = '';

  $('div.category-list > button').on('click', function(el) {
    console.log(this.value);
    if (category != this.value) {
      // clear old values if value changed
      $('div#all-container, div#chart-tables').html('');

      // create tables
      getData(this.value);
    }
  })
});

var xAxis = []

// month data
for (var i = 0; i < 36; i++) {
  xAxis.push(i);
}

function getData(category) {
  $.when($.get('timeseries/'+category+'.csv')).then(function(data) {
    var csv_data = $.csv.toArrays(data, {});
    var values = [];
    var name = '';
    var final = [];

    // loop over rows
    for (row_id = 0; row_id < csv_data.length; row_id++) {
      fandom = csv_data[row_id][1];

      // new fandom
      if (name != fandom) {
        if (name != '') {
          final.push({name: name, data: values.reverse()});

          createSingleChart({name: name, data: values.reverse()});
        }

        // update fandom
        name = fandom;
        values = [];
      }

      values.push(parseInt(csv_data[row_id][0]));
    }
    createSingleChart({ name: name, data: values.reverse() });
    createTopChart(final, category);
  });
}

function createTopChart(series, category) {
  Highcharts.chart('all-container', {
    title: {
      text: 'Top 25 Fandoms in ' + category
    },
    subtitle: {
      text: 'Source: archiveofourown.org'
    },
    yAxis: {
      title: {
        text: 'Total Works Added'
      }
    },
    xAxis: {
      categories: xAxis
    },
    legend: {
      layout: 'horizontal',
      align: 'center',
      verticalAlign: 'bottom'
    },
    series: series
  });
}

function createSingleChart(series) {
  var i = $('#chart-tables > div').length;

  $('<div id="SingleChart'+i+'">').appendTo($('#chart-tables'));

  Highcharts.chart('SingleChart'+i, {
    title: {
      text: series.name
    },
    subtitle: {
      text: 'Source: archiveofourown.org'
    },
    yAxis: {
      title: {
        text: 'Total Works Added'
      }
    },
    xAxis: {
      categories: xAxis
    },
    legend: {
      layout: 'horizontal',
      align: 'center',
      verticalAlign: 'bottom'
    },
    series: [series]
  });
}

// Google Analytics
if (window.location.hostname != 'localhost') {
  (function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function () {
      (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date();
    a = s.createElement(o),
      m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
  })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
  ga('create', 'UA-93496143-1', 'auto');
  ga('send', 'pageview');
}