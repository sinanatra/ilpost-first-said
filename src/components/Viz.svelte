<script>
	import { onMount } from 'svelte';
	import { scaleTime, timeFormat, zoom } from 'd3';

	let data = [];
	let xScale;
	let svg;
	let g;
	export let sortingOption;

	$: console.log(data);
	$: w = g?.getBoundingClientRect().width;
	$: h = g?.getBoundingClientRect().height + 20;

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
			.sort((a, b) => b.date - a.date);

		return datum;
	}

	onMount(async () => {
		data = await fetchData();
		xScale = scaleTime()
			.domain([data[0].date, data[data.length - 1].date])
			.range([0, 100]);
	});

	$: {
		if (sortingOption == 'Time') {
			data = data.sort((a, b) => b.date - a.date);
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
			<g bind:this={g}>
				{#each data as d, i}
					<a href={d.url} target="_blank">
						<text x={xScale(d.date)} y={20 + i * 20}>
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
		fill: blue;
	}

	.text {
		font-style: italic;
	}

	.highlight {
		fill: blue;
	}

	.date {
		fill: #666;
		font-size: 0.6em;
	}
</style>
