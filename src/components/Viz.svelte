<script>
	import { onMount } from 'svelte';
	import { scaleTime, timeFormat } from 'd3';
	import { axisBottom } from 'd3-axis';

	export let sortingOption;
	let data = [];
	let xScale;
	let svg;
	let g;
	let xAxis;

	$: w = g?.getBoundingClientRect().width;
	$: h = g?.getBoundingClientRect().height + 20;
	$: uniqueDates = [...new Set(data.map((item) => timeFormat('%Y-%m-%d')(item?.date)))];

	async function fetchData() {
		const res = await fetch(`/api/get`);
		const json = await res.json();
		const datum = json
			.filter((d) => d.date_added)
			.map((d) => ({
				...d,
				date: new Date(d.date_added),
				snippets: d.context.split(d.word)
			}))
			.sort((a, b) => a._id.toString().localeCompare(b._id.toString()));

		return datum;
	}

	onMount(async () => {
		data = await fetchData();
		xScale = scaleTime()
			.domain([data[0]?.date, data[data.length - 1]?.date])
			.range([0, 100]);
		xAxis = axisBottom(xScale);
	});

	$: {
		if (sortingOption == 'Time') {
			data = data.sort((a, b) => a._id.toString().localeCompare(b._id.toString()));
		} else if (sortingOption == 'Alphabetically') {
			data = data.sort((a, b) => a.word.localeCompare(b.word));
		}
	}
</script>

<section>
	{#if data.length === 0}
		<p>Loading...</p>
	{:else}
		<svg bind:this={svg} height="{h || 100}px" width="{w || 100}px">
			<g class="dates">
				{#each uniqueDates as d, i}
					{#if i % 20 === 0}
						<text class="data" x={xScale(new Date(d))} y="10">{d}</text>
						<line x1={xScale(new Date(d))} y1="10" x2={xScale(new Date(d))} y2={h} />
					{/if}
				{/each}
			</g>
			<g bind:this={g}>
				{#each data as d, i}
					<a href={d.url} target="_blank">
						<text x={xScale(d.date)} y={40 + i * 22}>
							<tspan class="text">...</tspan>
							<tspan class="text">{d.snippets[0]}</tspan>
							<tspan class="highlight">{d.word}</tspan>
							<tspan class="text">{d.snippets[1]}</tspan>
							<tspan class="text">...</tspan>
							<tspan class="date">{timeFormat('%Y-%m-%d')(d.date)}</tspan>
						</text>
					</a>
				{/each}
			</g>
		</svg>
	{/if}
</section>

<style>
	section {
		overflow: scroll;
		padding: 10px;
	}

	a:hover {
		fill: #ffd53d;
	}

	.text {
		font-style: italic;
	}

	.highlight {
		fill: #2da8c6;
	}

	.date {
		fill: #666;
		font-size: 0.6em;
	}

	.data {
		fill: #a2a2a2;
		text-anchor: start;
	}

	line {
		stroke: #a2a2a2;
		stroke-dasharray: 1, 2;
	}
</style>
