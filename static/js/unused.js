//This is a unused script after move onto C3
var medshare_data;
var medsum_data;
var kol_data;
var wordfreq_data;

function get_url_param(){
  var _GET = {},
    args = location.search.substr(1).split(/&/);
  for (var i=0; i<args.length; ++i) {
      var tmp = args[i].split(/=/);
      if (tmp[0] != "") {
          _GET[decodeURIComponent(tmp[0])] = decodeURIComponent(tmp.slice(1).join("").replace("+", " "));
      }
  }
  return _GET;
}

function d3_zindex(){
  // set SVG element to the highest layer on SVG
  d3.selection.prototype.moveToFront = function() {
    return this.each(function(){
      this.parentNode.appendChild(this);
    });
  };

  // set SVG element to its normal layer on SVG
  d3.selection.prototype.moveToBack = function() { 
      return this.each(function() { 
          var firstChild = this.parentNode.firstChild; 
          if (firstChild) { 
              this.parentNode.insertBefore(this, firstChild); 
          } 
      }); 
  };
}

// Start media share
// Customized from http://bl.ocks.org/mbostock/3884955
function load_media_share(){
  var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = $(window).width() - margin.left - margin.right - 100,
    height = 300 - margin.top - margin.bottom,
    parseDate = d3.time.format("%Y-%m-%d").parse;

  var canvas = d3.select("#medshare");
  canvas.style("background-image","url(/static/img/loader.gif)");
  canvas.style("background-repeat","no-repeat");
  canvas.style("background-position","center center");

  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.category20();

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var line = d3.svg.line()
      .interpolate("cardinal")
      .x(function(d) { return x(d["date"]); })
      .y(function(d) { return y(d["total"]); });

  var div = canvas.append("div").attr("class","tooltip");

  var svg = canvas.append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  //Change the path to url for production use
  d3.json("http://128.199.120.29:8274/api/v1/mediashare", function(error, data) {
    canvas.attr("style","");
    data = data.result
    color.domain(d3.keys(data[0]["media"]));
    med_list = color.domain();
    //console.log(med_list)
    data.forEach(function(d) {
      d.date = parseDate(d["date"]);
    });

    var medias = color.domain().map(function(name) {
      return {
        name: name,
        values: data.map(function(d) {
          return {date: d["date"], total: d["media"][name]};
        })
      };
    });

    //console.log(medias)

    x.domain(d3.extent(data, function(d) { return d["date"]; }));

    y.domain([
      d3.min(medias, function(c) { return d3.min(c.values, function(v) { return v.total; }); }),
      d3.max(medias, function(c) { return d3.max(c.values, function(v) { return v.total; }); })
    ]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Total Articles");

    var med_num = color.domain().slice().reverse();

    function get_distance(d, padding){
      console.log(d.split(".").join("").split("/").join("")+" "+padding);
      padding += 25;
      var dist = 30 *(med_num.length);
      var stop = med_num.indexOf(d);
      for (var i=0;i<stop;++i){
        dist += (med_num[i].split(".")[0].length*6);
        dist += padding;
      }
      console.log(dist);
      return dist;
    }

    var legend = canvas.append("svg")
    // .attr("style","transform: translate(100px,-10px)")
    .attr("class", "legend")
    .attr("width", "100%")
    .attr("height", 50)
    .selectAll("g")
    .style("text-align","center")
    .style("cursor","pointer")
    .data(med_num)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate("+get_distance(d,20)+",20)"; })
    .on("click",function(d){
      var clicked = d3.select(this);

      new_d = d.split(".").join("").split("/").join("");
      console.log(new_d);

      //get element status from its attribute
      click_status = d3.select("#"+new_d).attr("clicked");

      //set active status
      var active = click_status == "true" ? false : true;

      //set display value according to element status
      this_opacity_val = active ? 0 : 1;
      other_opacity_val = active ? 1 : 0;

      //update dipslay according to element status
      d3.select("#"+new_d).transition().duration(250).style("opacity",this_opacity_val);
      d3.selectAll("."+new_d+"-dots").transition().duration(250).style("opacity",this_opacity_val);
      d3.selectAll("."+new_d+"-tips").transition().duration(250).style("display",function(){return active ? "none":"inline";});
      d.active = active;
      d3.select("#"+new_d).attr("clicked",active);

    });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("font-size","13px")
        .text(function(d) { return d.split(".")[0]; });

    var media = svg.selectAll(".media")
        .data(medias)
        .enter().append("g")
        .attr("class", "media")
        .attr("clicked","false")
        .attr("id",function(d){return d.name.split(".").join("").split("/").join("");});

    media.append("path")
        .attr("class", "line")
        .attr("d", function(d) { return line(d.values); })
        .style("stroke", function(d) { return color(d.name); })

    // Add legend on the last line of chart      
    // media.append("text")
    //   .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
    //   .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.total) + ")"; })
    //   .attr("x", 3)
    //   .attr("dy", ".35em")
    //   .text(function(d) { return d.name; });


    med_list.forEach(function(e){
      var dots = d3.svg.line()
        .interpolate("cardinal")
        .x(function(d) { return x(d["date"]); })
        .y(function(d) { return y(d["media"][e]); });

      var tip = d3.svg.line()
        .interpolate("cardinal")
        .x(function(d) { return x(d["date"]) - 30; })
        .y(function(d) { return y(d["media"][e]) - 20; });

      var teks = d3.svg.line()
        .interpolate("cardinal")
        .x(function(d) { return x(d["date"])-35; })
        .y(function(d) { return y(d["media"][e]) - 15; });

      cls = ".dot"+e.split(".").join("").split("/").join("")
      svg.selectAll(cls)
        .data(data)
        .enter().append("circle")
        .style("fill",color(e))
        .attr("date",function(d){return d["date"];})
        .attr("total",function(d){return d["media"][e];})
        .attr("cx", dots.x())
        .attr("cy", dots.y())
        .attr("class",function(d){return e.split(".").join("").split("/").join("")+"-dots";})
        .attr("r", 4)

      var node = svg.selectAll(cls)
        .data(data)
        .enter().append("g")
        .attr("transform", function(d, i) { return "scale(1,1)"; })
        .attr("class",e.split(".").join("").split("/").join("")+"-tips g-tips")
        .style("opacity","0")
        .on("mouseover",function(){
          var selected_dot = d3.select(this);
          selected_dot.transition().duration(100).style({opacity:'1'}).style({cursor:'pointer'})
        })
        .on("mouseout",function(){
          var selected_dot = d3.select(this);
          selected_dot.transition().duration(40).style({opacity:'0'});
        })

      node.append("rect")
        .attr("class", "tooltip")
        .style("fill","rgba(1,1,1,1)")
        .attr("date",function(d){return d["date"];})
        .attr("total",function(d){return d["media"][e];})
        .attr("x", tip.x())
        .attr("y", tip.y())
        .attr("rx", 2)
        .attr("ry", 2)
        .attr("width", 60)
        .attr("height", 34)

      node.append("foreignObject")
        .html(function(d){return "<div style='text-align:center;color:white;font-size:12px;'>"+String(d["date"]).substring(4,11)+"<br>"+d["media"][e]+"</div>";})
        .attr("x", teks.x())
        .attr("y", teks.y())
        .style("fill","white")
        .attr("width", 70)
        .attr("height", 40);
    })
  })
  .header("Content-Type","application/json")
  .send("POST",medshare_data);
}
// End media share

// Start media summary
function load_media_summary(){
  var width_medsum = $(window).width()/2.5,
    height_medsum = 300,
    radius_medsum = Math.min(width_medsum, height_medsum) / 2.7,
    padding_medsum = 0;

  //var color = d3.scale.ordinal()
  //  .range(["#F44336", "#FF9800", "#4FC3F7", "#3F51B5", "#009688", "#00E676", "#FFEB3B"]);
  var color_medsum = d3.scale.category20c();

  var percentageFormat_medsum = d3.format("%");

  var arc_medsum = d3.svg.arc()
      .outerRadius(radius_medsum)
      .innerRadius(0);

  var pie_medsum = d3.layout.pie()
      .value(function(d) { return d.total; });

  function sum(data){
    res = 0;
    Object.keys(data[0].media).forEach(function(d){res += data[0].media[d]});
    return res;  
  }

  var val = '';

  var canvas_medsum = d3.select("#medsum")
      .attr("width", width_medsum)
      .attr("height", height_medsum);
  
  canvas_medsum.style("background-image","url(/static/img/loader.gif)");
  canvas_medsum.style("background-repeat","no-repeat");
  canvas_medsum.style("background-position","center center");

  d3.json("http://128.199.120.29:8274/api/v1/mediashare/summary", function(error, data) {
  //d3.json("http://127.0.0.1:8274/api/v1/mediashare", function(error, data) {
    canvas_medsum.attr("style","");
    data = data.result
    color_medsum.domain(d3.keys(data[0]["media"]));
    // console.log(color.domain());
    data.forEach(function(d) {
      //console.log(d);
      d.total = color_medsum.domain().map(function(name) {
        return {name: name, total: d["media"][name]};
      });
    });

    var legend = canvas_medsum.append("svg")
        .attr("class", "legend")
        .attr("width", radius_medsum * 2)
        .attr("height", radius_medsum * 2)
        .selectAll("g")
        .data(color_medsum.domain().slice().reverse())
        .enter().append("g")
        .attr("transform", function(d, i) { return "translate(40," + (i * 25) + ")"; });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color_medsum);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("font-size","13px")
        .text(function(d) { return d+" ("+data[0]["media"][d]+")"; });

    var svg = canvas_medsum.selectAll(".pie")
        .data(data)
        .enter().append("svg")
        .attr("class", "pie")
        .attr("width", radius_medsum * 2)
        .attr("height", radius_medsum * 2)
        .append("g")
        .attr("transform", "translate(" + radius_medsum + "," + radius_medsum + ")");

    svg.selectAll(".arc")
        .data(function(d) { return pie_medsum(d.total); })
        .enter().append("path")
        .attr("class", "arc")
        .attr("d", arc_medsum)
        .style("fill", function(d) { return color_medsum(d.data.name); });

    svg.append("text")
        .attr("dy", ".35em")
        .style("text-anchor", "middle");
        // .text(function(d) { return "Media Summary"; });

    var gg = canvas_medsum.selectAll(".pie")
          .data(pie_medsum(data))
          .enter().append("g")
          .attr("class", "val");

    val = data[0].media;
    percent = color_medsum.domain();
    var i = 0;
    var tot = sum(data);
    percent.forEach(function(e){
      // console.log(e);
      svg.append("text")
        .attr("transform", function(d) {
          return "translate(" + arc_medsum.centroid(pie_medsum(d.total)[i]) + ")";
        })
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .style("font-size","13px")
        // .text(function(d) { return Math.floor((d.media[e]/tot)*100000)/1000+"%"; })
        .style("opacity","1");
        i +=1;
    });
    // console.log(color.domain());

  })
  .header("Content-Type","application/json")
  .send("POST",medsum_data);
}
// End media summary

// Start key opinion leader
function load_key_opinion_leader(){
  var width_kop = $(window).width() - ($(window).width()/2.5) - 15,
    height_kop = 300 - 5,
    radius_kop = Math.min(width_kop, height_kop) / 2.8,
    padding_kop = 10;

  var color = d3.scale.ordinal()
    .range(["#F44336", "#FF9800", "#4FC3F7", "#3F51B5", "#009688", "#00E676", "#FFEB3B","#FF5722","#76FF03","#F50057"]);

  var percentageFormat_kop = d3.format("%");

  var arc_kop = d3.svg.arc()
      .outerRadius(radius_kop)
      .innerRadius(0);

  var pie_kop = d3.layout.pie()
      .value(function(d) { return d.total; });


  var val = '';
  var canvas3 = d3.select("#keyop")
      .attr("width",width_kop)
      .attr("height",height_kop);
  canvas3.style("background-image","url(/static/img/loader.gif)");
  canvas3.style("background-repeat","no-repeat");
  canvas3.style("background-position","center center");

  d3.json("http://128.199.120.29:8274/api/v1/keyopinionleader", function(error, data) {
  //d3.json("http://127.0.0.1:8274/api/v1/mediashare", function(error, data) {
    function sum(d){
      res = 0;
      Object.keys(d[0].people).forEach(function(e){res += d[0].people[e]});
      return res;  
    }
    canvas3.attr("style","");
    data = data.result
    //console.log(data);
    color.domain(d3.keys(data[0]["people"]));
    // console.log(color.domain());
    data.forEach(function(d) {
      //console.log(d);
      d.total = color.domain().map(function(name) {
        return {name: name, total: d["people"][name]};
      });
    });

    

    var legend = canvas3.append("svg")
        .attr("class", "legend")
        .attr("width", radius_kop * 2 )
        .attr("height", radius_kop * 2)
        .selectAll("g")
        .data(color.domain().slice().reverse())
        .enter().append("g")
        .attr("transform", function(d, i) { return "translate(0," + i * 25 + ")"; });

    legend.append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("font-size","13px")
        .text(function(d) { return d+" ("+data[0]["people"][d]+")"; });

    var svg = canvas3.selectAll(".pie")
        .data(data)
        .enter().append("svg")
        .attr("class", "pie")
        .attr("width", radius_kop * 2)
        .attr("height", radius_kop * 2)
        .append("g")
        .attr("transform", "translate(" + radius_kop + "," + radius_kop + ")");

    svg.selectAll(".arc")
        .data(function(d) { return pie_kop(d.total); })
        .enter().append("path")
        .attr("class", "arc")
        .attr("d", arc_kop)
        .style("fill", function(d) { return color(d.data.name); });

    var gg = canvas3.selectAll(".pie")
          .data(pie_kop(data))
          .enter().append("g")
          .attr("class", "val");

    val = data[0].people;
    percent = color.domain();
    var i = 0;
    var tot = sum(data);
    percent.forEach(function(e){
      // console.log(e);
      svg.append("text")
        .attr("transform", function(d) {
          //console.log(arc.centroid(pie(d.total)[i]));
          return "translate(" + arc_kop.centroid(pie_kop(d.total)[i]) + ")";
        })
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .style("font-size","13px")
        .style("opacity","0")
        .text(function(d) { return Math.floor((d.people[e]/tot)*100000)/1000+"%"; });
        i +=1;
    });
    // console.log(color.domain());

  })
  .header("Content-Type","application/json")
  .send("POST",kol_data);
}
// End key opinion leader

// Start word frequency
function load_word_frequency(){
  var margin = {top: 20, right: 20, bottom: 50, left: 50},
    width = $(window).width() - margin.left - margin.right - 150,
    height = 300 - margin.top - margin.bottom;

  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")

  var canvas = d3.select("#word");
  canvas.style("background-image","url(/static/img/loader.gif)");
  canvas.style("background-repeat","no-repeat");
  canvas.style("background-position","center center");

  var svg = d3.select("#word").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // set SVG element to the highest layer on SVG
  d3.selection.prototype.moveToFront = function() {
    return this.each(function(){
      this.parentNode.appendChild(this);
    });
  };

  // set SVG element to its normal layer on SVG
  d3.selection.prototype.moveToBack = function() { 
      return this.each(function() { 
          var firstChild = this.parentNode.parentNode.parentNode.firstChild; 
          if (firstChild) { 
              this.parentNode.parentNode.parentNode.insertBefore(this, firstChild); 
          } 
      }); 
  };


  var selected;

  d3.json("http://128.199.120.29:8274/api/v1/wordfrequencymanual", function(error, data) {

    data = data.result[0].words;
    canvas.attr("style","");
    //console.log(data);
    x.domain(d3.keys(data).map(function(d) { return d; }));
    y.domain([0, d3.max(d3.keys(data), function(d) { return data[d]; })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
          .style("text-anchor","start")
          .style("transform","rotate(45deg)");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 10)
        .attr("dy", ".41em")
        .style("text-anchor", "end")
        .text("Total");

    var group = svg.selectAll(".tooltip")
      .data(d3.keys(data))
      .enter().append("g");
      
      group.append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(data[d]); })
        .attr("height", function(d) { return height - y(data[d]); })
        .on("mouseover",function(){
          selected = d3.select(this.parentNode).moveToFront()
          selected.select("g").transition().duration(100).style({opacity:'1'}).style({cursor:'pointer'})
        })
        .on("mouseout",function(){
          selected = d3.select(this.parentNode);
          selected.select("g").transition().duration(40).style({opacity:'0'});
        });

      
      var gg = group.append("g")
        .style("opacity","0");

      gg.append("rect")
        .attr("class", "tooltip")
        .style("fill","rgba(1,1,1,0.999999)")
        //.style("opacity","0")
        .attr("x", function(d){ return x(d);})
        .attr("y", function(d){ return y(data[d])-1;})
        .attr("width", 41)
        .attr("height", 24)
      
      gg.append("text")
        .style("fill","white")
        .style("font-size","13px")
        .attr("transform", function(d){ 
          return "translate("+(x(d)+5)+","+(y(data[d])+20)+")";
        })
        .attr("dy","-.35em")
        .text(function(d){return data[d];})

  })
  .header("Content-Type","application/json")
  .send("POST",wordfreq_data);
}
// End word frequency

