function createV4SelectableForceDirectedGraph(svg, graph) {
  // if both d3v3 and d3v4 are loaded, we'll assume
  // that d3v4 is called d3v4, otherwise we'll assume
  // that d3v4 is the default (d3)
  if (typeof d3v4 === 'undefined')
    d3v4 = d3;

  var width = +svg.attr("width"),
    height = +svg.attr("height");

  parentWidth = 1250;
  parentHeight = 650;

  var svg = d3v4.select('svg')
    .attr('width', parentWidth)
    .attr('height', parentHeight);

  // remove any previous graphs
  svg.selectAll('.g-main').remove();

  var gMain = svg.append('g')
    .classed('g-main', true)
    .attr("transform", "translate(" + -350 + "," + 0 + ")");

  var rect = gMain.append('rect')
    .attr('width', parentWidth)
    .attr('height', parentHeight)
    .style('fill', 'white');


  var gDraw = gMain.append('g');

  var zoom = d3v4.zoom()
    .on('zoom', zoomed)

  gMain.call(zoom);


  function zoomed() {
    gDraw.attr('transform', d3v4.event.transform);
  }

  var color = d3v4.scaleOrdinal(d3v4.schemeCategory20);

  if (!("links" in graph)) {
    console.log("Graph is missing links");
    return;
  }

  var nodes = {};
  var i;
  for (i = 0; i < graph.nodes.length; i++) {
    nodes[graph.nodes[i].id] = graph.nodes[i];
    graph.nodes[i].weight = 1.01;
  }

  // the brush needs to go before the nodes so that it doesn't
  // get called when the mouse is over a node
  var gBrushHolder = gDraw.append('g');
  var gBrush = null;

  var link = gDraw.append("g")
    .attr("class", "link")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", function (d) {
      return Math.sqrt(d.value);
    });

  var r = d3v4.scaleSqrt().range([1, 5]);
  r.domain([d3v4.min(graph.nodes, function (c) {
      return c.value;
    }),
      d3v4.max(graph.nodes, function (c) {
        return c.value;
      })]
  );

  d3.csv("/data/C2.1/name_outer_mails_degree_weighted.csv", function (error1, data1) {
    if (error1) throw error1;
    d3.csv("/data/C2.1/name_outer_mails_degree_noweight.csv", function (error2, data2) {
      if (error2) throw error2;
      d3.csv("/data/C2.1/name_outer_mails_degree_avgWeight.csv", function (error3, data3) {

        var node = gDraw.append("g")
          .attr("class", "node")
          .selectAll("circle")
          .data(graph.nodes)
          .enter().append("circle")
          .attr("r", function (d) {
            return r(d.value)
          })
          .attr("fill", function (d) {
            return color(1);
          })
          .call(d3v4.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
          .on("click", show_outer_bullet);

        var avg_dict = {};
        var max_dict = {};
        var weighted_dict = {};
        var noweight_dict = {};
        var avgWeight_dict = {};
        var total = 0;
        var max = 0;
        for (i = 0; i < data1.length; i++) {
          total += parseInt(data1[i]['weight']);
          if (parseInt(data1[i]['weight']) > max)
            max = parseInt(data1[i]['weight']);
          weighted_dict[data1[i]['name']] = parseInt(data1[i]['weight']);
        }
        max_dict['weighted'] = max;
        avg_dict['weighted'] = total / data1.length;

        max = total = 0;
        for (i = 0; i < data2.length; i++) {
          total += parseInt(data2[i]['weight']);
          if (parseInt(data2[i]['weight']) > max)
            max = parseInt(data2[i]['weight']);
          noweight_dict[data2[i]['name']] = parseInt(data2[i]['weight']);

        }
        max_dict['noweight'] = max;
        avg_dict['noweight'] = total / data2.length;

        max = total = 0;
        for (i = 0; i < data3.length; i++) {
          total += parseInt(data3[i]['weight']);
          if (parseInt(data3[i]['weight']) > max)
            max = parseInt(data3[i]['weight']);
          avgWeight_dict[data3[i]['name']] = parseInt(data3[i]['weight']);
        }
        max_dict['avgWeight'] = max;
        avg_dict['avgWeight'] = total / data3.length;

        function show_outer_bullet(d, i) {
          var margin = {top: 5, right: 40, bottom: 20, left: 150},
            width = 700 - margin.left - margin.right,
            height = 50 - margin.top - margin.bottom;

          var chart = d3.bullet()
            .width(500)
            .height(height);

          d3.selectAll(".bullet").remove();
          svg.selectAll(".show_name").remove();

          var data = [];

          var item = {};
          item['title'] = "empty";
          item['subtitle'] = "empty";
          item['measures'] = [0, 0];
          item['marker'] = [0];
          data.push(item);

          item = {};
          item['title'] = "外部邮件数";
          item['subtitle'] = "封";
          item['measures'] = [avg_dict['weighted'], max_dict['weighted']];
          item['markers'] = [weighted_dict[d.id]];
          data.push(item);

          item = {};
          item['title'] = "外部邮箱数";
          item['subtitle'] = "个";
          item['measures'] = [avg_dict['noweight'], max_dict['noweight']];
          item['markers'] = [noweight_dict[d.id]];
          data.push(item);

          item = {};
          item['title'] = "外部平均邮件数";
          item['subtitle'] = "封";
          item['measures'] = [avg_dict['avgWeight'], max_dict['avgWeight']];
          item['markers'] = [avgWeight_dict[d.id]];
          data.push(item);

          svg.append("g")
            .style("text-anchor", "end")
            .attr("transform", "translate(" + 1100 + "," + 180 + ")")
            .append("text")
            .attr("class", "show_name")
            .attr("font-size", "40px")
            .text(d.id);

          var svg2 = svg.data(data)
            .enter().append("svg")
            .attr("class", "bullet")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .attr("transform", "translate(" + 600 + "," + -250 + ")")
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .call(chart);

          var title = svg2.append("g")
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + height / 2 + ")");

          title.append("text")
            .attr("class", "title")
            .text(function (d) {
              return d.title;
            });

          title.append("text")
            .attr("class", "subtitle")
            .attr("dy", "1em")
            .text(function (d) {
              return d.subtitle;
            });
        }

// add titles for mouseover blurbs
        node.append("title")
          .text(function (d) {
            if ('name' in d)
              return d.name;
            else
              return d.id;
          });

        var simulation = d3v4.forceSimulation()
          .force("link", d3v4.forceLink()
            .id(function (d) {
              return d.id;
            })
            .distance(function (d) {
              return 30;
            })
          )
          .force("charge", d3v4.forceManyBody())
          .force("center", d3v4.forceCenter(parentWidth / 2, parentHeight / 2))
          .force("x", d3v4.forceX(parentWidth / 2))
          .force("y", d3v4.forceY(parentHeight / 2));

        simulation
          .nodes(graph.nodes)
          .on("tick", ticked);

        simulation.force("link")
          .links(graph.links);

        function ticked() {
          // update node and line positions at every step of
          // the force simulation
          link.attr("x1", function (d) {
            return d.source.x;
          })
            .attr("y1", function (d) {
              return d.source.y;
            })
            .attr("x2", function (d) {
              return d.target.x;
            })
            .attr("y2", function (d) {
              return d.target.y;
            });

          node.attr("cx", function (d) {
            return d.x;
          })
            .attr("cy", function (d) {
              return d.y;
            });
        }

        var brushMode = false;
        var brushing = false;

        var brush = d3v4.brush()
          .on("start", brushstarted)
          .on("brush", brushed)
          .on("end", brushended);

        function brushstarted() {
          // keep track of whether we're actively brushing so that we
          // don't remove the brush on keyup in the middle of a selection
          brushing = true;

          node.each(function (d) {
            d.previouslySelected = shiftKey && d.selected;
          });
        }

        rect.on('click', function (d) {
          node.each(function (d) {
            d.selected = false;
            d.previouslySelected = false;
          });

          node.classed("selected", false);

        });

        function brushed() {
          if (!d3v4.event.sourceEvent) return;
          if (!d3v4.event.selection) return;

          var extent = d3v4.event.selection;

          node.classed("selected", function (d) {
            return d.selected = d.previouslySelected ^
              (extent[0][0] <= d.x && d.x < extent[1][0]
                && extent[0][1] <= d.y && d.y < extent[1][1]);
          });

        }

        function brushended() {
          if (!d3v4.event.sourceEvent) return;
          if (!d3v4.event.selection) return;
          if (!gBrush) return;

          gBrush.call(brush.move, null);

          if (!brushMode) {
            // the shift key has been release before we ended our brushing
            gBrush.remove();
            gBrush = null;
          }

          brushing = false;
        }

        d3v4.select('body').on('keydown', keydown);
        d3v4.select('body').on('keyup', keyup);

        var shiftKey;

        function keydown() {
          shiftKey = d3v4.event.shiftKey;

          if (shiftKey) {
            // if we already have a brush, don't do anything
            if (gBrush)
              return;

            brushMode = true;

            if (!gBrush) {
              gBrush = gBrushHolder.append('g');
              gBrush.call(brush);
            }
          }
        }

        function keyup() {
          shiftKey = false;
          brushMode = false;

          if (!gBrush)
            return;

          if (!brushing) {
            // only remove the brush if we're not actively brushing
            // otherwise it'll be removed when the brushing ends
            gBrush.remove();
            gBrush = null;
          }
        }

        function dragstarted(d) {
          if (!d3v4.event.active) simulation.alphaTarget(0.9).restart();

          if (!d.selected && !shiftKey) {
            // if this node isn't selected, then we have to unselect every other node
            node.classed("selected", function (p) {
              return p.selected = p.previouslySelected = false;
            });
          }

          d3v4.select(this).classed("selected", function (p) {
            d.previouslySelected = d.selected;
            return d.selected = true;
          });

          node.filter(function (d) {
            return d.selected;
          })
            .each(function (d) { //d.fixed |= 2;
              d.fx = d.x;
              d.fy = d.y;
            })

        }

        function dragged(d) {
          //d.fx = d3v4.event.x;
          //d.fy = d3v4.event.y;
          node.filter(function (d) {
            return d.selected;
          })
            .each(function (d) {
              d.fx += d3v4.event.dx;
              d.fy += d3v4.event.dy;
            })
        }

        function dragended(d) {
          if (!d3v4.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
          node.filter(function (d) {
            return d.selected;
          })
            .each(function (d) { //d.fixed &= ~6;
              d.fx = null;
              d.fy = null;
            })
        }

        return graph;
      });
    });
  });
};
