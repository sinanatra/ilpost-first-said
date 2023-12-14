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
	let lh = 22;

	$: w = g?.getBoundingClientRect().width;
	$: h = g?.getBoundingClientRect().height + lh + 5;

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
			.sort((a, b) => b.date_added.toString().localeCompare(a.date_added.toString()));

		return datum;
	}

	onMount(async () => {
		data = await fetchData();
		xScale = scaleTime()
			.domain([data[0]?.date, data[data.length - 1]?.date])
			.range([0, 800]);
		xAxis = axisBottom(xScale);
	});

	$: {
		if (sortingOption == 'Time') {
			data = data.sort((a, b) => b.date_added.toString().localeCompare(a.date_added.toString()));
		} else if (sortingOption == 'Alphabetically') {
			data = data.sort((a, b) => a.word.localeCompare(b.word));
		} else if (sortingOption == 'Length') {
			data = data.sort((a, b) => b.word.length - a.word.length);
		}
	}

	$: uniqueDates = [...new Set(data.map((item) => timeFormat('%Y-%m-%d')(item?.date)))].sort(
		(a, b) => b.localeCompare(a)
	);
</script>

<section>
	{#if data.length === 0}
		<p>Caricamento delle parole più recenti...</p>
	{:else}
		<svg bind:this={svg} height="{h || 100}px" width="{w || 100}px">
			<g class="dates">
				{#each uniqueDates as d, i}
					{#if i % 5 === 0}
						<text class="date" x={xScale(new Date(d))} y="10">
							{new Date(d)
								.toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' })
								.replace(/\b\w/g, (c) => c.toUpperCase())}
						</text>
						<line x1={xScale(new Date(d))} y1="14" x2={xScale(new Date(d))} y2={h || 0} />
					{/if}
				{/each}
			</g>
			<g bind:this={g}>
				{#each data as d, i}
					<text x={xScale(d.date)} y={40 + i * lh}>
						<tspan class="text">...</tspan><tspan class="text">{@html d.snippets[0] || ''}</tspan
						><tspan class="highlight">{d.word}</tspan><tspan class="text"
							>{@html d.snippets[1] || ''}</tspan
						><tspan class="text">...</tspan>
						<a href={d.url} target="_blank">
							<tspan class="date"
								>Menzionata il {new Date(d.date)
									.toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' })
									.replace(/\b\w/g, (c) => c.toUpperCase())} alle: {timeFormat('%H:%M')(d.date)} ↗</tspan
							>
						</a>
					</text>
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

	a tspan:hover {
		fill: var(--color-1);
	}

	.text {
		font-style: italic;
	}

	.highlight {
		fill: var(--color-1);
	}

	.date,
	a {
		fill: #666;
		font-size: 0.8em;
	}

	line {
		stroke: #b6b6b6;
		stroke-dasharray: 8, 8;
	}
</style>
