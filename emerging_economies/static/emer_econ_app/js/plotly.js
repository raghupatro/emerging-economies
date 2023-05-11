function genrateGraph(data, plotId, typeOfGraph, orientationType) {
  var xValues = [];
  var yValues = [];
  data = data[1];
  data.forEach(genratedData);

  function genratedData(item, index) {
    let date = new Date(item.date);
    if (item.value != null) {
      xValues.push(date.getFullYear());
      yValues.push(item.value);
    }
  }

  var dataPlot = [
    {
      x: xValues,
      y: yValues,
      type: typeOfGraph,
      orientation: orientationType,
    },
  ];

  var layout = {
    autosize: true,
    font: {
      family: 'Open Sans, serif',
      size: 12,
      // color: '#7f7f7f'
    },
    margin: {
      l: 20,
      r: 20,
      b: 100,
      t: 100,
      pad: 1
    },
    paper_bgcolor: '#dedede',
    plot_bgcolor: '#dedede',
    xaxis: {
      type: "date",
      title: "Years",
      ticks: "outside",
      tick0: 0,
      dtick: "M12",
      tickformat: '%Y',
      fixedrange: true,
      automargin: true,
    },
    yaxis: {
      title: "Values",
      fixedrange: true,
      automargin: true,
    },
    title: "Time vs Value",
  };

  const config = {
    displayModeBar: false, // this is the line that hides the bar.
  };

  Plotly.newPlot(plotId, dataPlot, layout, config);
}
