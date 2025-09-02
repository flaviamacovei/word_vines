import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface DataDisplayProps {
    data: any;
}

const width = 500;
const height = 400;
const margin = { top: 40, right: 20, bottom: 40, left: 40 };

const DataDisplay: React.FC<DataDisplayProps> = ({ data }) => {
    const svgRef = useRef<SVGSVGElement | null>(null);

    useEffect(() => {
        if (!data || !data.synonyms) return;

        const synonyms: Array<Record<string, Array<number>>> = data.synonyms;

        // Flatten synonyms to [{word, x, y}]
        const points = synonyms.map(syn => {
            const word = Object.keys(syn)[0];
            const [x, y] = syn[word];
            return { word, x, y };
        });

        // Set up scales
        const xExtent = d3.extent(points, d => d.x) as [number, number];
        const yExtent = d3.extent(points, d => d.y) as [number, number];

        const xScale = d3.scaleLinear()
            .domain(xExtent)
            .range([margin.left, width - margin.right]);

        const yScale = d3.scaleLinear()
            .domain(yExtent)
            .range([height - margin.bottom, margin.top]);

        // Clear previous svg
        d3.select(svgRef.current).selectAll("*").remove();

        const svg = d3.select(svgRef.current);

        // Axes
        // svg.append("g")
        //     .attr("transform", `translate(0,${height - margin.bottom})`)
        //     .call(d3.axisBottom(xScale));

        // svg.append("g")
        //     .attr("transform", `translate(${margin.left},0)`)
        //     .call(d3.axisLeft(yScale));

        // Points
        svg.selectAll("circle")
            .data(points)
            .enter()
            .append("circle")
            .attr("cx", d => xScale(d.x))
            .attr("cy", d => yScale(d.y))
            .attr("r", 6)
            .attr("fill", "#4682b4");

        // Labels
        svg.selectAll("text.synonym-label")
            .data(points)
            .enter()
            .append("text")
            .attr("class", "synonym-label")
            .attr("x", d => xScale(d.x) + 8)
            .attr("y", d => yScale(d.y) - 8)
            .text(d => d.word)
            .attr("font-size", "12px")
            .attr("fill", "#333");

        // Center word label
        if (data.centre) {
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", margin.top / 2)
                .attr("text-anchor", "middle")
                .text(`Center word: ${data.centre}`)
                .attr("font-size", "16px")
                .attr("font-weight", "bold");
        }
    }, [data]);

    return (
        <div>
            <svg ref={svgRef} width={width} height={height} />
        </div>
    );
};

export default DataDisplay;