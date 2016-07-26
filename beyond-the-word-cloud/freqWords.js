			var width 		= 800;
			var height 		= 600;
			var diameter	= 550, format = d3.format(",d");

			var color		= d3.scale.ordinal()
								.range(["#0000FF", "#009933" , "#FF0000"]);

			var canvas 		= d3.select("#fwords")
								.append("svg")
								.attr("width", diameter)
								.attr("height", diameter);

			var pack		= d3.layout.pack()
								.sort(null)
								.size([diameter, diameter])
								.padding(10);

			var tooltip = d3.select("body")
							.append("div")
							.style("position", "absolute")
							.style("z-index", "10")
							.style("visibility", "hidden")
							.style("color", "white")
							.style("padding", "8px")
							.style("background-color", "rgba(0, 0, 0, 0.75)")
							.style("border-radius", "6px")
							.style("font", "12px sans-serif")
							.text("tooltip");

			var May 		= "/May/word_counts_top_results.csv";
			var April 		= "/April/word_counts_top_results.csv";
			var March 		= "/March/word_counts_top_results.csv";
			var February 	= "/February/word_counts_top_results.csv";

		function updateData(dataSource)
		{
			var chart2 = d3.select("svg");
			chart2.selectAll("*").remove();
			d3.csv(dataSource, function(data)
			{
				var node = canvas.selectAll(".node")
							   .data(
							         	pack.nodes(
												 	{
														children: data
													}
												  ).filter(function(d)
															{
																return !d.children;
															}),
															function(d)
																{
																	return d.word
																}
									);

				var nodeEnter = node.enter()
									.append("g")
										.attr("class", "node")
										.attr("transform", function (d)
										{
											return "translate("
													+ d.x
													+ ","
													+ d.y
													+ ")";
										});

				// re-use enter selection for circles
				nodeEnter.append("circle")
						 .attr("r", function (d)
									{
										return d.r;
									})
						 .attr("opacity", 0.25)
						 .attr("stroke", "#000000")
						 .attr("stroke-width", "2")
						 .style("fill", function (d)
											{
												var val = color(d.value);
												return color(d.value);
											})
						.on("mouseover", function(d)
											{
												tooltip.text(d.word + ": " + d.value);
												tooltip.style("visibility", "visible");
											})
						.on("mousemove", function()
											{
											    return tooltip.style("top", (d3.event.pageY-10)+"px")
															   .style("left",(d3.event.pageX+10)+"px");
											})
						.on("mouseout", function()
											{
												return tooltip.style("visibility", "hidden");
											});


				nodeEnter.append("text")
					.text(function(d)
							{
								//don't display name if node has children
								return d.word;
							})
					.attr("dy", ".3em")
					.style("text-anchor", "middle")
					.style("pointer-events", "none")

				node.exit()
					.attr('opacity',0)
					.attr("r",0)
					.remove();
			})
		}

		updateData(May);

		d3.selectAll('.opts')
		  .on('click', function()
							{
								var dataSource = eval(d3.select(this).property('value'));
								updateData(dataSource);
							});

