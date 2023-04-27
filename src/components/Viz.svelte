<script>
	import { onMount } from 'svelte';
	import { articleData } from '../routes/store';

	let time = 100;

	let newWords = [];
	let addedWords = new Set();

	$: {
		newWords = [];
		addedWords = new Set();
	}


	async function fetchData() {
		const res = await fetch(`/api/get`);
		newWords = await res.json();
		return newWords;
	}

	onMount(async () => {
		await fetchData();

		//  i have to use eventlisteners because svelte is an asshole
		// or i'm just not capable
		let animateElements = document.querySelectorAll('animate');
		animateElements.forEach((element) => {
			element.addEventListener('endEvent', () => {
				let word = element.parentElement?.textContent;
				if (wordInNewWords(word)) {
					addedWords.add(word);
				}
			});
		});
	});

	function wordInNewWords(word) {
		return newWords.includes(word);
	}
</script>

<div class="chart">
	{#if newWords.length == 0}
		<p>Loading...</p>
	{:else}
		<svg viewBox="0 0 760 536" preserveAspectRatio="none">
			<!-- <path
				id="default"
				d="m7,0v474.66c0,6.26,5.07,11.34,11.34,11.34h4.69c6.26,0,11.34-5.07,11.34-11.34V92.34c0-6.26,5.07-11.34,11.34-11.34h4.33c6.26,0,11.34,5.07,11.34,11.34v247.05c0,13.99,20.39,15.57,22.54,1.74l27.34-175.74c2.04-13.08-16.18-18.44-21.56-6.35h0c-.86,1.93-1.16,4.07-.87,6.16l32.97,237.42c1.82,13.09,20.76,13.01,22.47-.09l15.48-118.67c.4-3.1,2.08-5.9,4.62-7.73l198.93-143.23c8.18-5.89,5.18-18.72-4.76-20.38l-174.37-29.06c-7.42-1.24-13.96,4.96-13.13,12.43l7.06,63.51c.19,1.71.76,3.35,1.68,4.8l104.07,164.77c1.62,2.57,2.15,5.69,1.45,8.65l-32.85,139.63c-1.2,5.12-5.77,8.74-11.03,8.74h-60.69c-6.26,0-11.34-5.07-11.34-11.34v-91.97c0-3.01,1.19-5.89,3.32-8.02l179.83-179.83c7.14-7.14,19.35-2.08,19.35,8.02v271.8c0,6.26,5.07,11.34,11.34,11.34h143.83c6.26,0,11.34-5.07,11.34-11.34V83.34c0-6.26,5.07-11.34,11.34-11.34h212.66"
				stroke-width="16"
				fill="none"
			/> -->
			<path
				id="new"
				d="m7,0v474.66c0,6.26,5.07,11.34,11.34,11.34h4.69c6.26,0,11.34-5.07,11.34-11.34V92.34c0-6.26,5.07-11.34,11.34-11.34h4.33c6.26,0,11.34,5.07,11.34,11.34v247.05c0,13.99,20.39,15.57,22.54,1.74l27.34-175.74c2.04-13.08-16.18-18.44-21.56-6.35h0c-.86,1.93-1.16,4.07-.87,6.16l32.97,237.42c1.82,13.09,20.76,13.01,22.47-.09l15.48-118.67c.4-3.1,2.08-5.9,4.62-7.73l198.93-143.23c8.18-5.89,5.18-18.72-4.76-20.38l-174.37-29.06c-7.42-1.24-13.96,4.96-13.13,12.43l7.06,63.51c.19,1.71.76,3.35,1.68,4.8l104.07,164.77c1.62,2.57,2.15,5.69,1.45,8.65l-32.85,139.63c-1.2,5.12-5.77,8.74-11.03,8.74h-60.69c-6.26,0-11.34-5.07-11.34-11.34v-91.97c0-3.01,1.19-5.89,3.32-8.02l179.83-179.83c7.14-7.14,19.35-2.08,19.35,8.02v271.8c0,6.26,5.07,11.34,11.34,11.34h143.83c6.26,0,11.34-5.07,11.34-11.34V83.34c0-6.26,5.07-11.34,11.34-11.34h212.66"
				stroke-width="16"
				fill="none"
			/>
			{#each newWords as word, i}
				<text font-size="12" dy="4">
					<textPath xlink:href="#new" startOffset="-10%">
						{word}
						<animate
							attributeName="startOffset"
							from="0%"
							to="110%"
							begin="{i * 2}s"
							end="{i + time}s"
							dur="{time}s"
							repeatCount="indefinite"
						/>
					</textPath>
				</text>
			{/each}
		</svg>
	{/if}
</div>
<input type="range" bind:value={time} min="10" max="200" />

<style>
	.newWords {
		font-family: Arial, Helvetica, sans-serif;
		position: absolute;
		width: 21%;
		left: 73%;
		top: 26%;
		height: 71%;
		word-break: break-all;
		display: flex;
		align-items: flex-end;
	}

	.chart {
		position: relative;
		width: 100%;
		padding-left: .5rem;
		max-width: 1240px;
		margin: 0 auto;
	}

	text {
		font-family: Arial, Helvetica, sans-serif;
	}
	path {
		stroke: rgb(229, 226, 253);
	}
</style>
