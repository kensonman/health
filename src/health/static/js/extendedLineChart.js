// File:    health/static/js/extendedLineChart.js
// Date:    2019-03-05 21:44
// Author:  Kenson Man <kenson@kenson.idv.hk>
// Desc:    According to [JSFiddle](https://jsfiddle.net/742zut83/22/), extend the LineChart in ChartJS for drawing the highlight-range.

// The original draw function for the line chart. This will be applied after we have drawn our highlight range (as a rectangle behind the line chart).
var originalLineDraw = Chart.controllers.line.prototype.draw;
// Extend the line chart, in order to override the draw function.
Chart.helpers.extend(Chart.controllers.line.prototype, {
  draw : function() {
    var chart = this.chart;
    // Get the object that determines the region to highlight.
    var yHighlightRange = chart.config.data.yHighlightRange;

    // If the object exists.
    if (yHighlightRange !== undefined) {
      var ctx = chart.chart.ctx;

      var yRangeBegin = yHighlightRange.begin;
      var yRangeEnd = yHighlightRange.end;

      var xaxis = chart.scales['x-axis-0'];
      var yaxis = chart.scales['y-axis-0'];

      var yRangeBeginPixel = yaxis.getPixelForValue(yRangeBegin);
      var yRangeEndPixel = yaxis.getPixelForValue(yRangeEnd);

      ctx.save();

      // The fill style of the rectangle we are about to fill.
      ctx.fillStyle = (yHighlightRange.fill==undefined)?'rgba(0, 255, 0, 0.3)':yHighlightRange.fill;
      // Fill the rectangle that represents the highlight region. The parameters are the closest-to-starting-point pixel's x-coordinate,
      // the closest-to-starting-point pixel's y-coordinate, the width of the rectangle in pixels, and the height of the rectangle in pixels, respectively.
      var x=xaxis.left;
      var y=Math.min(yRangeBeginPixel, yRangeEndPixel);
      var width=xaxis.right-xaxis.left;
      var height=Math.max(yRangeBeginPixel, yRangeEndPixel)-Math.min(yRangeBeginPixel, yRangeEndPixel);
      //ctx.fillRect(xaxis.left, Math.min(yRangeBeginPixel, yRangeEndPixel), xaxis.right - xaxis.left, Math.max(yRangeBeginPixel, yRangeEndPixel) - Math.min(yRangeBeginPixel, yRangeEndPixel));
      ctx.fillRect(x, y, width, height);

      ctx.restore();
    }

    // Apply the original draw function for the line chart.
    originalLineDraw.apply(this, arguments);
  }
});
